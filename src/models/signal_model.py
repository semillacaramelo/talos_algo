import os
import pandas as pd
import joblib
from src.utils.logger import setup_logger

# Define signal constants
BUY = "BUY"
SELL = "SELL"
HOLD = "HOLD"

# Define minimum data points needed for feature engineering
MIN_FEATURE_POINTS = 20

# Set up logger
logger = setup_logger()

def train_or_load_model():
    """
    Load a pre-trained ML model from disk.

    Returns:
        object: The loaded ML model object, or None if loading fails.
    """
    # Path is relative to the current file
    MODEL_FILE_PATH = os.path.join(os.path.dirname(__file__), 'basic_predictor.joblib')
    
    try:
        logger.info(f"Attempting to load model from: {MODEL_FILE_PATH}")
        model = joblib.load(MODEL_FILE_PATH)
        logger.info(f"Model loaded successfully from {MODEL_FILE_PATH}")
        return model
    except FileNotFoundError:
        logger.error(f"Model file not found at {MODEL_FILE_PATH}. Cannot generate ML signals.")
        return None
    except Exception as e:
        logger.exception(f"Failed to load model from {MODEL_FILE_PATH}: {e}")
        return None

def generate_signal(model_obj, recent_ticks_deque):
    """
    Generates a trading signal based on ML model prediction.

    Parameters:
        model_obj (object): The loaded ML model object
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
        
        # TODO: Replace these placeholders with ACTUAL feature engineering used for training!
        # Example Features (MUST BE REPLACED):
        df['price_change_1'] = df['close'].diff()
        df['price_change_5'] = df['close'].diff(5)
        df['rolling_mean_5'] = df['close'].rolling(window=5).mean()
        df['rolling_mean_10'] = df['close'].rolling(window=10).mean()
        df['ma_diff'] = df['rolling_mean_5'] - df['rolling_mean_10']
        df['rolling_std_5'] = df['close'].rolling(window=5).std()
        
        # Drop rows with NaN values resulting from feature calculation
        df.dropna(inplace=True)
        
        # Select ONLY the feature columns used by the model in the correct order
        feature_columns = ['price_change_1', 'price_change_5', 'ma_diff', 'rolling_std_5']  # TODO: Use ACTUAL feature columns
        
        # Check if we have enough data after preprocessing
        if df.empty or len(df) == 0:
            logger.warning("No data available after preprocessing for ML prediction.")
            return HOLD
            
        # Get the most recent row of features for prediction
        latest_features = df[feature_columns].iloc[-1:] 
        
        # Log feature shape for debugging
        logger.debug(f"Features shape for prediction: {latest_features.shape}")
        
        # Make prediction
        try:
            prediction = model_obj.predict(latest_features)[0]
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