import pytest
import pandas as pd
import numpy as np
from unittest.mock import patch, MagicMock
from src.models.signal_model import (
    engineer_features, 
    train_or_load_model, 
    generate_signal, 
    generate_signals_for_dataset,
    FEATURE_COLUMNS,
    BUY,
    SELL,
    HOLD
)
from collections import deque

@pytest.mark.model
class TestSignalModel:
    
    def test_feature_engineering(self, sample_ohlc_data):
        """Test feature engineering pipeline."""
        result = engineer_features(sample_ohlc_data.copy())
        
        # Verify all required features are present
        assert all(col in result.columns for col in FEATURE_COLUMNS)
        
        # Verify calculations
        assert 'price_change_1' in result.columns
        assert 'price_change_5' in result.columns
        assert 'ma_diff' in result.columns
        assert 'RSI_14' in result.columns
        assert 'ATRr_14' in result.columns
        
        # Check for NaN values after feature engineering
        assert not result.isnull().any().any()

    @pytest.mark.asyncio
    async def test_model_loading(self):
        """Test model loading functionality."""
        with patch('joblib.load') as mock_load:
            # Mock successful model load
            mock_model = MagicMock()
            mock_scaler = MagicMock()
            mock_load.side_effect = [mock_model, mock_scaler]
            
            model, scaler = await train_or_load_model()
            assert model is not None
            assert scaler is not None

    @pytest.mark.asyncio
    async def test_model_loading_error(self):
        """Test model loading error handling."""
        with patch('joblib.load', side_effect=FileNotFoundError):
            model, scaler = await train_or_load_model()
            assert model is None
            assert scaler is None

    def test_signal_generation(self, mock_model, mock_scaler, sample_tick_data):
        """Test signal generation from tick data."""
        # Create deque of recent ticks
        recent_ticks = deque(
            [{'time': row['time'], 'close': row['close']} 
             for _, row in sample_tick_data.iterrows()],
            maxlen=100
        )
        
        # Set up mock prediction
        mock_model.predict.return_value = np.array([1])  # Predict BUY
        
        signal = generate_signal(mock_model, mock_scaler, recent_ticks)
        assert signal in [BUY, SELL, HOLD]
        
        # Verify feature scaling was applied
        mock_scaler.transform.assert_called_once()
        
        # Verify prediction was made
        mock_model.predict.assert_called_once()

    def test_signal_generation_insufficient_data(self, mock_model, mock_scaler):
        """Test signal generation with insufficient data."""
        recent_ticks = deque([{'time': pd.Timestamp.now(), 'close': 100.0}], maxlen=100)
        
        signal = generate_signal(mock_model, mock_scaler, recent_ticks)
        assert signal == HOLD
        
        # Verify no prediction was attempted
        mock_model.predict.assert_not_called()

    def test_signal_generation_error_handling(self, mock_model, mock_scaler, sample_tick_data):
        """Test error handling in signal generation."""
        recent_ticks = deque(
            [{'time': row['time'], 'close': row['close']} 
             for _, row in sample_tick_data.iterrows()],
            maxlen=100
        )
        
        # Simulate error in prediction
        mock_model.predict.side_effect = Exception("Prediction error")
        
        signal = generate_signal(mock_model, mock_scaler, recent_ticks)
        assert signal == HOLD

    def test_dataset_signal_generation(self, mock_model, mock_scaler, sample_ohlc_data):
        """Test signal generation for entire dataset."""
        # Setup mock predictions
        mock_model.predict.return_value = np.array([1, -1, 0] * (len(sample_ohlc_data) // 3 + 1))[:len(sample_ohlc_data)]
        
        signals = generate_signals_for_dataset(mock_model, mock_scaler, sample_ohlc_data)
        assert len(signals) == len(sample_ohlc_data)
        assert all(s in [1, -1] for s in signals)

    @pytest.mark.performance
    def test_feature_engineering_performance(self, sample_ohlc_data, performance_metrics):
        """Test performance of feature engineering pipeline."""
        import time
        
        # Measure execution time
        start_time = time.time()
        result = engineer_features(sample_ohlc_data.copy())
        execution_time = time.time() - start_time
        
        performance_metrics.record_latency(execution_time)
        
        # Performance assertions
        assert execution_time < 1.0  # Should complete within 1 second
        assert len(result) > 0

    @pytest.mark.integration
    def test_model_pipeline_integration(self, mock_model, mock_scaler, sample_ohlc_data):
        """Test complete model pipeline from features to signals."""
        # Engineer features
        feature_df = engineer_features(sample_ohlc_data.copy())
        assert not feature_df.empty
        
        # Generate signals
        signals = generate_signals_for_dataset(mock_model, mock_scaler, feature_df)
        assert len(signals) == len(feature_df)
        
        # Verify signal distribution
        unique_signals = np.unique(signals)
        assert all(s in [1, -1] for s in unique_signals)
        
        # Check feature importance (if model supports it)
        if hasattr(mock_model, 'feature_importances_'):
            importances = mock_model.feature_importances_
            assert len(importances) == len(FEATURE_COLUMNS)