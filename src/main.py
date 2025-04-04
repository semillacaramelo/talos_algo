import sys
import os
import asyncio
from collections import deque
from datetime import datetime
import pandas as pd
from typing import Dict, Optional, Any, Tuple, List

from src.api.deriv_api_handler import DerivAPIWrapper
from src.models.signal_model import train_or_load_model, generate_signal
from config.settings import (
    OPTION_DURATION, OPTION_DURATION_UNIT, BASIS, CURRENCY,
    MAX_CONCURRENT_TRADES, DYNAMIC_STAKE_PERCENT, MIN_STAKE_AMOUNT,
    MAX_STAKE_AMOUNT, MAX_DAILY_LOSS
)

class TradingBot:
    def __init__(self, api_key: str = ""):
        # Use API_TOKEN from settings if no api_key provided
        from config.settings import API_TOKEN
        self.api_key = api_key or API_TOKEN
        if not self.api_key:
            raise ValueError("API key is required. Set DERIV_DEMO_API_TOKEN environment variable.")
        self.api = DerivAPIWrapper(self.api_key)
        self.active_contracts: Dict[str, dict] = {}
        self.recent_ticks_deque = deque(maxlen=50)  # Store more points than needed
        self.daily_pnl = 0.0
        self.last_pnl_reset = datetime.now().date()
        self.model = None
        self.scaler = None
        self.is_running = False

    async def initialize(self):
        """Initialize the bot by loading models and connecting to API."""
        try:
            print("Loading ML model and scaler...")
            self.model, self.scaler = train_or_load_model()
            if not self.model or not self.scaler:
                # Try to create a dummy model as fallback
                from src.models.dummy_model import create_dummy_model
                print("Loading from file failed, creating dummy model...")
                self.model, self.scaler = create_dummy_model()
                if not self.model or not self.scaler:
                    raise ValueError("Failed to load model or create dummy model")
            print("Model and scaler successfully loaded or created")
            await self.api.connect()
        except Exception as e:
            print(f"Initialization error: {e}")
            raise ValueError(f"Failed to initialize: {e}")

    async def _get_dynamic_stake(self) -> float:
        """Calculate dynamic stake based on account balance."""
        try:
            # Access the underlying DerivAPI object
            api = self.api.api
            if not api:
                print("API not initialized, using minimum stake")
                return MIN_STAKE_AMOUNT
                
            # Get balance using the official API
            balance = await api.balance()
            
            # Parse the balance response
            if 'error' in balance:
                print(f"Failed to get balance: {balance['error'].get('message', 'Unknown error')}")
                return MIN_STAKE_AMOUNT
                
            # Extract the balance value
            account_balance = float(balance['balance']['balance'])
            stake = account_balance * DYNAMIC_STAKE_PERCENT
            return max(min(stake, MAX_STAKE_AMOUNT), MIN_STAKE_AMOUNT)
        except Exception as e:
            print(f"Error calculating stake: {e}")
            return MIN_STAKE_AMOUNT

    async def _check_trading_limits(self) -> bool:
        """Check if trading should proceed based on risk limits."""
        current_date = datetime.now().date()
        if current_date > self.last_pnl_reset:
            self.daily_pnl = 0.0
            self.last_pnl_reset = current_date
            print("Daily P&L reset for new trading day")

        if self.daily_pnl < -MAX_DAILY_LOSS:
            print(f"Daily loss limit of ${MAX_DAILY_LOSS} reached")
            return False

        if len(self.active_contracts) >= MAX_CONCURRENT_TRADES:
            print("Maximum concurrent trades reached")
            return False

        return True

    async def handle_tick(self, tick_data: dict):
        """Process new tick data and potentially execute trades."""
        try:
            # Validate tick_data structure
            if not tick_data or 'tick' not in tick_data:
                print("Invalid tick data received")
                return
                
            # Update tick history
            self.recent_ticks_deque.append({
                'timestamp': tick_data['tick']['epoch'],
                'close': float(tick_data['tick']['quote']),
                'high': float(tick_data['tick']['quote']),
                'low': float(tick_data['tick']['quote']),
                'open': float(tick_data['tick']['quote'])
            })

            # Check if we have enough data and can trade
            if not await self._check_trading_limits():
                return

            # Log the tick data for debugging
            print(f"Received tick: {tick_data['tick']['symbol']} = {tick_data['tick']['quote']}")
            
            # Convert deque to DataFrame for analysis
            df = pd.DataFrame(list(self.recent_ticks_deque))

            # Generate trading signal
            signal = generate_signal(self.model, self.scaler, df)
            if not signal:
                return

            # Calculate stake
            stake_amount = await self._get_dynamic_stake()

            # Execute trade based on signal
            if signal == "BUY":
                contract_type = "CALL"
            else:  # SELL signal
                contract_type = "PUT"
                
            # Prepare proposal request
            from config.settings import INSTRUMENT, OPTION_DURATION, OPTION_DURATION_UNIT, BASIS, CURRENCY
            proposal_request = {
                "proposal": 1,
                "amount": stake_amount,
                "basis": BASIS,
                "contract_type": contract_type,
                "currency": CURRENCY,
                "duration": OPTION_DURATION,
                "duration_unit": OPTION_DURATION_UNIT,
                "symbol": INSTRUMENT,
            }
            
            # Get API object
            api = self.api.api
            if not api:
                print("API not initialized")
                return

            # Get proposal using the official API
            proposal = await api.proposal(proposal_request)

            if not proposal or 'error' in proposal:
                print(f"Proposal error: {proposal.get('error', {}).get('message', 'Unknown error')}")
                return

            # Buy contract using the official API
            buy_request = {
                "buy": proposal['proposal']['id'],
                "price": proposal['proposal']['ask_price']
            }
            buy_response = await api.buy(buy_request)

            if 'error' in buy_response:
                print(f"Buy error: {buy_response['error']['message']}")
                return

            # Track contract
            contract_id = buy_response['buy']['contract_id']
            self.active_contracts[contract_id] = {
                'type': signal,
                'stake': stake_amount,
                'entry_time': datetime.now()
            }

            # Subscribe to contract updates directly
            api = self.api.api
            
            # Define wrapper to handle async callback
            def contract_update_wrapper(message):
                # Schedule the async function in the event loop
                asyncio.create_task(self.handle_contract_update(message))
                
            # Use the official API to subscribe to contract updates
            contract_request = {
                "proposal_open_contract": 1,
                "contract_id": contract_id,
                "subscribe": 1
            }
            
            # Subscribe to contract updates
            contract_observable = await api.subscribe(contract_request)
            
            # Register our callback wrapper
            contract_subscription = contract_observable.subscribe(contract_update_wrapper)
            
            # Store the subscription in our active contracts dict for cleanup
            self.active_contracts[contract_id]['subscription'] = contract_subscription

        except Exception as e:
            print(f"Error in handle_tick: {e}")

    async def handle_contract_update(self, update_data: dict):
        """Handle contract status updates."""
        try:
            contract_id = update_data['proposal_open_contract']['contract_id']

            if update_data['proposal_open_contract']['is_sold'] == 1:
                profit = float(update_data['proposal_open_contract']['profit'])
                self.daily_pnl += profit

                print(f"Contract {contract_id} finished. Profit: ${profit:.2f}, Daily P&L: ${self.daily_pnl:.2f}")

                if contract_id in self.active_contracts:
                    del self.active_contracts[contract_id]

        except Exception as e:
            print(f"Error in handle_contract_update: {e}")

    def get_status(self):
        """Get the current status of the trading bot."""
        return {
            'is_running': getattr(self, 'is_running', False),
            'active_contracts': len(self.active_contracts)
        }
        
    async def start(self):
        """Start the trading bot."""
        if getattr(self, 'is_running', False):
            return False
            
        self.is_running = True
        # Start the bot in a separate task
        asyncio.create_task(self.run())
        return True
        
    async def stop(self):
        """Stop the trading bot."""
        self.is_running = False
        return True
        
    async def run(self):
        """Main bot execution loop."""
        try:
            await self.initialize()

            # Subscribe to price feed
            from config.settings import INSTRUMENT
            from src.utils.logger import setup_logger
            logger = setup_logger()
            
            # Create a non-async callback that will schedule the async function
            def tick_callback_wrapper(message):
                if message and 'tick' in message:
                    logger.info(f"Received tick: {message['tick']['symbol']} = {message['tick']['quote']}")
                    # Schedule the async function in the event loop
                    asyncio.create_task(self.handle_tick(message))
            
            # Subscribe to ticks using the official API library
            from config.settings import INSTRUMENT
            
            # Subscribe to ticks using official Deriv API
            tick_observable = await self.api.api.subscribe({"ticks": INSTRUMENT, "subscribe": 1})
            
            # Subscribe to the observable with our non-async wrapper
            tick_subscription = tick_observable.subscribe(tick_callback_wrapper)
            
            # Store the subscription for later cleanup
            self.tick_subscription = tick_subscription
            
            logger.info(f"Successfully subscribed to ticks for {INSTRUMENT}")

            # Keep the bot running
            while getattr(self, 'is_running', False):
                await asyncio.sleep(1)

        except Exception as e:
            print(f"Error in run: {e}")
        finally:
            # Cleanup
            try:
                # Clean up tick subscription
                if hasattr(self, 'tick_subscription'):
                    self.tick_subscription.unsubscribe()
                
                # Clean up contract subscriptions
                for contract_id, contract_data in list(self.active_contracts.items()):
                    if 'subscription' in contract_data:
                        try:
                            contract_data['subscription'].unsubscribe()
                            print(f"Unsubscribed from contract {contract_id}")
                        except Exception as e:
                            print(f"Error unsubscribing from contract {contract_id}: {e}")
                
                # Disconnect from API
                await self.api.disconnect()
                print("API connection closed and cleaned up")
            except Exception as e:
                print(f"Error in cleanup: {e}")

if __name__ == "__main__":
    # Get API key from environment variable with default empty string
    api_key = os.getenv("DERIV_API_TOKEN", "")
    bot = TradingBot(api_key)
    asyncio.run(bot.run())