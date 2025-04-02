import os
import pandas as pd # Import pandas
from src.utils.logger import setup_logger

# Define signal constants
BUY = "BUY"
SELL = "SELL"
HOLD = "HOLD"

# --- Strategy Parameters --- 
SHORT_MA_PERIOD = 5
LONG_MA_PERIOD = 20
# Minimum data points needed to calculate the longest MA
MIN_DATA_POINTS = LONG_MA_PERIOD

# Set up logger
logger = setup_logger()

def train_or_load_model():
    """
    Placeholder function to train or load a model.

    Returns:
        dict: A dummy object representing the model status.
    """
    model_path = "models/basic_predictor.joblib"

    try:
        if os.path.exists(model_path):
            logger.info("Model file found, attempting to load.")
            # TODO: Add loading logic using joblib/pickle
            return {"status": "loaded"}
        else:
            logger.info("Model file not found. Training placeholder activated.")
            # TODO: Add actual training logic using historical data
            return {"status": "trained_dummy"}
    except Exception as e:
        logger.exception("Error in train_or_load_model")
        return {"status": "error"}

def generate_signal(price_data_df):
    """
    Generates a trading signal based on SMA crossover.

    Parameters:
        price_data_df (pd.DataFrame): DataFrame containing recent price data 
                                      with at least a 'close' column.

    Returns:
        str: A trading signal (BUY, SELL, or HOLD).
    """
    # Check if we have any data
    if price_data_df is None or len(price_data_df) == 0:
        logger.debug("No data provided to generate signal.")
        return HOLD

    # Log data information for debugging
    if len(price_data_df) < MIN_DATA_POINTS:
        logger.debug(f"Insufficient data points ({len(price_data_df)}/{MIN_DATA_POINTS}) to calculate crossover.")
        return HOLD

    try:
        # Ensure 'close' column is numeric
        price_data_df['close'] = pd.to_numeric(price_data_df['close'])

        # Calculate SMAs
        price_data_df['short_ma'] = price_data_df['close'].rolling(window=SHORT_MA_PERIOD).mean()
        price_data_df['long_ma'] = price_data_df['close'].rolling(window=LONG_MA_PERIOD).mean()

        # Drop rows with NaN values (resulting from the rolling calculations)
        valid_data = price_data_df.dropna()
        
        # Check if we have enough valid data after MA calculations
        if len(valid_data) < 2:
            logger.debug(f"Not enough valid data after MA calculations. Need at least 2 rows, got {len(valid_data)}.")
            return HOLD

        # Get the latest two values to check for crossover
        last_row = valid_data.iloc[-1]
        prev_row = valid_data.iloc[-2]

        # Check for crossover conditions
        if last_row['short_ma'] > last_row['long_ma'] and prev_row['short_ma'] <= prev_row['long_ma']:
            logger.info(f"SMA Crossover Detected: BUY Signal (Short MA: {last_row['short_ma']:.2f}, Long MA: {last_row['long_ma']:.2f})")
            return BUY
        elif last_row['short_ma'] < last_row['long_ma'] and prev_row['short_ma'] >= prev_row['long_ma']:
            logger.info(f"SMA Crossover Detected: SELL Signal (Short MA: {last_row['short_ma']:.2f}, Long MA: {last_row['long_ma']:.2f})")
            return SELL
        else:
            # Only log detailed info occasionally to avoid log spam
            if hasattr(generate_signal, 'log_counter'):
                generate_signal.log_counter += 1
                if generate_signal.log_counter % 10 == 0:  # Log every 10th check
                    logger.debug(f"No crossover: Short MA ({last_row['short_ma']:.2f}) vs Long MA ({last_row['long_ma']:.2f})")
            else:
                generate_signal.log_counter = 1
            return HOLD

    except Exception as e:
        logger.exception("Error generating SMA signal")
        return HOLD