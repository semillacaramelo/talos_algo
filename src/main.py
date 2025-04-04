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

class TradingBot:
    def __init__(self):
        self.logger = setup_logger()
        self.is_running = False
        self.api = None
        self.model = None
        self.scaler = None
        self.active_contracts = {}
        self.recent_ticks_deque = deque(maxlen=MIN_FEATURE_POINTS + 10)
        self.subscription_data = None

    async def start(self):
        """Start the trading bot and its main loop."""
        if self.is_running:
            self.logger.warning("Bot is already running")
            return False

        try:
            # Connect to API
            self.api = await connect_deriv_api()
            if not self.api:
                self.logger.error("Connection failed")
                return False
            self.logger.info("Connection successful")

            # Get historical data
            historical_df = await get_historical_data(self.api, INSTRUMENT, TIMEFRAME_SECONDS, HISTORICAL_BARS_COUNT)
            if historical_df.empty:
                self.logger.warning("Historical data is empty")

            # Initialize model
            self.model, self.scaler = train_or_load_model()
            if self.model is None:
                self.logger.critical("Failed to load ML model")
                return False

            # Subscribe to tick stream
            self.subscription_data = await subscribe_to_ticks(
                self.api, 
                INSTRUMENT, 
                api_ref=self.api, 
                model_ref=self.model, 
                scaler_ref=self.scaler,
                tick_handler=self.handle_tick,
                contract_update_handler=self.handle_contract_update
            )

            if not self.subscription_data:
                self.logger.error(f"Failed to initiate subscription for {INSTRUMENT}")
                return False

            self.is_running = True
            self.logger.info("Bot started successfully")
            return True

        except Exception as e:
            self.logger.exception("Error during bot startup")
            await self.stop()
            return False

    async def stop(self):
        """Stop the trading bot and cleanup resources."""
        try:
            self.is_running = False

            # Clean up tick subscription
            if self.subscription_data and 'disposable' in self.subscription_data:
                try:
                    self.logger.info("Disposing tick subscription...")
                    self.subscription_data['disposable'].dispose()
                    await asyncio.sleep(0.2)
                    self.logger.info("Tick subscription disposed")
                except Exception as e:
                    self.logger.exception("Error disposing tick subscription")

            # Clean up contract subscriptions
            if self.active_contracts:
                try:
                    self.logger.info(f"Disposing {len(self.active_contracts)} active contract subscriptions...")
                    for contract_id, contract_data in list(self.active_contracts.items()):
                        try:
                            contract_data['disposable'].dispose()
                            self.logger.info(f"Disposed subscription for contract {contract_id}")
                        except Exception as e:
                            self.logger.error(f"Error disposing subscription for contract {contract_id}: {e}")
                    self.active_contracts = {} #clear the dictionary
                except Exception as e:
                    self.logger.exception("Error during contract subscriptions cleanup")

            # Disconnect API
            if self.api:
                await asyncio.sleep(0.5)
                await disconnect(self.api)
                await asyncio.sleep(0.5)
                self.api = None

            self.logger.info("Bot stopped successfully")
            return True

        except Exception as e:
            self.logger.exception("Error during bot shutdown")
            return False

    def get_status(self):
        """Get the current status of the bot."""
        return {
            "is_running": self.is_running,
            "active_contracts": len(self.active_contracts),
            "recent_ticks": len(self.recent_ticks_deque)
        }

    async def handle_tick(self, tick_data_msg):
        """Handle incoming tick data."""
        if not self.is_running:
            return

        if not isinstance(tick_data_msg, dict) or 'tick' not in tick_data_msg:
            return

        current_tick = tick_data_msg['tick']
        self.logger.info(f"Processing tick in handler: {current_tick}")
        current_price = current_tick.get('quote')
        current_time = current_tick.get('epoch')

        if current_price and current_time:
            self.recent_ticks_deque.append({
                'time': pd.to_datetime(current_time, unit='s'),
                'close': current_price
            })

        if len(self.recent_ticks_deque) >= MIN_FEATURE_POINTS:
            signal = generate_signal(self.model, self.scaler, self.recent_ticks_deque)

            if signal != HOLD:
                self.logger.info(f"Generated ML Signal: {signal}")

            can_trade = len(self.active_contracts) < MAX_CONCURRENT_TRADES

            if can_trade and current_price and signal in (BUY, SELL):
                await self._execute_trade(signal, current_price)

    async def handle_contract_update(self, message):
        """Handle contract updates."""
        if not self.is_running:
            return

        try:
            if 'proposal_open_contract' not in message:
                self.logger.warning("Received contract update with missing proposal_open_contract key")
                return

            contract = message['proposal_open_contract']
            contract_id = contract['contract_id']
            is_sold = contract.get('is_sold', 0)

            self.logger.debug(f"Contract update received for ID: {contract_id}")

            if is_sold == 1:
                profit = contract.get('profit', 0)
                self.logger.info(f"Contract {contract_id} is now finished. Profit/Loss: {profit}")

                if contract_id in self.active_contracts:
                    try:
                        self.active_contracts[contract_id]['disposable'].dispose()
                        self.logger.info(f"Disposed subscription for contract {contract_id}")
                    except Exception as e:
                        self.logger.error(f"Error disposing subscription for contract {contract_id}: {e}")

                    self.active_contracts.pop(contract_id)
                    self.logger.info(f"Removed contract {contract_id} from active_contracts. Active contracts remaining: {len(self.active_contracts)}")

        except Exception as e:
            self.logger.exception("Error processing contract update")

    async def _execute_trade(self, signal, current_price):
        """Execute a trade based on the signal."""
        try:
            if signal == BUY:
                # CALL option - prediction that price will RISE
                self.logger.info(f"BUY signal received. Requesting RISE (CALL) option proposal...")
                proposal_response = await get_option_proposal(
                    self.api, INSTRUMENT, "CALL", OPTION_DURATION, OPTION_DURATION_UNIT, 
                    CURRENCY, STAKE_AMOUNT, BASIS
                )
                
                if proposal_response and proposal_response.get('proposal'):
                    proposal = proposal_response.get('proposal')
                    proposal_id = proposal.get('id')
                    ask_price = proposal.get('ask_price')
                    
                    self.logger.info(f"Buying RISE (CALL) option contract with proposal ID: {proposal_id}")
                    buy_confirmation = await buy_option_contract(self.api, proposal_id, ask_price)
                    
                    if buy_confirmation and buy_confirmation.get('buy'):
                        contract_info = buy_confirmation.get('buy')
                        contract_id = contract_info.get('contract_id')
                        self.logger.info(f"Successfully purchased RISE contract ID: {contract_id}")
                        
                        # Subscribe to contract updates
                        contract_subscription_disposable = await subscribe_to_contract_updates(
                            self.api, contract_id, self.handle_contract_update
                        )
                        
                        # Store the contract with its subscription
                        if contract_subscription_disposable:
                            self.active_contracts[contract_id] = {
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
                            self.logger.info(f"Stored active contract {contract_id} with its subscription.")
                        else:
                            self.logger.error(f"Failed to subscribe to updates for contract {contract_id}")
            elif signal == SELL:
                # PUT option - prediction that price will FALL
                self.logger.info(f"SELL signal received. Requesting FALL (PUT) option proposal...")
                proposal_response = await get_option_proposal(
                    self.api, INSTRUMENT, "PUT", OPTION_DURATION, OPTION_DURATION_UNIT, 
                    CURRENCY, STAKE_AMOUNT, BASIS
                )
                
                if proposal_response and proposal_response.get('proposal'):
                    proposal = proposal_response.get('proposal')
                    proposal_id = proposal.get('id')
                    ask_price = proposal.get('ask_price')
                    
                    self.logger.info(f"Buying FALL (PUT) option contract with proposal ID: {proposal_id}")
                    buy_confirmation = await buy_option_contract(self.api, proposal_id, ask_price)
                    
                    if buy_confirmation and buy_confirmation.get('buy'):
                        contract_info = buy_confirmation.get('buy')
                        contract_id = contract_info.get('contract_id')
                        self.logger.info(f"Successfully purchased FALL contract ID: {contract_id}")
                        
                        # Subscribe to contract updates
                        contract_subscription_disposable = await subscribe_to_contract_updates(
                            self.api, contract_id, self.handle_contract_update
                        )
                        
                        # Store the contract with its subscription
                        if contract_subscription_disposable:
                            self.active_contracts[contract_id] = {
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
                            self.logger.info(f"Stored active contract {contract_id} with its subscription.")
                        else:
                            self.logger.error(f"Failed to subscribe to updates for contract {contract_id}")
        except Exception as e:
            self.logger.exception(f"Error in Digital Options trading execution")


if __name__ == "__main__":
    # Create bot instance but don't start it
    bot = TradingBot()

    # This can be used for direct testing, but we'll let the web interface control the bot
    # asyncio.run(bot.start())