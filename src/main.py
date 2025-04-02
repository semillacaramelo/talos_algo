import asyncio
from collections import deque
from src.api.deriv_api_handler import connect_deriv_api, place_trade_order, disconnect
from src.data.data_handler import get_historical_data, subscribe_to_ticks
from src.models.signal_model import train_or_load_model, generate_signal, HOLD, BUY, SELL, LONG_MA_PERIOD
from config.settings import INSTRUMENT, TIMEFRAME_SECONDS, HISTORICAL_BARS_COUNT
from src.utils.logger import setup_logger
import pandas as pd

# Set up logger
logger = setup_logger()

# --- Risk Management Placeholders --- 
MAX_CONCURRENT_TRADES = 1
TRADE_VOLUME = 0.01
STOP_LOSS_POINTS = 10
TAKE_PROFIT_POINTS = 20

# --- State Management --- 
open_trades = []
# Use deque to store recent ticks for signal generation
recent_ticks_deque = deque(maxlen=LONG_MA_PERIOD + 5)

# --- Tick Handler Function ---
def handle_tick(tick_data_msg):
    global recent_ticks_deque, open_trades
    
    if not isinstance(tick_data_msg, dict) or 'tick' not in tick_data_msg:
        return
    
    current_tick = tick_data_msg['tick']
    logger.info(f"Processing tick in handler: {current_tick}")
    current_price = current_tick.get('quote')
    current_time = current_tick.get('epoch')
    
    # Accumulate tick data for signal generation
    if current_price and current_time:
        recent_ticks_deque.append({'time': pd.to_datetime(current_time, unit='s'), 'close': current_price})
    
    # Convert deque to DataFrame for signal generation
    if len(recent_ticks_deque) >= 2:  # Need at least 2 points for previous comparison
        signal_df = pd.DataFrame(list(recent_ticks_deque))
        
        # Generate trading signal
        signal = generate_signal(signal_df)
        if signal != HOLD:
            logger.info(f"Generated Signal: {signal}")
        
        # Risk management check
        can_trade = len(open_trades) < MAX_CONCURRENT_TRADES
        
        # Trading logic
        if can_trade and current_price and signal in (BUY, SELL):
            logger.info(f"{signal} signal received. Trade execution would happen here.")
            # Commented out for safety until verified with correct API parameters
            # if signal == BUY:
            #     sl_price = current_price - STOP_LOSS_POINTS
            #     tp_price = current_price + TAKE_PROFIT_POINTS
            #     # Would call place_trade_order here with verified parameters
            # elif signal == SELL:
            #     sl_price = current_price + STOP_LOSS_POINTS
            #     tp_price = current_price - TAKE_PROFIT_POINTS
            #     # Would call place_trade_order here with verified parameters

async def main():
    logger.info("Bot is starting...")
    api = None
    subscription_data = None

    try:
        # Connect to API
        api = await connect_deriv_api()
        if not api:
            logger.error("Connection failed.")
            return
        logger.info("Connection successful.")

        # Get historical data
        historical_df = await get_historical_data(api, INSTRUMENT, TIMEFRAME_SECONDS, HISTORICAL_BARS_COUNT)
        if not historical_df.empty:
            logger.info("Successfully fetched historical data.")
        else:
            logger.warning("Historical data is empty.")

        # Initialize model
        model = train_or_load_model()
        logger.info(f"Model status: {model.get('status')}")

        # Subscribe to tick stream using ReactiveX Observable
        subscription_data = await subscribe_to_ticks(api, INSTRUMENT)
        
        if subscription_data:
            logger.info(f"Subscription initiated for {INSTRUMENT}. Waiting for ticks...")
            
            # The tick handling is now done by the observer callbacks in subscribe_to_ticks
            # We just need to keep the main coroutine alive
            await asyncio.sleep(30)  # Run for 30 seconds
            
        else:
            logger.error(f"Failed to initiate subscription for {INSTRUMENT}.")

    except Exception as e:
        logger.exception("Error during main execution.")
    finally:
        # Clean up subscription if it exists
        if subscription_data and 'disposable' in subscription_data:
            try:
                logger.info("Disposing subscription...")
                # Ensure we dispose of the subscription and wait a moment for cleanup
                subscription_data['disposable'].dispose()
                await asyncio.sleep(0.2)  # Give some time for cleanup
                logger.info("Subscription disposed.")
            except Exception as e:
                logger.exception("Error disposing subscription")

        # Proper disconnect with error handling
        if api:
            try:
                # Ensure all pending API operations complete
                await asyncio.sleep(0.5)  # Wait for any pending operations to complete
                # Properly disconnect using our improved function
                await disconnect(api)
                # Give time for event loop to process the disconnect completely
                await asyncio.sleep(0.5)
            except Exception as e:
                logger.exception("Error during API disconnect")

if __name__ == "__main__":
    asyncio.run(main())