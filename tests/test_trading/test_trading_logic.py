import pytest
import pandas as pd
import numpy as np
from unittest.mock import AsyncMock, patch, MagicMock
from collections import deque # Import deque
from src.trading.trading_logic import execute_trade, validate_signal, calculate_position_size
# Import necessary components for the integration test
from src.models.signal_model import generate_signal
from datetime import datetime

@pytest.mark.trading
class TestTradingLogic:
    
    @pytest.mark.asyncio
    async def test_signal_validation(self, trading_env):
        """Test trading signal validation logic."""
        # Test valid BUY signal
        is_valid = validate_signal(
            signal="BUY",
            current_price=100.0,
            account_balance=1000.0,
            active_positions=0,
            max_positions=trading_env['max_concurrent_trades']
        )
        assert is_valid is True

        # Test invalid signal due to max positions
        is_valid = validate_signal(
            signal="BUY",
            current_price=100.0,
            account_balance=1000.0,
            active_positions=1,
            max_positions=1
        )
        assert is_valid is False

        # Test invalid signal due to insufficient balance
        is_valid = validate_signal(
            signal="BUY",
            current_price=1500.0,
            account_balance=1000.0,
            active_positions=0,
            max_positions=1
        )
        assert is_valid is False

    def test_position_sizing(self, trading_env):
        """Test position size calculation."""
        # Test normal case
        position_size = calculate_position_size(
            account_balance=1000.0,
            risk_per_trade=trading_env['risk_per_trade'],
            current_price=100.0,
            stop_loss_pct=0.02
        )
        assert position_size > 0
        assert position_size <= 1000.0  # Should not exceed account balance

        # Test with very small account balance
        position_size = calculate_position_size(
            account_balance=10.0,
            risk_per_trade=0.02,
            current_price=100.0,
            stop_loss_pct=0.02
        )
        assert position_size > 0
        assert position_size <= 10.0

        # Test with zero balance (should return 0)
        position_size = calculate_position_size(
            account_balance=0.0,
            risk_per_trade=0.02,
            current_price=100.0,
            stop_loss_pct=0.02
        )
        assert position_size == 0.0

    @pytest.mark.asyncio
    async def test_trade_execution(self, mock_api, trading_env):
        """Test trade execution flow."""
        # Setup mock responses
        mock_api.proposal = AsyncMock(return_value={
            'proposal': {
                'id': 'test_proposal',
                'ask_price': 10.0,
                'payout': 20.0
            }
        })
        
        mock_api.buy = AsyncMock(return_value={
            'buy': {
                'contract_id': 'test_contract',
                'purchase_time': 1234567890,
                'balance_after': 990.0
            }
        })

        result = await execute_trade(
            api=mock_api,
            signal="BUY",
            instrument=trading_env['instrument'],
            stake_amount=trading_env['stake_amount'],
            duration=5,
            duration_unit='m'
        )
        
        assert result is not None
        assert 'contract_id' in result['buy']
        mock_api.proposal.assert_called_once()
        mock_api.buy.assert_called_once()

    @pytest.mark.asyncio
    async def test_trade_execution_error_handling(self, mock_api, trading_env):
        """Test error handling in trade execution."""
        # Test proposal error
        mock_api.proposal = AsyncMock(return_value={
            'error': {
                'code': 'InvalidAmount',
                'message': 'Invalid stake amount'
            }
        })
        
        result = await execute_trade(
            api=mock_api,
            signal="BUY",
            instrument=trading_env['instrument'],
            stake_amount=trading_env['stake_amount'],
            duration=5,
            duration_unit='m'
        )
        
        assert result is None
        
        # Test buy error
        mock_api.proposal = AsyncMock(return_value={
            'proposal': {
                'id': 'test_proposal',
                'ask_price': 10.0,
                'payout': 20.0
            }
        })
        mock_api.buy = AsyncMock(side_effect=Exception("Purchase failed"))
        
        result = await execute_trade(
            api=mock_api,
            signal="BUY",
            instrument=trading_env['instrument'],
            stake_amount=trading_env['stake_amount'],
            duration=5,
            duration_unit='m'
        )
        
        assert result is None

    @pytest.mark.integration
    @pytest.mark.asyncio
    async def test_trading_flow_integration(self, mock_api, mock_model, mock_scaler, sample_tick_data, trading_env): # Added trading_env fixture
        """Test the complete trading flow from signal to execution."""
        # Setup mocks for API calls
        mock_api.proposal = AsyncMock(return_value={"proposal": {"id": "prop123", "ask_price": 10.0}})
        mock_api.buy = AsyncMock(return_value={"buy": {"contract_id": "cont456"}})

        # Setup mock model prediction to ensure a BUY signal
        mock_model.predict.return_value = np.array([1]) # 1 corresponds to BUY

        # Prepare tick data
        recent_ticks = deque(
            [{'time': row['time'], 'close': row['close']}
             for _, row in sample_tick_data.iterrows()],
            maxlen=100
        )

        # Generate signal (should now be BUY due to mock setup)
        signal = generate_signal(mock_model, mock_scaler, recent_ticks)
        assert signal == "BUY" # Verify the signal is BUY as expected
        
        # Validate signal
        is_valid = validate_signal(
            signal=signal,
            current_price=100.0,
            account_balance=1000.0,
            active_positions=0,
            max_positions=trading_env['max_concurrent_trades']
        )
        assert is_valid is True
        
        # Calculate position size
        position_size = calculate_position_size(
            account_balance=1000.0,
            risk_per_trade=trading_env['risk_per_trade'],
            current_price=100.0,
            stop_loss_pct=0.02
        )
        assert position_size > 0
        
        # Execute trade
        mock_api.proposal = AsyncMock(return_value={
            'proposal': {
                'id': 'test_proposal',
                'ask_price': position_size,
                'payout': position_size * 2
            }
        })
        
        mock_api.buy = AsyncMock(return_value={
            'buy': {
                'contract_id': 'test_contract',
                'purchase_time': int(datetime.now().timestamp()),
                'balance_after': 1000.0 - position_size
            }
        })
        
        result = await execute_trade(
            api=mock_api,
            signal=signal,
            instrument=trading_env['instrument'],
            stake_amount=position_size,
            duration=5,
            duration_unit='m'
        )
        
        assert result is not None
        assert result['buy']['contract_id'] == 'test_contract'

    @pytest.mark.performance
    @pytest.mark.asyncio
    async def test_trading_performance(self, mock_api, trading_env, performance_metrics):
        """Test trading system performance under load."""
        import time
        
        # Test rapid trade validation
        start_time = time.time()
        for _ in range(100):
            validate_signal(
                signal="BUY",
                current_price=100.0,
                account_balance=1000.0,
                active_positions=0,
                max_positions=trading_env['max_concurrent_trades']
            )
        validation_time = time.time() - start_time
        performance_metrics.record_latency(validation_time)
        
        # Performance assertions
        assert validation_time < 0.1  # Should validate 100 signals in under 0.1 seconds
        
        # Test position sizing performance
        start_time = time.time()
        for _ in range(100):
            calculate_position_size(
                account_balance=1000.0,
                risk_per_trade=0.02,
                current_price=100.0,
                stop_loss_pct=0.02
            )
        sizing_time = time.time() - start_time
        performance_metrics.record_latency(sizing_time)
        
        # Performance assertions
        assert sizing_time < 0.1  # Should calculate 100 position sizes in under 0.1 seconds
