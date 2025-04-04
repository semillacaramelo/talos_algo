import os
import pandas as pd
from joblib import load
from typing import Tuple, Optional, List, Union
import numpy as np

# Features used by the model
FEATURE_COLUMNS = [
    'price_change', 'ma_diff', 'rsi', 'atr', 
    'stoch_k', 'stoch_d', 'macd', 'macd_signal'
]

def train_or_load_model(model_path: str = "", 
                       scaler_path: str = "") -> Tuple[Optional[object], Optional[object]]:
    """Load the trained model and scaler."""
    # Use relative paths based on the current file location if none provided
    if not model_path:
        model_path = os.path.join(os.path.dirname(__file__), 'basic_predictor.joblib')
    if not scaler_path:
        scaler_path = os.path.join(os.path.dirname(__file__), 'scaler.joblib')
    try:
        model = load(model_path)
        scaler = load(scaler_path)
        return model, scaler
    except Exception as e:
        print(f"Error loading model/scaler: {e}")
        return None, None

def engineer_features(df: pd.DataFrame) -> pd.DataFrame:
    """Calculate technical indicators for feature engineering."""
    try:
        # Basic price changes
        df['price_change'] = df['close'].pct_change()

        # Moving average difference
        df['ma_fast'] = df['close'].rolling(window=5).mean()
        df['ma_slow'] = df['close'].rolling(window=20).mean()
        df['ma_diff'] = (df['ma_fast'] - df['ma_slow']) / df['close']

        # Calculate RSI
        # First calculate price differences
        delta = df['close'].diff()
        # Split gains (up) and losses (down)
        up = delta.clip(lower=0)
        down = -1 * delta.clip(upper=0)
        # Calculate averages
        avg_gain = up.rolling(window=14).mean()
        avg_loss = down.rolling(window=14).mean()
        # Calculate RS and RSI
        rs = avg_gain / avg_loss
        df['rsi'] = 100 - (100 / (1 + rs))

        # Calculate ATR (Simplified version)
        high_low = df['high'] - df['low']
        high_close = abs(df['high'] - df['close'].shift())
        low_close = abs(df['low'] - df['close'].shift())
        ranges = pd.concat([high_low, high_close, low_close], axis=1)
        true_range = ranges.max(axis=1)
        df['atr'] = true_range.rolling(14).mean() / df['close']

        # Calculate Stochastic (Simplified version)
        low_min = df['low'].rolling(window=14).min()
        high_max = df['high'].rolling(window=14).max()
        df['stoch_k'] = 100 * ((df['close'] - low_min) / (high_max - low_min))
        df['stoch_d'] = df['stoch_k'].rolling(window=3).mean()

        # Calculate MACD (Moving Average Convergence Divergence)
        exp1 = df['close'].ewm(span=12, adjust=False).mean()
        exp2 = df['close'].ewm(span=26, adjust=False).mean()
        df['macd'] = exp1 - exp2
        df['macd_signal'] = df['macd'].ewm(span=9, adjust=False).mean()

        # Drop rows with NaN values after calculations
        df = df.dropna()

        return df
    except Exception as e:
        print(f"Error engineering features: {e}")
        return pd.DataFrame()

def generate_signal(model, scaler, recent_data: pd.DataFrame) -> Optional[str]:
    """Generate trading signals using the ML model."""
    try:
        if len(recent_data) < 30:  # Minimum required points for feature calculation
            return None

        # Engineer features
        df = engineer_features(recent_data.copy())
        if df.empty:
            return None

        # Extract features for prediction
        features = df[FEATURE_COLUMNS].iloc[-1:].values

        # Scale features
        if scaler:
            features = scaler.transform(features)

        # Make prediction
        prediction = model.predict(features)[0]

        # Map prediction to signal
        return "BUY" if prediction == 1 else "SELL"

    except Exception as e:
        print(f"Error generating signal: {e}")
        return None

#Retain the original function, adapting it to use the new functions.
def generate_signals_for_dataset(model_obj, scaler_obj, df):
    """Generate signals for entire dataset."""
    result_signals = pd.Series(0, index=df.index)

    if model_obj is None:
        print("ML model not loaded")
        return result_signals

    try:
        feature_df = engineer_features(df.copy())

        if feature_df.empty:
            print("Empty dataset after feature engineering")
            return result_signals

        missing_columns = [col for col in FEATURE_COLUMNS if col not in feature_df.columns]
        if missing_columns:
            print(f"Missing features: {missing_columns}")
            return result_signals

        X = feature_df[FEATURE_COLUMNS]

        if scaler_obj:
            try:
                X_scaled = scaler_obj.transform(X)
            except Exception as e:
                print(f"Scaling error: {e}")
                return result_signals
        else:
            X_scaled = X

        predictions = model_obj.predict(X_scaled)
        signals = pd.Series(np.where(predictions == 1, 1, -1), index=feature_df.index)
        result_signals.update(signals)

        return result_signals

    except Exception as e:
        print(f"Error generating dataset signals: {e}")
        return result_signals