import pytest
import pandas as pd
import numpy as np
from unittest.mock import AsyncMock, MagicMock
import asyncio
from datetime import datetime, timedelta

# Mock API fixtures
@pytest.fixture
def mock_api():
    """Create a mock Deriv API client with common methods."""
    mock = AsyncMock()
    # Add common API method mocks
    mock.authorize = AsyncMock(return_value={"authorize": {"email": "test@example.com"}})
    mock.disconnect = AsyncMock(return_value=True)
    mock.subscription_manager = MagicMock()
    # Explicitly define is_connected as a synchronous mock method returning True
    mock.is_connected = MagicMock(return_value=True)
    return mock

@pytest.fixture
def mock_websocket():
    """Create a mock WebSocket connection."""
    mock = AsyncMock()
    mock.send = AsyncMock()
    mock.recv = AsyncMock()
    mock.close = AsyncMock()
    return mock

# Data fixtures
@pytest.fixture
def sample_tick_data():
    """Generate sample tick data for testing."""
    current_time = datetime.now()
    data = []
    for i in range(100):
        tick_time = current_time + timedelta(seconds=i)
        data.append({
            'time': tick_time,
            'close': 100 + np.sin(i/10) * 5,  # Generate sine wave pattern
            'volume': abs(np.random.normal(1000, 100))
        })
    return pd.DataFrame(data)

@pytest.fixture
def sample_ohlc_data():
    """Generate sample OHLC data for testing."""
    current_time = datetime.now()
    data = []
    base_price = 100
    for i in range(100):
        candle_time = current_time + timedelta(minutes=i)
        high = base_price + abs(np.random.normal(0, 1))
        low = base_price - abs(np.random.normal(0, 1))
        data.append({
            'time': candle_time,
            'open': base_price,
            'high': high,
            'low': low,
            'close': np.random.uniform(low, high),
            'volume': abs(np.random.normal(1000, 100))
        })
        base_price = data[-1]['close']
    return pd.DataFrame(data)

@pytest.fixture
def mock_model():
    """Create a mock ML model with predict method."""
    mock = MagicMock()
    mock.predict = MagicMock(return_value=np.array([1, -1, 0]))  # Sample predictions
    return mock

@pytest.fixture
def mock_scaler():
    """Create a mock scaler with transform method."""
    mock = MagicMock()
    mock.transform = MagicMock(return_value=np.array([[0.1, 0.2, 0.3]]))
    return mock

# Trading environment fixtures
@pytest.fixture
def trading_env():
    """Set up a mock trading environment with configuration."""
    return {
        'instrument': 'R_100',
        'timeframe': 60,
        'stake_amount': 1.0,
        'currency': 'USD',
        'risk_per_trade': 0.02,
        'max_concurrent_trades': 1
    }

# Performance testing fixtures
@pytest.fixture
def performance_metrics():
    """Initialize performance metrics collector."""
    class MetricsCollector:
        def __init__(self):
            self.latencies = []
            self.memory_usage = []
            self.cpu_usage = []
        
        def record_latency(self, latency):
            self.latencies.append(latency)
        
        def record_memory(self, memory):
            self.memory_usage.append(memory)
        
        def record_cpu(self, cpu):
            self.cpu_usage.append(cpu)
        
        def get_stats(self):
            return {
                'avg_latency': np.mean(self.latencies) if self.latencies else 0,
                'max_memory': max(self.memory_usage) if self.memory_usage else 0,
                'avg_cpu': np.mean(self.cpu_usage) if self.cpu_usage else 0
            }
    
    return MetricsCollector()
