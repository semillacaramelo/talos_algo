import os
import pandas as pd
import numpy as np
import pandas_ta as ta
import joblib
from src.utils.logger import setup_logger

# Define signal constants
BUY = "BUY"
SELL = "SELL"
HOLD = "HOLD"

# Update feature columns to match RandomForest model
FEATURE_COLUMNS = ['price_change_1', 'price_change_5', 'ma_diff', 'RSI_14', 'ATRr_14', 
                  'STOCHk_14_3_3', 'STOCHd_14_3_3', 'MACD_12_26_9', 'MACDs_12_26_9']

# Define minimum data points needed for feature engineering
MIN_FEATURE_POINTS = 26  # Increased due to MACD requirements

# Set up logger
logger = setup_logger()

def engineer_features(df):
    """
    Calculate technical features for machine learning prediction.

    Parameters:
        df (pd.DataFrame): DataFrame containing at least 'time' and 'close' columns

    Returns:
        pd.DataFrame: DataFrame with calculated features
    """
    df_copy = df.copy()

    # Calculate price changes
    df_copy['price_change_1'] = df_copy['close'].diff(1)
    df_copy['price_change_5'] = df_copy['close'].diff(5)

    # Calculate moving averages and difference
    df_copy['sma_5'] = df_copy['close'].rolling(window=5).mean()
    df_copy['sma_20'] = df_copy['close'].rolling(window=20).mean()
    df_copy['ma_diff'] = df_copy['sma_5'] - df_copy['sma_20']

    # Calculate RSI
    try:
        df_copy.ta.rsi(length=14, append=True)
    except Exception as e:
        logger.warning(f"Error calculating RSI: {e}. Using simple implementation.")
        delta = df_copy['close'].diff()
        gain = delta.where(delta > 0, 0)
        loss = -delta.where(delta < 0, 0)
        avg_gain = gain.rolling(window=14).mean()
        avg_loss = loss.rolling(window=14).mean()
        rs = avg_gain / avg_loss.replace(0, 0.001)
        df_copy['RSI_14'] = 100 - (100 / (1 + rs))

    # Calculate ATR and ATRr
    try:
        if 'high' in df_copy.columns and 'low' in df_copy.columns:
            df_copy.ta.atr(high='high', low='low', close='close', length=14, append=True)
        else:
            logger.warning("Missing high/low data for ATR. Using close price volatility.")
            close_changes = df_copy['close'].diff().abs()
            df_copy['ATR_14'] = close_changes.rolling(window=14).mean()
        df_copy['ATRr_14'] = df_copy['ATR_14'] / df_copy['close'] * 100
    except Exception as e:
        logger.warning(f"Error calculating ATR: {e}")
        close_changes = df_copy['close'].diff().abs()
        df_copy['ATR_14'] = close_changes.rolling(window=14).mean()
        df_copy['ATRr_14'] = df_copy['ATR_14'] / df_copy['close'] * 100

    # Calculate Stochastic
    try:
        df_copy.ta.stoch(high='high', low='low', close='close', k=14, d=3, append=True)
    except Exception as e:
        logger.warning(f"Error calculating Stochastic: {e}")
        # Fallback calculation for Stochastic if needed
        n = 14
        df_copy['lowest_low'] = df_copy['low'].rolling(window=n).min()
        df_copy['highest_high'] = df_copy['high'].rolling(window=n).max()
        df_copy['STOCHk_14_3_3'] = ((df_copy['close'] - df_copy['lowest_low']) / 
                                   (df_copy['highest_high'] - df_copy['lowest_low'])) * 100
        df_copy['STOCHd_14_3_3'] = df_copy['STOCHk_14_3_3'].rolling(window=3).mean()

    # Calculate MACD
    try:
        df_copy.ta.macd(close='close', fast=12, slow=26, signal=9, append=True)
    except Exception as e:
        logger.warning(f"Error calculating MACD: {e}")
        # Fallback calculation for MACD
        exp1 = df_copy['close'].ewm(span=12, adjust=False).mean()
        exp2 = df_copy['close'].ewm(span=26, adjust=False).mean()
        df_copy['MACD_12_26_9'] = exp1 - exp2
        df_copy['MACDs_12_26_9'] = df_copy['MACD_12_26_9'].ewm(span=9, adjust=False).mean()

    # Drop rows with NaN values
    df_copy.dropna(inplace=True)

    return df_copy

def train_or_load_model():
    """Load pre-trained ML model and scaler from disk."""
    MODEL_FILE_PATH = os.path.join(os.path.dirname(__file__), 'basic_predictor.joblib')
    SCALER_FILE_PATH = os.path.join(os.path.dirname(__file__), 'scaler.joblib')

    try:
        logger.info(f"Loading model from: {MODEL_FILE_PATH}")
        model = joblib.load(MODEL_FILE_PATH)
        logger.info("Model loaded successfully")
    except Exception as e:
        logger.error(f"Failed to load model: {e}")
        return None, None

    try:
        logger.info(f"Loading scaler from: {SCALER_FILE_PATH}")
        scaler = joblib.load(SCALER_FILE_PATH)
        logger.info("Scaler loaded successfully")
    except Exception as e:
        logger.warning(f"Failed to load scaler: {e}")
        scaler = None

    return model, scaler

def generate_signal(model_obj, scaler_obj, recent_ticks_deque):
    """Generate trading signal based on ML model prediction."""
    if model_obj is None:
        logger.error("ML model not loaded")
        return HOLD

    if len(recent_ticks_deque) < MIN_FEATURE_POINTS:
        logger.debug(f"Insufficient data points ({len(recent_ticks_deque)}/{MIN_FEATURE_POINTS})")
        return HOLD

    try:
        # Prepare features
        df = pd.DataFrame(list(recent_ticks_deque))
        df = engineer_features(df)

        if df.empty:
            logger.warning("No data after preprocessing")
            return HOLD

        # Verify all features exist
        missing_columns = [col for col in FEATURE_COLUMNS if col not in df.columns]
        if missing_columns:
            logger.error(f"Missing features: {missing_columns}")
            return HOLD

        # Get latest features
        latest_features = df[FEATURE_COLUMNS].iloc[-1:]

        # Scale features if scaler exists
        if scaler_obj:
            try:
                features_scaled = scaler_obj.transform(latest_features)
            except Exception as e:
                logger.error(f"Scaling error: {e}")
                return HOLD
        else:
            features_scaled = latest_features

        # Generate prediction
        prediction = model_obj.predict(features_scaled)[0]
        logger.debug(f"Model prediction: {prediction}")

        return BUY if prediction == 1 else SELL

    except Exception as e:
        logger.exception(f"Error generating signal: {e}")
        return HOLD

def generate_signals_for_dataset(model_obj, scaler_obj, df):
    """Generate signals for entire dataset."""
    result_signals = pd.Series(0, index=df.index)

    if model_obj is None:
        logger.error("ML model not loaded")
        return result_signals

    try:
        feature_df = engineer_features(df.copy())

        if feature_df.empty:
            logger.warning("Empty dataset after feature engineering")
            return result_signals

        missing_columns = [col for col in FEATURE_COLUMNS if col not in feature_df.columns]
        if missing_columns:
            logger.error(f"Missing features: {missing_columns}")
            return result_signals

        X = feature_df[FEATURE_COLUMNS]

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
        logger.exception(f"Error generating dataset signals: {e}")
        return result_signals