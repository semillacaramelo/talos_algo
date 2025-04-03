import os
import pandas as pd
import numpy as np
import joblib
from src.utils.logger import setup_logger

# Define signal constants
BUY = "BUY"
SELL = "SELL"
HOLD = "HOLD"

# Define SMA periods for strategy
SHORT_MA_PERIOD = 5
LONG_MA_PERIOD = 20

# Define feature columns used for prediction
FEATURE_COLUMNS = ['price_change_1', 'price_change_5', 'ma_diff']

# Define minimum data points needed for feature engineering
MIN_FEATURE_POINTS = 20

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
    # Calculate price changes
    df['price_change_1'] = df['close'].diff(1)
    df['price_change_5'] = df['close'].diff(5)
    
    # Calculate moving averages
    df['sma_5'] = df['close'].rolling(window=SHORT_MA_PERIOD).mean()
    df['sma_20'] = df['close'].rolling(window=LONG_MA_PERIOD).mean()
    
    # Calculate difference between moving averages
    df['ma_diff'] = df['sma_5'] - df['sma_20']
    
    # Drop rows with NaN values from feature calculations
    df.dropna(inplace=True)
    
    return df

def train_or_load_model():
    """
    Load a pre-trained ML model and scaler from disk.

    Returns:
        tuple: (model, scaler) where model is the loaded ML model object and scaler is the StandardScaler object,
               or (None, None) if loading fails.
    """
    # Paths are relative to the current file
    MODEL_FILE_PATH = os.path.join(os.path.dirname(__file__), 'basic_predictor.joblib')
    SCALER_FILE_PATH = os.path.join(os.path.dirname(__file__), 'scaler.joblib')
    
    # Load the model
    try:
        logger.info(f"Attempting to load model from: {MODEL_FILE_PATH}")
        model = joblib.load(MODEL_FILE_PATH)
        logger.info(f"Model loaded successfully from {MODEL_FILE_PATH}")
    except FileNotFoundError:
        logger.error(f"Model file not found at {MODEL_FILE_PATH}. Cannot generate ML signals.")
        return None, None
    except Exception as e:
        logger.exception(f"Failed to load model from {MODEL_FILE_PATH}: {e}")
        return None, None
        
    # Load the scaler
    scaler = None
    try:
        logger.info(f"Attempting to load scaler from: {SCALER_FILE_PATH}")
        scaler = joblib.load(SCALER_FILE_PATH)
        logger.info(f"Scaler loaded successfully from {SCALER_FILE_PATH}")
    except FileNotFoundError:
        logger.warning(f"Scaler file not found at {SCALER_FILE_PATH}. Will use unscaled features.")
        scaler = None
    except Exception as e:
        logger.exception(f"Failed to load scaler from {SCALER_FILE_PATH}: {e}")
        scaler = None
    
    return model, scaler

def generate_signal(model_obj, scaler_obj, recent_ticks_deque):
    """
    Generates a trading signal based on ML model prediction.

    Parameters:
        model_obj (object): The loaded ML model object
        scaler_obj (object): The loaded scaler object for feature scaling
        recent_ticks_deque (deque): Deque containing recent tick data

    Returns:
        str: A trading signal (BUY, SELL, or HOLD).
    """
    # Check if model is loaded
    if model_obj is None:
        logger.error("ML model not loaded, cannot generate signal")
        return HOLD

    # Check if we have enough data points for feature engineering
    if len(recent_ticks_deque) < MIN_FEATURE_POINTS:
        logger.debug(f"Insufficient data points ({len(recent_ticks_deque)}/{MIN_FEATURE_POINTS}) for ML prediction.")
        return HOLD

    try:
        # Preparing features for ML prediction
        logger.info("Preparing features for ML prediction...")
        df = pd.DataFrame(list(recent_ticks_deque))
        
        # Use the engineer_features function to calculate features
        df = engineer_features(df)
        
        # Check if we have enough data after preprocessing
        if df.empty or len(df) == 0:
            logger.warning("No data available after preprocessing for ML prediction.")
            return HOLD
            
        # Get the most recent row of features for prediction
        latest_features_df = df[FEATURE_COLUMNS].iloc[-1:] 
        
        # Apply scaler if available
        if scaler_obj:
            try:
                features_to_predict = scaler_obj.transform(latest_features_df)
                logger.debug("Features scaled successfully.")
            except Exception as e:
                logger.exception(f"Error applying scaler: {e}")
                return HOLD  # Cannot predict without scaling if scaler exists
        else:
            features_to_predict = latest_features_df  # Use unscaled if no scaler loaded
        
        # Log feature shape for debugging
        logger.debug(f"Features shape for prediction: {features_to_predict.shape}")
        
        # Make prediction
        try:
            prediction = model_obj.predict(features_to_predict)[0]
            logger.debug(f"Raw model prediction: {prediction}")
            
            # Map prediction to trading signal
            if prediction == 1:
                logger.info("ML Prediction: RISE")
                return BUY
            elif prediction == 0:
                logger.info("ML Prediction: FALL")
                return SELL
            else:
                logger.warning(f"Unexpected model prediction value: {prediction}")
                return HOLD
                
        except Exception as e:
            logger.exception(f"Error during model prediction: {e}")
            return HOLD
            
    except Exception as e:
        logger.exception("Error generating ML signal")
        return HOLD

def generate_signals_for_dataset(model_obj, scaler_obj, df):
    """
    Generates trading signals for an entire dataset using the ML model.
    Useful for backtesting or analyzing historical performance.

    Parameters:
        model_obj (object): The loaded ML model object
        scaler_obj (object): The loaded scaler object for feature scaling
        df (pd.DataFrame): DataFrame containing at least 'time' and 'close' columns

    Returns:
        pd.Series: A series of trading signals indexed the same as the input dataframe
    """
    # Check if model is loaded
    if model_obj is None:
        logger.error("ML model not loaded, cannot generate signals for dataset")
        return pd.Series(index=df.index)

    try:
        # Engineer features for the entire dataset
        logger.info("Engineering features for the dataset...")
        feature_df = engineer_features(df.copy())
        
        # Check if we have data after feature engineering
        if feature_df.empty:
            logger.warning("Feature engineering resulted in empty dataset")
            return pd.Series(index=df.index)
        
        # Extract features for prediction
        X = feature_df[FEATURE_COLUMNS]
        
        # Apply scaler if available
        if scaler_obj:
            try:
                X_scaled = scaler_obj.transform(X)
                logger.info("Features scaled successfully")
            except Exception as e:
                logger.exception(f"Error applying scaler to dataset: {e}")
                return pd.Series(index=df.index)
        else:
            X_scaled = X
        
        # Generate predictions
        try:
            predictions = model_obj.predict(X_scaled)
            logger.info(f"Generated {len(predictions)} predictions")
            
            # Map predictions to signals (1=BUY, -1=SELL)
            signals = pd.Series(
                np.where(predictions == 1, 1, -1),
                index=feature_df.index
            )
            
            # Count signal types for logging
            buy_count = len(signals[signals == 1])
            sell_count = len(signals[signals == -1])
            logger.info(f"Signal distribution - BUY: {buy_count}, SELL: {sell_count}")
            
            return signals
            
        except Exception as e:
            logger.exception(f"Error generating predictions: {e}")
            return pd.Series(index=df.index)
            
    except Exception as e:
        logger.exception(f"Error in generate_signals_for_dataset: {e}")
        return pd.Series(index=df.index)