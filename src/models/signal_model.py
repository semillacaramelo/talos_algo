import os
import pandas as pd
from joblib import load
from typing import Tuple, Optional, List, Union
import numpy as np
import pandas_ta as ta
import logging

# Configure logging
logger = logging.getLogger(__name__)

# Constants
MIN_FEATURE_POINTS = 50  # Increased from default to ensure enough data for calculations

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
    'wma_diff', 'ichimoku_diff',
    # New extended Ichimoku features
    'cloud_strength', 'price_to_cloud'
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
            from models.dummy_model import create_dummy_model
            return create_dummy_model()
        except Exception as e2:
            print(f"Failed to create dummy model: {e2}")
            return None, None

def engineer_features(df: pd.DataFrame) -> pd.DataFrame:
    """Calculate technical indicators for feature engineering."""
    if df is None or df.empty:
        logger.error("Cannot engineer features on empty DataFrame")
        return pd.DataFrame()
        
    if len(df) < MIN_FEATURE_POINTS:
        logger.warning(f"DataFrame has only {len(df)} points, minimum {MIN_FEATURE_POINTS} required for reliable feature engineering")
        # Still continue and try to process it, the caller will handle if returns empty
    
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
        try:
            # Manual calculation for CCI
            tp = (df['high'] + df['low'] + df['close']) / 3  # Typical price
            tp_sma = tp.rolling(window=20).mean()  # SMA of typical price
            
            # Instead of using Series.mad() which might not be available in all pandas versions,
            # calculate mean absolute deviation manually
            def mad(x):
                return np.abs(x - x.mean()).mean()
            
            md = tp.rolling(window=20).apply(mad, raw=True)  # Mean deviation using custom function
            
            # Handle zero mean deviation
            df['cci'] = df.apply(
                lambda x: (x['close'] - tp_sma.loc[x.name]) / (0.015 * md.loc[x.name]) if md.loc[x.name] > 0 else 0,
                axis=1
            )
            # Normalize CCI for consistent scale with other features
            df['cci'] = df['cci'] / 100
        except Exception as e:
            logger.error(f"CCI calculation error: {e}")
            df['cci'] = 0  # Neutral value
        
        # New Feature #4: MFI (Money Flow Index) - volume weighted RSI
        if 'volume' in df.columns:
            try:
                mfi = df.ta.mfi(length=14)
                if not mfi.empty:
                    df['mfi'] = mfi[f'MFI_14']
                else:
                    df['mfi'] = 50  # Neutral value for MFI
            except Exception as e:
                logger.error(f"MFI calculation error: {e}")
                df['mfi'] = 50  # Neutral value
        else:
            # No volume data, use RSI as proxy for MFI
            df['mfi'] = df['rsi']
        
        # New Feature #5: OBV (On-Balance Volume) - or proxy if volume not available
        if 'volume' in df.columns:
            try:
                df['obv'] = df.ta.obv()
                # Normalize OBV based on the last 20 periods
                df['obv_norm'] = (df['obv'] - df['obv'].rolling(20).min()) / (df['obv'].rolling(20).max() - df['obv'].rolling(20).min())
            except Exception as e:
                logger.error(f"OBV calculation error: {e}")
                # Use price momentum as a proxy
                df['obv_norm'] = df['price_change'].rolling(10).sum() / df['price_change'].rolling(10).std()
        else:
            # No volume data, use price momentum as proxy
            df['obv_norm'] = df['price_change'].rolling(10).sum() / df['price_change'].rolling(10).std()
        
        # New Feature #6: Volatility ratio (20-day vs 50-day)
        df['vol_20'] = df['close'].pct_change().rolling(20).std()
        df['vol_50'] = df['close'].pct_change().rolling(50).std()
        # Handle divide by zero
        df['volatility'] = df.apply(
            lambda x: x['vol_20'] / x['vol_50'] if x['vol_50'] > 0 else 1.0, 
            axis=1
        )
        
        # New Feature #7: EMA (Exponential Moving Average) difference
        df['ema_fast'] = df['close'].ewm(span=12, adjust=False).mean()
        df['ema_slow'] = df['close'].ewm(span=26, adjust=False).mean()
        df['ema_diff'] = (df['ema_fast'] - df['ema_slow']) / df['close']
        
        # New Feature #8: WMA (Weighted Moving Average) difference
        try:
            # Manual calculation of WMA
            # Create weight series
            fast_window = 10
            slow_window = 30
            
            # Calculate weighted moving averages manually
            # For fast WMA
            weights_fast = np.arange(1, fast_window + 1)
            df['wma_fast'] = df['close'].rolling(window=fast_window).apply(
                lambda x: np.sum(weights_fast * x) / np.sum(weights_fast), raw=True
            )
            
            # For slow WMA
            weights_slow = np.arange(1, slow_window + 1)
            df['wma_slow'] = df['close'].rolling(window=slow_window).apply(
                lambda x: np.sum(weights_slow * x) / np.sum(weights_slow), raw=True
            )
            
            # Calculate the difference
            df['wma_diff'] = (df['wma_fast'] - df['wma_slow']) / df['close']
            
        except Exception as e:
            logger.error(f"WMA calculation error: {e}")
            # Fallback to SMA if WMA fails
            df['wma_fast'] = df['close'].rolling(window=10).mean()
            df['wma_slow'] = df['close'].rolling(window=30).mean()
            df['wma_diff'] = (df['wma_fast'] - df['wma_slow']) / df['close']
        
        # New Feature #9: Ichimoku Cloud - Manual calculation
        try:
            # Tenkan-sen (Conversion Line): (highest high + lowest low)/2 for the past 9 periods
            high_9 = df['high'].rolling(window=9).max()
            low_9 = df['low'].rolling(window=9).min()
            df['tenkan'] = (high_9 + low_9) / 2
            
            # Kijun-sen (Base Line): (highest high + lowest low)/2 for the past 26 periods
            high_26 = df['high'].rolling(window=26).max()
            low_26 = df['low'].rolling(window=26).min()
            df['kijun'] = (high_26 + low_26) / 2
            
            # Senkou Span A (Leading Span A): (Conversion Line + Base Line)/2 (26 periods ahead)
            df['senkou_span_a'] = ((df['tenkan'] + df['kijun']) / 2)
            
            # Senkou Span B (Leading Span B): (highest high + lowest low)/2 for the past 52 periods (26 periods ahead)
            high_52 = df['high'].rolling(window=52).max()
            low_52 = df['low'].rolling(window=52).min()
            df['senkou_span_b'] = ((high_52 + low_52) / 2)
            
            # Chikou Span (Lagging Span): Current closing price (26 periods behind)
            # We don't calculate this as it won't be used for the feature
            
            # Calculate difference between Tenkan and Kijun as a feature
            df['ichimoku_diff'] = (df['tenkan'] - df['kijun']) / df['close']
            
            # Add additional Ichimoku-derived features
            # Cloud strength
            df['cloud_strength'] = (df['senkou_span_a'] - df['senkou_span_b']) / df['close']
            
            # Price relative to cloud
            df['price_to_cloud'] = (df['close'] - (df['senkou_span_a'] + df['senkou_span_b'])/2) / df['close']
            
        except Exception as e:
            logger.error(f"Ichimoku calculation error: {e}")
            # Fallback calculation
            df['tenkan'] = df['close'].rolling(window=9).mean()
            df['kijun'] = df['close'].rolling(window=26).mean()
            df['ichimoku_diff'] = (df['tenkan'] - df['kijun']) / df['close']
            # Set additional features to neutral values
            df['cloud_strength'] = 0
            df['price_to_cloud'] = 0
        
        # Drop any rows with NaN values after all calculations
        df.dropna(inplace=True)
        
        if df.empty:
            logger.warning("After feature engineering and dropping NaN values, DataFrame is empty")
        
        return df
        
    except Exception as e:
        logger.error(f"Error during feature calculation: {e}", exc_info=False)
        return pd.DataFrame()

def generate_signal(model, scaler, recent_data: pd.DataFrame) -> Optional[str]:
    """Generate trading signals using the ML model with improved features."""
    from enum import Enum
    
    # Define constants for signal types
    class Signal(str, Enum):
        BUY = "BUY"
        SELL = "SELL" 
        HOLD = "HOLD"
    
    try:
        if recent_data is None or len(recent_data) < MIN_FEATURE_POINTS:
            logger.warning(f"Not enough data points for feature calculation: {len(recent_data) if recent_data is not None else 0} (need {MIN_FEATURE_POINTS}+)")
            return Signal.HOLD
        
        # Engineer features - only after checking min data points
        df = engineer_features(recent_data.copy())
        
        # Handle empty dataframe case immediately
        if df is None or df.empty:
            logger.warning("Feature engineering resulted in empty DataFrame")
            return Signal.HOLD
            
        # Get currently selected features for the model
        try:
            # Try to load the selected features list
            import os
            import joblib
            features_path = os.path.join(os.path.dirname(__file__), 'selected_features.joblib')
            threshold_path = os.path.join(os.path.dirname(__file__), 'threshold_stats.joblib')
            
            if os.path.exists(features_path):
                selected_features = joblib.load(features_path)
                logger.info(f"Using {len(selected_features)} selected features for prediction")
            else:
                # If no selected features file exists, use all features
                selected_features = FEATURE_COLUMNS
                logger.info("Using all features for prediction (no feature selection file found)")
                
            # Load threshold statistics if available
            threshold_stats = None
            if os.path.exists(threshold_path):
                threshold_stats = joblib.load(threshold_path)
                logger.info(f"Using adaptive threshold with avg value: {threshold_stats['avg_threshold']:.6f}")
            
        except Exception as e:
            logger.error(f"Error loading selected features: {e}")
            # If there's an error, use all features
            selected_features = FEATURE_COLUMNS
            threshold_stats = None

        # Extract features for prediction
        available_features = [f for f in selected_features if f in df.columns]
        
        if len(available_features) < len(selected_features):
            missing = set(selected_features) - set(available_features)
            logger.warning(f"Missing {len(missing)} features: {missing}")
            
        if not available_features:
            logger.warning("No valid features available for prediction")
            return Signal.HOLD
            
        features_df = df[available_features].iloc[-1:]
        
        # Calculate prediction confidence before converting to numpy array
        # Check current volatility for adaptive threshold
        if threshold_stats:
            try:
                # Calculate current volatility
                current_volatility = df['close'].pct_change().rolling(window=20).std().iloc[-1]
                
                # Determine current adaptive threshold
                adaptive_threshold = max(
                    current_volatility * threshold_stats['volatility_multiplier'],
                    threshold_stats['min_threshold']
                )
                
                logger.info(f"Current volatility: {current_volatility:.6f}, Adaptive threshold: {adaptive_threshold:.6f}")
            except Exception as e:
                logger.error(f"Error calculating adaptive threshold: {e}")
        
        # Convert to numpy array without feature names to avoid warnings
        features = features_df.values

        # Scale features
        if scaler:
            try:
                features = scaler.transform(features)
            except Exception as e:
                logger.error(f"Error during feature scaling: {e}")
                return Signal.HOLD

        # Get prediction probability
        try:
            prediction_proba = model.predict_proba(features)[0]
            confidence = max(prediction_proba)
            prediction_class = 1 if prediction_proba[1] > prediction_proba[0] else 0
            
            # Stronger confidence requirement based on threshold
            min_confidence = 0.55  # Can be adjusted
            
            if confidence < min_confidence:
                logger.info(f"Prediction confidence too low: {confidence:.4f} < {min_confidence}")
                return Signal.HOLD
                
            # Make prediction
            prediction = prediction_class
                
        except AttributeError:
            # If model doesn't have predict_proba, use regular predict
            prediction = model.predict(features)[0]
        except Exception as e:
            logger.error(f"Error during prediction: {e}")
            return Signal.HOLD

        # Apply contextual logic based on price action
        try:
            # Get latest price data
            latest_close = df['close'].iloc[-1]
            prev_close = df['close'].iloc[-2]
            price_change = (latest_close - prev_close) / prev_close
            
            # Check for extreme price movements that might need caution
            extreme_move_threshold = 0.005  # 0.5% change
            
            if abs(price_change) > extreme_move_threshold:
                # In case of extreme movements, be more cautious
                logger.info(f"Extreme price movement detected: {price_change:.4f}")
                
                # Don't chase extreme movements in the same direction
                if (prediction == 1 and price_change > extreme_move_threshold) or \
                   (prediction == 0 and price_change < -extreme_move_threshold):
                    logger.info("Avoiding chasing extreme price movement")
                    return Signal.HOLD
        except Exception as e:
            logger.error(f"Error during price action analysis: {e}")
        
        # Map prediction to signal, including confidence
        if prediction == 1:
            return Signal.BUY
        else:
            return Signal.SELL

    except Exception as e:
        logger.error(f"Error generating signal: {e}")
        return Signal.HOLD

def generate_signals_for_dataset(model_obj, scaler_obj, df):
    """Generate signals for entire dataset."""
    result_signals = pd.Series(0, index=df.index)

    if model_obj is None:
        logger.error("ML model not loaded")
        return result_signals

    # Check if we have enough data points for feature engineering
    if len(df) < MIN_FEATURE_POINTS:
        logger.warning(f"Not enough data points for feature calculation: {len(df)} (need {MIN_FEATURE_POINTS}+)")
        return result_signals

    try:
        feature_df = engineer_features(df.copy())

        if feature_df.empty:
            logger.warning("Empty dataset after feature engineering")
            return result_signals

        missing_columns = [col for col in FEATURE_COLUMNS if col not in feature_df.columns]
        if missing_columns:
            logger.warning(f"Missing features: {missing_columns}")
            return result_signals

        # Get features as DataFrame first
        available_features = [f for f in FEATURE_COLUMNS if f in feature_df.columns]
        if not available_features:
            logger.warning("No valid features available for prediction")
            return result_signals
            
        X_df = feature_df[available_features]
        
        # Convert to numpy array to avoid feature names warnings
        X = X_df.values

        if scaler_obj:
            try:
                X_scaled = scaler_obj.transform(X)
            except Exception as e:
                logger.error(f"Scaling error: {e}")
                return result_signals
        else:
            X_scaled = X

        predictions = model_obj.predict(X_scaled)
        signals = pd.Series(np.where(predictions == 1, 1, -1), index=feature_df.index)
        result_signals.update(signals)

        return result_signals

    except Exception as e:
        logger.error(f"Error generating dataset signals: {e}", exc_info=True)
        return result_signals