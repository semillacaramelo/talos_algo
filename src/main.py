import sys
import os

# Fix import path by adding project root directory to Python path
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

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

# Adding a main function that can be imported from talos_algo.py
async def main_async():
    """Main async entry point for the trading bot."""
    # Get API key from environment variable with default empty string
    api_key = os.getenv("DERIV_API_TOKEN", "")
    bot = TradingBot(api_key)
    await bot.run()

def main():
    """Main synchronous entry point that runs the async main function."""
    asyncio.run(main_async())

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
        self.is_running = False  # Explicitly initialize to False
        
        # Enhanced logging attributes
        self.last_signal = "N/A"
        self.last_tick_price = None
        self.last_feature_count = None
        self.last_trade_time = None
        self.start_time = None
        self.processed_ticks_count = 0
        self.feature_calculation_success = False
        self.signal_calculation_success = False
        
        # Additional tracking attributes for UI
        self.feature_data_count = 0
        self.win_count = 0
        self.loss_count = 0
        self.model_status = "Not Loaded"
        
        # Add a lock for thread-safe state checking
        import threading
        self._state_lock = threading.Lock()
        
    # Getter and setter for is_running with thread safety
    def get_running_status(self):
        with self._state_lock:
            return self.is_running
            
    def set_running_status(self, status: bool):
        with self._state_lock:
            self.is_running = status

    async def initialize(self):
        """Initialize the bot by loading models and connecting to API."""
        try:
            print("Loading ML model and scaler...")
            self.model_status = "Loading..."
            self.model, self.scaler = train_or_load_model()
            if not self.model or not self.scaler:
                # Try to create a dummy model as fallback
                from src.models.dummy_model import create_dummy_model
                print("Loading from file failed, creating dummy model...")
                self.model_status = "Creating Dummy Model..."
                self.model, self.scaler = create_dummy_model()
                if not self.model or not self.scaler:
                    self.model_status = "Failed to Load"
                    raise ValueError("Failed to load model or create dummy model")
            print("Model and scaler successfully loaded or created")
            self.model_status = "Loaded"
            await self.api.connect()
        except Exception as e:
            print(f"Initialization error: {e}")
            self.model_status = "Error: " + str(e)
            raise ValueError(f"Failed to initialize: {e}")

    async def _get_dynamic_stake(self) -> float:
        """Calculate dynamic stake based on account balance."""
        try:
            # Import the config settings at the top to avoid undefined variables
            from config.settings import STAKE_AMOUNT, MIN_STAKE_AMOUNT, MAX_STAKE_AMOUNT, DYNAMIC_STAKE_PERCENT
            
            # Use the configured STAKE_AMOUNT instead of calculating dynamically
            # This ensures what's displayed in the UI matches what's actually used
            print(f"Using configured stake amount: {STAKE_AMOUNT}")
            return STAKE_AMOUNT
            
            # The following code is commented out to use fixed STAKE_AMOUNT
            # Access the underlying DerivAPI object
            #api = self.api.api
            #if not api:
            #    print("API not initialized, using minimum stake")
            #    return MIN_STAKE_AMOUNT
                
            # Get balance using the official API
            #balance = await api.balance()
            
            # Parse the balance response
            #if 'error' in balance:
            #    print(f"Failed to get balance: {balance['error'].get('message', 'Unknown error')}")
            #    return MIN_STAKE_AMOUNT
                
            # Extract the balance value
            #account_balance = float(balance['balance']['balance'])
            #stake = account_balance * DYNAMIC_STAKE_PERCENT
            #return max(min(stake, MAX_STAKE_AMOUNT), MIN_STAKE_AMOUNT)
        except Exception as e:
            print(f"Error calculating stake: {e}")
            # Import here too for error handling case
            from config.settings import STAKE_AMOUNT
            return STAKE_AMOUNT  # Return configured amount even on error

    async def _check_trading_limits(self) -> bool:
        """Check if trading should proceed based on risk limits."""
        # Import at the beginning to avoid undefined variables
        from config.settings import MAX_DAILY_LOSS, MAX_CONCURRENT_TRADES
        
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
            tick_price = float(tick_data['tick']['quote'])
            self.last_tick_price = tick_price
            self.processed_ticks_count += 1
            
            self.recent_ticks_deque.append({
                'timestamp': tick_data['tick']['epoch'],
                'close': tick_price,
                'high': tick_price,
                'low': tick_price,
                'open': tick_price
            })
            
            # Update feature data count for UI
            self.feature_data_count = len(self.recent_ticks_deque)

            # Check if we have enough data and can trade
            if not await self._check_trading_limits():
                return

            # Log the tick data for debugging
            print(f"Received tick: {tick_data['tick']['symbol']} = {tick_price}")
            
            # Convert deque to DataFrame for analysis
            df = pd.DataFrame(list(self.recent_ticks_deque))
            
            # Track feature engineering metrics before signal generation
            try:
                from src.models.signal_model import engineer_features
                feature_df = engineer_features(df.copy())
                if not feature_df.empty:
                    # Count the actual features created
                    self.feature_calculation_success = True
                    self.last_feature_count = len(feature_df.columns)
                else:
                    self.feature_calculation_success = False
            except Exception as e:
                print(f"Error tracking features: {e}")
                self.feature_calculation_success = False

            # Generate trading signal
            signal = generate_signal(self.model, self.scaler, df)
            self.last_signal = signal
            self.signal_calculation_success = (signal is not None)
            
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
                
                # Update win/loss counters based on profit result
                if profit > 0:
                    self.win_count += 1
                else:
                    self.loss_count += 1
                
                # Update last trade time for UI display
                self.last_trade_time = datetime.now()

                print(f"Contract {contract_id} finished. Profit: ${profit:.2f}, Daily P&L: ${self.daily_pnl:.2f}")
                print(f"Updated stats - Wins: {self.win_count}, Losses: {self.loss_count}")
                
                # Log more detailed trade info
                contract_type = update_data['proposal_open_contract']['contract_type']
                entry_tick = update_data['proposal_open_contract'].get('entry_tick', 'N/A')
                exit_tick = update_data['proposal_open_contract'].get('exit_tick', 'N/A')
                entry_time = update_data['proposal_open_contract'].get('date_start', 'N/A')
                exit_time = update_data['proposal_open_contract'].get('sell_time', 'N/A')
                
                print(f"Trade details - Type: {contract_type}, Entry: {entry_tick}, Exit: {exit_tick}")
                print(f"Trade timing - Entry: {entry_time}, Exit: {exit_time}")

                if contract_id in self.active_contracts:
                    del self.active_contracts[contract_id]

        except Exception as e:
            print(f"Error in handle_contract_update: {e}")

    async def update_config(self, config_data):
        """Update bot configuration during runtime."""
        print(f"Updating bot configuration with: {config_data}")
        
        # Import settings to reference current values
        from config.settings import (
            INSTRUMENT, OPTION_DURATION, OPTION_DURATION_UNIT, 
            STAKE_AMOUNT, CURRENCY, MAX_CONCURRENT_TRADES
        )
        
        # Track which settings got updated
        updated = []
        
        # Update instrument if provided (requires restart for tick subscription)
        if 'instrument' in config_data and config_data['instrument']:
            print(f"Note: Changing instrument from {INSTRUMENT} to {config_data['instrument']} requires bot restart")
            updated.append('instrument')
            
        # Update stake amount if provided
        if 'stake' in config_data and config_data['stake'] is not None:
            try:
                new_stake = float(config_data['stake'])
                if new_stake > 0:
                    print(f"Updated stake amount from {STAKE_AMOUNT} to {new_stake}")
                    updated.append('stake')
            except (ValueError, TypeError) as e:
                print(f"Invalid stake value: {config_data['stake']} - {e}")
        
        # Update duration if provided
        if 'duration' in config_data and config_data['duration'] is not None:
            try:
                new_duration = int(config_data['duration'])
                print(f"Updated option duration from {OPTION_DURATION} to {new_duration}")
                updated.append('duration')
            except (ValueError, TypeError) as e:
                print(f"Invalid duration value: {config_data['duration']} - {e}")
                
        # Update duration unit if provided
        if 'duration_unit' in config_data and config_data['duration_unit']:
            valid_units = ['t', 's', 'm', 'h', 'd']
            if config_data['duration_unit'] in valid_units:
                print(f"Updated duration unit from {OPTION_DURATION_UNIT} to {config_data['duration_unit']}")
                updated.append('duration_unit')
            else:
                print(f"Invalid duration unit: {config_data['duration_unit']}")
        
        return updated

    def get_status(self):
        """Get the current status of the trading bot."""
        return {
            'is_running': self.get_running_status(),
            'active_contracts': len(self.active_contracts)
        }
        
    async def start(self):
        """Start the trading bot."""
        if self.get_running_status():
            return False
        
        # Record the start time for uptime tracking
        self.start_time = datetime.now()
        self.set_running_status(True)
        self.processed_ticks_count = 0
        self.last_signal = None
        self.last_tick_price = None
        self.last_feature_count = None
        
        # Start the bot in a separate task
        asyncio.create_task(self.run())
        return True
        
    async def stop(self):
        """Stop the trading bot."""
        print("Stopping the trading bot...")
        self.set_running_status(False)
        
        # Clean up the resources immediately rather than waiting
        try:
            # Clean up tick subscription - official Deriv API uses .dispose() not .unsubscribe()
            if hasattr(self, 'tick_subscription'):
                try:
                    # First try the dispose method (official Deriv API)
                    if hasattr(self.tick_subscription, 'dispose'):
                        self.tick_subscription.dispose()
                    # Fallback to unsubscribe (custom implementation)
                    elif hasattr(self.tick_subscription, 'unsubscribe'):
                        self.tick_subscription.unsubscribe()
                    print("Unsubscribed from tick feed")
                except Exception as e:
                    print(f"Error unsubscribing from tick feed: {e}")
            
            # Clean up contract subscriptions
            for contract_id, contract_data in list(self.active_contracts.items()):
                if 'subscription' in contract_data:
                    try:
                        # First try the dispose method (official Deriv API)
                        if hasattr(contract_data['subscription'], 'dispose'):
                            contract_data['subscription'].dispose()
                        # Fallback to unsubscribe (custom implementation)
                        elif hasattr(contract_data['subscription'], 'unsubscribe'):
                            contract_data['subscription'].unsubscribe()
                        print(f"Unsubscribed from contract {contract_id}")
                    except Exception as e:
                        print(f"Error unsubscribing from contract {contract_id}: {e}")
            
            # Disconnect from API
            if hasattr(self, 'api') and self.api:
                await self.api.disconnect()
                print("API connection closed and cleaned up")
                
            # Wait a short time to ensure cleanup completes
            await asyncio.sleep(0.2)
        except Exception as e:
            print(f"Error in cleanup during stop: {e}")
            
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
            while self.get_running_status():
                await asyncio.sleep(1)

        except Exception as e:
            print(f"Error in run: {e}")
        finally:
            # Cleanup
            try:
                # Clean up tick subscription
                if hasattr(self, 'tick_subscription'):
                    try:
                        # First try the dispose method (official Deriv API)
                        if hasattr(self.tick_subscription, 'dispose'):
                            self.tick_subscription.dispose()
                        # Fallback to unsubscribe (custom implementation)
                        elif hasattr(self.tick_subscription, 'unsubscribe'):
                            self.tick_subscription.unsubscribe()
                        print("Unsubscribed from tick feed")
                    except Exception as e:
                        print(f"Error unsubscribing from tick feed: {e}")
                
                # Clean up contract subscriptions
                for contract_id, contract_data in list(self.active_contracts.items()):
                    if 'subscription' in contract_data:
                        try:
                            # First try the dispose method (official Deriv API)
                            if hasattr(contract_data['subscription'], 'dispose'):
                                contract_data['subscription'].dispose()
                            # Fallback to unsubscribe (custom implementation)
                            elif hasattr(contract_data['subscription'], 'unsubscribe'):
                                contract_data['subscription'].unsubscribe()
                            print(f"Unsubscribed from contract {contract_id}")
                        except Exception as e:
                            print(f"Error unsubscribing from contract {contract_id}: {e}")
                
                # Disconnect from API
                if hasattr(self, 'api') and self.api:
                    await self.api.disconnect()
                    print("API connection closed and cleaned up")
                    
                # Wait a short time to ensure cleanup completes
                await asyncio.sleep(0.2)
            except Exception as e:
                print(f"Error in cleanup: {e}")

if __name__ == "__main__":
    main()