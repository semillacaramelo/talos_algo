import pytest
import pandas as pd
import numpy as np
from src.utils.backtest import SimpleBacktester

@pytest.mark.unit
class TestBacktester:

    def test_backtester_initialization(self):
        """Test backtester initialization with different parameters."""
        # Test default initialization
        backtester = SimpleBacktester()
        assert backtester.initial_capital == 1000.0

        # Test custom initial capital
        backtester = SimpleBacktester(initial_capital=5000.0)
        assert backtester.initial_capital == 5000.0

    def test_sma_strategy_backtest(self, sample_ohlc_data):
        """Test SMA crossover strategy backtesting."""
        backtester = SimpleBacktester(initial_capital=1000.0)
        
        results = backtester.run_backtest(
            historical_df=sample_ohlc_data,
            short_period=5,
            long_period=20,
            risk_per_trade=0.02,
            stop_loss_pct=0.01,
            take_profit_pct=0.02
        )
        
        assert results is not None
        assert 'metrics' in results
        assert 'trades' in results
        assert 'equity_curve' in results
        
        # Verify metrics
        metrics = results['metrics']
        assert 'initial_capital' in metrics
        assert 'final_capital' in metrics
        assert 'total_return_pct' in metrics
        assert 'total_trades' in metrics
        
        # Verify trades dataframe
        trades_df = results['trades']
        if not trades_df.empty:
            required_columns = ['entry_time', 'exit_time', 'entry_price', 'exit_price', 
                              'position', 'exit_type', 'pnl', 'pnl_pct']
            assert all(col in trades_df.columns for col in required_columns)

        # Verify equity curve
        equity_curve = results['equity_curve']
        assert 'time' in equity_curve.columns
        assert 'capital' in equity_curve.columns
        assert len(equity_curve) > 0

    def test_ml_strategy_backtest(self, sample_ohlc_data, mock_model, mock_scaler):
        """Test ML-based strategy backtesting."""
        backtester = SimpleBacktester(initial_capital=1000.0)
        
        # Generate mock signals
        mock_signals = pd.Series(
            np.random.choice([1, -1], size=len(sample_ohlc_data)),
            index=sample_ohlc_data.index
        )
        
        results = backtester.run_backtest(
            historical_df=sample_ohlc_data,
            signals=mock_signals,
            risk_per_trade=0.02,
            stop_loss_pct=0.01,
            take_profit_pct=0.02
        )
        
        assert results is not None
        assert 'metrics' in results
        assert results['metrics']['total_trades'] > 0

    def test_risk_management(self, sample_ohlc_data):
        """Test risk management rules in backtesting."""
        backtester = SimpleBacktester(initial_capital=1000.0)
        
        # Test with tight stop loss
        results_tight = backtester.run_backtest(
            historical_df=sample_ohlc_data,
            short_period=5,
            long_period=20,
            risk_per_trade=0.01,  # 1% risk
            stop_loss_pct=0.005,  # 0.5% stop loss
            take_profit_pct=0.02
        )
        
        # Test with loose stop loss
        results_loose = backtester.run_backtest(
            historical_df=sample_ohlc_data,
            short_period=5,
            long_period=20,
            risk_per_trade=0.01,
            stop_loss_pct=0.02,  # 2% stop loss
            take_profit_pct=0.02
        )
        
        # Verify risk management impact
        assert results_tight['metrics']['avg_loss'] <= abs(0.005 * 1000.0)  # Max loss should be stop loss
        assert results_loose['metrics']['avg_loss'] <= abs(0.02 * 1000.0)

    def test_position_sizing(self, sample_ohlc_data):
        """Test position sizing in backtesting."""
        backtester = SimpleBacktester(initial_capital=1000.0)
        
        # Test with different position size limits
        results_small = backtester.run_backtest(
            historical_df=sample_ohlc_data,
            short_period=5,
            long_period=20,
            risk_per_trade=0.01,
            stop_loss_pct=0.01,
            take_profit_pct=0.02,
            max_position_size=0.1  # 10% max position
        )
        
        results_large = backtester.run_backtest(
            historical_df=sample_ohlc_data,
            short_period=5,
            long_period=20,
            risk_per_trade=0.01,
            stop_loss_pct=0.01,
            take_profit_pct=0.02,
            max_position_size=0.5  # 50% max position
        )
        
        # Verify position sizing constraints
        if len(results_small['trades']) > 0:
            max_position_small = results_small['trades']['shares'].max() * \
                               results_small['trades']['entry_price'].max()
            assert max_position_small <= 1000.0 * 0.1
        
        if len(results_large['trades']) > 0:
            max_position_large = results_large['trades']['shares'].max() * \
                               results_large['trades']['entry_price'].max()
            assert max_position_large <= 1000.0 * 0.5

    @pytest.mark.performance
    def test_backtest_performance(self, sample_ohlc_data, performance_metrics):
        """Test backtesting system performance."""
        import time
        
        backtester = SimpleBacktester(initial_capital=1000.0)
        
        # Test backtest execution time
        start_time = time.time()
        results = backtester.run_backtest(
            historical_df=sample_ohlc_data,
            short_period=5,
            long_period=20,
            risk_per_trade=0.02,
            stop_loss_pct=0.01,
            take_profit_pct=0.02
        )
        execution_time = time.time() - start_time
        
        performance_metrics.record_latency(execution_time)
        
        # Performance assertions
        assert execution_time < 1.0  # Should complete within 1 second
        assert results is not None

    @pytest.mark.integration
    def test_backtest_with_ml_pipeline(self, sample_ohlc_data, mock_model, mock_scaler):
        """Test integration of ML pipeline with backtesting."""
        from src.models.signal_model import generate_signals_for_dataset
        
        # Generate signals using ML model
        signals = generate_signals_for_dataset(mock_model, mock_scaler, sample_ohlc_data)
        
        # Run backtest with ML signals
        backtester = SimpleBacktester(initial_capital=1000.0)
        results = backtester.run_backtest(
            historical_df=sample_ohlc_data,
            signals=signals,
            risk_per_trade=0.02,
            stop_loss_pct=0.01,
            take_profit_pct=0.02
        )
        
        assert results is not None
        assert 'metrics' in results
        assert results['metrics']['total_trades'] > 0
        
        # Verify ML signal impact
        if len(results['trades']) > 0:
            trades_df = results['trades']
            win_rate = len(trades_df[trades_df['pnl'] > 0]) / len(trades_df)
            assert 0 <= win_rate <= 1  # Sanity check on win rate