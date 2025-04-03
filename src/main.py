import asyncio
from collections import deque
import sys
import os

# Add the project root directory to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.api.deriv_api_handler import connect_deriv_api, disconnect, get_option_proposal, buy_option_contract, subscribe_to_contract_updates
from src.data.data_handler import get_historical_data, subscribe_to_ticks
from src.models.signal_model import train_or_load_model, generate_signal, HOLD, BUY, SELL, MIN_FEATURE_POINTS
from config.settings import (INSTRUMENT, TIMEFRAME_SECONDS, HISTORICAL_BARS_COUNT,
                            OPTION_DURATION, OPTION_DURATION_UNIT, STAKE_AMOUNT, 
                            BASIS, CURRENCY, MAX_CONCURRENT_TRADES)
from src.utils.logger import setup_logger
import pandas as pd

# Set up logger
logger = setup_logger()

# --- State Management --- 
# Change to dictionary to store contracts with their subscriptions
active_contracts = {}
# Use deque to store recent ticks for signal generation - update size based on feature requirements
recent_ticks_deque = deque(maxlen=MIN_FEATURE_POINTS + 10)  # Add some buffer

# --- Tick Handler Function ---
async def handle_tick(tick_data_msg, api_obj=None, model_obj=None):
    global recent_ticks_deque, active_contracts
    
    # Use the passed api_obj instead of relying on a global variable
    if not api_obj:
        logger.error("API object is not provided to handle_tick.")
        return
        
    # Check if model is provided
    if not model_obj:
        logger.error("ML model is not provided to handle_tick.")
        return
        
    if not isinstance(tick_data_msg, dict) or 'tick' not in tick_data_msg:
        return
    
    current_tick = tick_data_msg['tick']
    logger.info(f"Processing tick in handler: {current_tick}")
    current_price = current_tick.get('quote')
    current_time = current_tick.get('epoch')
    
    # Accumulate tick data for signal generation
    if current_price and current_time:
        recent_ticks_deque.append({'time': pd.to_datetime(current_time, unit='s'), 'close': current_price})
    
    # Generate trading signal using ML model
    if len(recent_ticks_deque) >= MIN_FEATURE_POINTS:  # Make sure we have enough data for feature engineering
        # Generate signal by passing the model and the entire deque
        signal = generate_signal(model_obj, recent_ticks_deque)
        
        if signal != HOLD:
            logger.info(f"Generated ML Signal: {signal}")
        
        # Risk management check
        can_trade = len(active_contracts) < MAX_CONCURRENT_TRADES
        
        # Trading logic for Digital Options
        if can_trade and current_price and signal in (BUY, SELL):
            try:
                if signal == BUY:
                    # CALL option - prediction that price will RISE
                    logger.info(f"BUY signal received. Requesting RISE (CALL) option proposal...")
                    proposal_response = await get_option_proposal(
                        api_obj, INSTRUMENT, "CALL", OPTION_DURATION, OPTION_DURATION_UNIT, 
                        CURRENCY, STAKE_AMOUNT, BASIS
                    )
                    
                    if proposal_response and proposal_response.get('proposal'):
                        proposal = proposal_response.get('proposal')
                        proposal_id = proposal.get('id')
                        ask_price = proposal.get('ask_price')
                        
                        logger.info(f"Buying RISE (CALL) option contract with proposal ID: {proposal_id}")
                        buy_confirmation = await buy_option_contract(api_obj, proposal_id, ask_price)
                        
                        if buy_confirmation and buy_confirmation.get('buy'):
                            contract_info = buy_confirmation.get('buy')
                            contract_id = contract_info.get('contract_id')
                            logger.info(f"Successfully purchased RISE contract ID: {contract_id}")
                            
                            # Subscribe to contract updates
                            contract_subscription_disposable = await subscribe_to_contract_updates(
                                api_obj, contract_id, contract_update_handler_wrapper
                            )
                            
                            # Store the contract with its subscription
                            if contract_subscription_disposable:
                                active_contracts[contract_id] = {
                                    'details': {
                                        'type': 'CALL',
                                        'entry_price': current_price,
                                        'stake': STAKE_AMOUNT,
                                        'purchase_time': contract_info.get('purchase_time'),
                                        'expiry_time': contract_info.get('start_time') + OPTION_DURATION * (
                                            60 if OPTION_DURATION_UNIT == 'm' else 
                                            1 if OPTION_DURATION_UNIT == 's' else 
                                            10  # Approximation for ticks
                                        )
                                    },
                                    'disposable': contract_subscription_disposable
                                }
                                logger.info(f"Stored active contract {contract_id} with its subscription.")
                            else:
                                logger.error(f"Failed to subscribe to updates for contract {contract_id}")
                
                elif signal == SELL:
                    # PUT option - prediction that price will FALL
                    logger.info(f"SELL signal received. Requesting FALL (PUT) option proposal...")
                    proposal_response = await get_option_proposal(
                        api_obj, INSTRUMENT, "PUT", OPTION_DURATION, OPTION_DURATION_UNIT, 
                        CURRENCY, STAKE_AMOUNT, BASIS
                    )
                    
                    if proposal_response and proposal_response.get('proposal'):
                        proposal = proposal_response.get('proposal')
                        proposal_id = proposal.get('id')
                        ask_price = proposal.get('ask_price')
                        
                        logger.info(f"Buying FALL (PUT) option contract with proposal ID: {proposal_id}")
                        buy_confirmation = await buy_option_contract(api_obj, proposal_id, ask_price)
                        
                        if buy_confirmation and buy_confirmation.get('buy'):
                            contract_info = buy_confirmation.get('buy')
                            contract_id = contract_info.get('contract_id')
                            logger.info(f"Successfully purchased FALL contract ID: {contract_id}")
                            
                            # Subscribe to contract updates
                            contract_subscription_disposable = await subscribe_to_contract_updates(
                                api_obj, contract_id, contract_update_handler_wrapper
                            )
                            
                            # Store the contract with its subscription
                            if contract_subscription_disposable:
                                active_contracts[contract_id] = {
                                    'details': {
                                        'type': 'PUT',
                                        'entry_price': current_price,
                                        'stake': STAKE_AMOUNT,
                                        'purchase_time': contract_info.get('purchase_time'),
                                        'expiry_time': contract_info.get('start_time') + OPTION_DURATION * (
                                            60 if OPTION_DURATION_UNIT == 'm' else 
                                            1 if OPTION_DURATION_UNIT == 's' else 
                                            10  # Approximation for ticks
                                        )
                                    },
                                    'disposable': contract_subscription_disposable
                                }
                                logger.info(f"Stored active contract {contract_id} with its subscription.")
                            else:
                                logger.error(f"Failed to subscribe to updates for contract {contract_id}")
            
            except Exception as e:
                logger.exception(f"Error in Digital Options trading execution")

# Non-async wrapper for the async contract update handler
def contract_update_handler_wrapper(message):
    """
    Non-async wrapper function that schedules the async handler on the event loop.
    This solves the 'coroutine not awaited' warning.
    
    Parameters:
        message (dict): The message received from the proposal_open_contract stream
    """
    asyncio.create_task(handle_contract_update(message))

async def handle_contract_update(message):
    """
    Handle updates for an open contract.
    
    Parameters:
        message (dict): The message received from the proposal_open_contract stream
    """
    global active_contracts
    
    try:
        # Verify structure and extract contract details
        if 'proposal_open_contract' not in message:
            logger.warning("Received contract update with missing proposal_open_contract key")
            return
            
        contract = message['proposal_open_contract']
        
        # Extract the contract_id and is_sold status
        try:
            contract_id = contract['contract_id']
            is_sold = contract.get('is_sold', 0)
            
            # Log brief update
            logger.debug(f"Contract update received for ID: {contract_id}")
            
            # Check if contract is finished
            if is_sold == 1:
                # Extract profit information
                profit = contract.get('profit', 0)
                logger.info(f"Contract {contract_id} is now finished. Profit/Loss: {profit}")
                
                # Find and remove from active_contracts
                if contract_id in active_contracts:
                    # First dispose of the subscription
                    try:
                        active_contracts[contract_id]['disposable'].dispose()
                        logger.info(f"Disposed subscription for contract {contract_id}")
                    except Exception as e:
                        logger.error(f"Error disposing subscription for contract {contract_id}: {e}")
                    
                    # Then remove from active contracts
                    active_contracts.pop(contract_id)
                    logger.info(f"Removed contract {contract_id} from active_contracts. Active contracts remaining: {len(active_contracts)}")
                else:
                    logger.warning(f"Contract {contract_id} marked as sold but not found in active_contracts")
        
        except KeyError as e:
            logger.error(f"Missing expected key in contract update: {e}")
            
    except Exception as e:
        logger.exception("Error processing contract update")

async def main():
    logger.info("Bot is starting...")
    subscription_data = None
    api = None

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

        # Initialize model - Load ONCE at startup
        model = train_or_load_model()
        
        # Check if model loaded successfully
        if model is None:
            logger.critical("Failed to load ML model. Bot cannot proceed with ML strategy.")
            return
            
        logger.info(f"ML model loaded successfully and ready for predictions")

        # Subscribe to tick stream using ReactiveX Observable
        # Pass both the api object and model object to be used in handle_tick
        subscription_data = await subscribe_to_ticks(api, INSTRUMENT, api_ref=api, model_ref=model)
        
        if subscription_data:
            logger.info(f"Subscription initiated for {INSTRUMENT}. Waiting for ticks...")
            
            # The tick handling is now done by the observer callbacks in subscribe_to_ticks
            # We just need to keep the main coroutine alive
            await asyncio.sleep(300)  # Run for 5 minutes (longer for testing)
            
        else:
            logger.error(f"Failed to initiate subscription for {INSTRUMENT}.")

    except Exception as e:
        logger.exception("Error during main execution.")
    finally:
        # Clean up subscriptions
        if subscription_data and 'disposable' in subscription_data:
            try:
                logger.info("Disposing tick subscription...")
                subscription_data['disposable'].dispose()
                await asyncio.sleep(0.2)  # Give some time for cleanup
                logger.info("Tick subscription disposed.")
            except Exception as e:
                logger.exception("Error disposing tick subscription")

        # Clean up any active contract subscriptions
        if active_contracts:
            try:
                logger.info(f"Disposing {len(active_contracts)} active contract subscriptions...")
                for contract_id, contract_data in list(active_contracts.items()):
                    try:
                        contract_data['disposable'].dispose()
                        logger.info(f"Disposed subscription for contract {contract_id}")
                    except Exception as e:
                        logger.error(f"Error disposing subscription for contract {contract_id}: {e}")
                logger.info("All contract subscriptions disposed.")
            except Exception as e:
                logger.exception("Error during contract subscriptions cleanup")

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