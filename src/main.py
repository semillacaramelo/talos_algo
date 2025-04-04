import sys
import os
import asyncio
from collections import deque
from datetime import datetime
import pandas as pd
from typing import Dict, Optional

from src.api.deriv_api_handler import DerivAPIAsync
from src.models.signal_model import train_or_load_model, generate_signal
from config.settings import (
    OPTION_DURATION, OPTION_DURATION_UNIT, BASIS, CURRENCY,
    MAX_CONCURRENT_TRADES, DYNAMIC_STAKE_PERCENT, MIN_STAKE_AMOUNT,
    MAX_STAKE_AMOUNT, MAX_DAILY_LOSS
)

class TradingBot:
    def __init__(self, api_key: str):
        self.api = DerivAPIAsync(api_key)
        self.active_contracts: Dict[str, dict] = {}
        self.recent_ticks_deque = deque(maxlen=50)  # Store more points than needed
        self.daily_pnl = 0.0
        self.last_pnl_reset = datetime.now().date()
        self.model = None
        self.scaler = None

    async def initialize(self):
        """Initialize the bot by loading models and connecting to API."""
        self.model, self.scaler = train_or_load_model()
        if not self.model or not self.scaler:
            raise ValueError("Failed to load model or scaler")
        await self.api.connect()

    async def _get_dynamic_stake(self) -> float:
        """Calculate dynamic stake based on account balance."""
        try:
            balance = await self.api.balance()
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
                proposal = await self.api.get_option_proposal(
                    contract_type="CALL",
                    duration=OPTION_DURATION,
                    duration_unit=OPTION_DURATION_UNIT,
                    currency=CURRENCY,
                    amount=stake_amount,
                    basis=BASIS
                )
            else:  # SELL signal
                proposal = await self.api.get_option_proposal(
                    contract_type="PUT",
                    duration=OPTION_DURATION,
                    duration_unit=OPTION_DURATION_UNIT,
                    currency=CURRENCY,
                    amount=stake_amount,
                    basis=BASIS
                )

            if not proposal or 'error' in proposal:
                print(f"Proposal error: {proposal.get('error', {}).get('message', 'Unknown error')}")
                return

            # Buy contract
            buy_response = await self.api.buy_contract(
                proposal_id=proposal['proposal']['id'],
                price=proposal['proposal']['ask_price']
            )

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

            # Subscribe to contract updates
            await self.api.subscribe_to_contract(
                contract_id,
                self.handle_contract_update
            )

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

    async def run(self):
        """Main bot execution loop."""
        try:
            await self.initialize()

            # Subscribe to price feed
            await self.api.subscribe_to_ticks(
                "frxEURUSD",
                self.handle_tick
            )

            # Keep the bot running
            while True:
                await asyncio.sleep(1)

        except Exception as e:
            print(f"Error in run: {e}")
        finally:
            # Cleanup
            for contract_id in list(self.active_contracts.keys()):
                try:
                    await self.api.unsubscribe_from_contract(contract_id)
                except:
                    pass
            await self.api.disconnect()

if __name__ == "__main__":
    bot = TradingBot(os.getenv("DERIV_API_TOKEN"))
    asyncio.run(bot.run())