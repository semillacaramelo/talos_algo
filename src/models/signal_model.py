import os
import pandas as pd
from joblib import load
from typing import Tuple, Optional, List, Union
import numpy as np
import pandas_ta as ta

# Features used by the model
FEATURE_COLUMNS = [
    'price_change', 'ma_diff', 'rsi', 'atr', 
    'stoch_k', 'stoch_d', 'macd', 'macd_signal',
    'STOCHk_14_3_3', 'STOCHd_14_3_3',
    'MACD_12_26_9', 'MACDh_12_26_9', 'MACDs_12_26_9',
    # Adding more technical indicators as features
    'bollinger_pct_b', 'bollinger_width',
    'adx', 'adx_pos', 'adx_neg',
    'cci', 'mfi', 'obv_norm',
    'volatility', 'ema_diff', 
    'wma_diff', 'ichimoku_diff'
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
        print("Successfully loaded ML model and scaler")
        return model, scaler
    except Exception as e:
        print(f"Error loading model/scaler: {e}")
        print("Attempting to create a new compatible dummy model...")
        try:
            # Import here to avoid circular imports
            from src.models.dummy_model import create_dummy_model
            return create_dummy_model()
        except Exception as e2:
            print(f"Failed to create dummy model: {e2}")
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

        # Add enhanced technical indicators using pandas_ta
        # Stochastic Oscillator (standard 14,3,3 periods)
        df.ta.stoch(k=14, d=3, append=True)
        
        # MACD (standard 12,26,9 periods)
        df.ta.macd(fast=12, slow=26, signal=9, append=True)
        
        # New Feature #1: Bollinger Bands
        bb = df.ta.bbands(length=20, std=2)
        # Extract middle, upper and lower bands
        if not bb.empty:
            df['bollinger_mid'] = bb[f'BBM_20_2.0']
            df['bollinger_upper'] = bb[f'BBU_20_2.0']
            df['bollinger_lower'] = bb[f'BBL_20_2.0']
            # Calculate %B (percentage of price relative to the bands)
            df['bollinger_pct_b'] = (df['close'] - df['bollinger_lower']) / (df['bollinger_upper'] - df['bollinger_lower'])
            # Calculate bandwidth
            df['bollinger_width'] = (df['bollinger_upper'] - df['bollinger_lower']) / df['bollinger_mid']
        
        # New Feature #2: ADX (Average Directional Index)
        adx = df.ta.adx(length=14)
        if not adx.empty:
            # Get ADX value and directional indicators
            df['adx'] = adx[f'ADX_14']
            df['adx_pos'] = adx[f'DMP_14']  # Positive directional movement
            df['adx_neg'] = adx[f'DMN_14']  # Negative directional movement
        
        # New Feature #3: CCI (Commodity Channel Index)
        cci = df.ta.cci(length=20)
        if not cci.empty:
            df['cci'] = cci[f'CCI_20']
        
        # New Feature #4: MFI (Money Flow Index) - volume weighted RSI
        if 'volume' in df.columns:
            mfi = df.ta.mfi(length=14)
            if not mfi.empty:
                df['mfi'] = mfi[f'MFI_14']
        
        # New Feature #5: OBV (On-Balance Volume) - normalized to recent range
        if 'volume' in df.columns:
            df['obv'] = df.ta.obv()
            # Normalize OBV based on the last 20 periods
            df['obv_norm'] = (df['obv'] - df['obv'].rolling(20).min()) / (df['obv'].rolling(20).max() - df['obv'].rolling(20).min())
        
        # New Feature #6: Volatility ratio (20-day vs 50-day)
        df['vol_20'] = df['close'].pct_change().rolling(20).std()
        df['vol_50'] = df['close'].pct_change().rolling(50).std()
        df['volatility'] = df['vol_20'] / df['vol_50']
        
        # New Feature #7: EMA (Exponential Moving Average) difference
        df['ema_fast'] = df['close'].ewm(span=12, adjust=False).mean()
        df['ema_slow'] = df['close'].ewm(span=26, adjust=False).mean()
        df['ema_diff'] = (df['ema_fast'] - df['ema_slow']) / df['close']
        
        # New Feature #8: WMA (Weighted Moving Average) difference
        wma_fast = df.ta.wma(length=10)
        wma_slow = df.ta.wma(length=30)
        if not wma_fast.empty and not wma_slow.empty:
            df['wma_fast'] = wma_fast[f'WMA_10']
            df['wma_slow'] = wma_slow[f'WMA_30']
            df['wma_diff'] = (df['wma_fast'] - df['wma_slow']) / df['close']
        
        # New Feature #9: Ichimoku Cloud
        ichimoku = df.ta.ichimoku()
        if not ichimoku.empty:
            # Extract key Ichimoku components
            df['tenkan'] = ichimoku['ITS_9']  # Conversion line
            df['kijun'] = ichimoku['IKS_26']  # Base line
            # Calculate difference between conversion and base lines
            df['ichimoku_diff'] = (df['tenkan'] - df['kijun']) / df['close']
        
        # Drop any rows with NaN values after all calculations
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
        features_df = df[FEATURE_COLUMNS].iloc[-1:]
        
        # Convert to numpy array without feature names to avoid warnings
        features = features_df.values

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

        # Get features as DataFrame first
        X_df = feature_df[FEATURE_COLUMNS]
        
        # Convert to numpy array to avoid feature names warnings
        X = X_df.values

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