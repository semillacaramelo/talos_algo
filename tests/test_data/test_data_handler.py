import pytest
import pandas as pd
import numpy as np
from unittest.mock import AsyncMock, patch, MagicMock
from src.data.data_handler import get_historical_data, subscribe_to_ticks
from datetime import datetime, timedelta

@pytest.mark.unit
class TestDataHandler:
    
    @pytest.mark.asyncio
    async def test_get_historical_data(self, mock_api, sample_ohlc_data):
        """Test fetching historical data."""
        # Setup mock response
        mock_api.ticks_history = AsyncMock(return_value={
            "candles": [
                {
                    "epoch": int(row['time'].timestamp()),
                    "open": row['open'],
                    "high": row['high'],
                    "low": row['low'],
                    "close": row['close']
                }
                for _, row in sample_ohlc_data.head().iterrows()
            ]
        })

        result = await get_historical_data(mock_api, 'R_100', 60, 5)
        assert isinstance(result, pd.DataFrame)
        assert len(result) == 5
        assert all(col in result.columns for col in ['time', 'open', 'high', 'low', 'close'])

    @pytest.mark.asyncio
    async def test_historical_data_error_handling(self, mock_api):
        """Test error handling in historical data fetching."""
        mock_api.ticks_history = AsyncMock(side_effect=Exception("API Error"))
        
        result = await get_historical_data(mock_api, 'R_100', 60, 100)
        assert isinstance(result, pd.DataFrame)
        assert result.empty

    @pytest.mark.asyncio
    async def test_historical_data_empty_response(self, mock_api):
        """Test handling of empty API response."""
        mock_api.ticks_history = AsyncMock(return_value={"candles": []})
        
        result = await get_historical_data(mock_api, 'R_100', 60, 100)
        assert isinstance(result, pd.DataFrame)
        assert result.empty

    @pytest.mark.asyncio
    async def test_subscribe_to_ticks(self, mock_api):
        """Test tick subscription setup."""
        observable = MagicMock()
        mock_api.subscription_manager.subscribe = AsyncMock(return_value=observable)
        
        result = await subscribe_to_ticks(mock_api, 'R_100')
        assert result is not None
        assert 'observable' in result
        assert 'disposable' in result
        mock_api.subscription_manager.subscribe.assert_called_once_with({"ticks": "R_100"})

    @pytest.mark.asyncio
    async def test_tick_subscription_error(self, mock_api):
        """Test error handling in tick subscription."""
        mock_api.subscription_manager.subscribe = AsyncMock(side_effect=Exception("Subscription failed"))
        
        result = await subscribe_to_ticks(mock_api, 'R_100')
        assert result is None

    @pytest.mark.asyncio
    async def test_tick_data_processing(self, mock_api, sample_tick_data):
        """Test tick data processing pipeline."""
        # Setup mock observable
        observable = MagicMock()
        mock_api.subscription_manager.subscribe = AsyncMock(return_value=observable)
        
        # Create a list to capture processed ticks
        processed_ticks = []
        
        # Mock the tick handler
        async def mock_handler(message):
            if 'tick' in message:
                processed_ticks.append(message['tick'])
        
        # Subscribe to ticks with mock handler
        result = await subscribe_to_ticks(mock_api, 'R_100', mock_api, None, None)
        assert result is not None
        
        # Simulate receiving ticks
        for _, row in sample_tick_data.head().iterrows():
            observable.subscribe.call_args[1]['on_next']({
                'tick': {
                    'quote': row['close'],
                    'epoch': int(row['time'].timestamp())
                }
            })
        
        assert len(processed_ticks) == 5

    @pytest.mark.integration
    @pytest.mark.slow
    @pytest.mark.asyncio
    async def test_data_pipeline_integration(self, mock_api, sample_ohlc_data, sample_tick_data):
        """Test complete data pipeline from historical to real-time data."""
        # Setup historical data mock
        mock_api.ticks_history = AsyncMock(return_value={
            "candles": [
                {
                    "epoch": int(row['time'].timestamp()),
                    "open": row['open'],
                    "high": row['high'],
                    "low": row['low'],
                    "close": row['close']
                }
                for _, row in sample_ohlc_data.head().iterrows()
            ]
        })
        
        # Get historical data
        hist_data = await get_historical_data(mock_api, 'R_100', 60, 5)
        assert not hist_data.empty
        
        # Setup tick subscription
        observable = MagicMock()
        mock_api.subscription_manager.subscribe = AsyncMock(return_value=observable)
        
        # Subscribe to ticks
        sub_result = await subscribe_to_ticks(mock_api, 'R_100')
        assert sub_result is not None
        
        # Verify data pipeline
        assert len(hist_data) == 5
        assert all(col in hist_data.columns for col in ['time', 'open', 'high', 'low', 'close'])
        mock_api.subscription_manager.subscribe.assert_called_once()