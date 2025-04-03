#!/usr/bin/env python3
import asyncio
import pandas as pd
import joblib
import os
import sys

# Add the project root directory to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report
from sklearn.preprocessing import StandardScaler

# Import project code
from api.deriv_api_handler import connect_deriv_api, disconnect
from data.data_handler import get_historical_data
from models.signal_model import engineer_features, FEATURE_COLUMNS
from config.settings import INSTRUMENT, TIMEFRAME_SECONDS

async def fetch_data_for_training(count=5000):
    """
    Fetches historical data from the Deriv API for model training.
    
    Parameters:
        count (int): Number of historical data points to fetch
        
    Returns:
        pd.DataFrame: DataFrame containing historical price data
    """
    print(f"Fetching {count} historical data points for {INSTRUMENT}...")
    
    # Connect to the API
    api = await connect_deriv_api()
    if not api:
        print("Failed to connect to Deriv API.")
        return None
    
    try:
        # Fetch historical data
        historical_df = await get_historical_data(api, INSTRUMENT, TIMEFRAME_SECONDS, count)
        print(f"Successfully fetched {len(historical_df)} data points.")
        return historical_df
    except Exception as e:
        print(f"Error fetching historical data: {e}")
        return None
    finally:
        # Ensure proper disconnection
        await disconnect(api)
        print("Disconnected from Deriv API.")

def train_and_save_model(df):
    """
    Trains and saves a machine learning model using the provided data.
    
    Parameters:
        df (pd.DataFrame): DataFrame containing time and close price data
    """
    print("Starting feature engineering process...")
    
    # Engineer features
    df = engineer_features(df)
    
    # Check if dataframe is empty after feature engineering
    if df.empty:
        print("Error: DataFrame is empty after feature engineering.")
        return
    
    print(f"Feature engineering completed. Data shape: {df.shape}")
    
    # Define target - predict next candle's direction
    df['future_price'] = df['close'].shift(-1)
    df['target'] = (df['future_price'] > df['close']).astype(int)
    df.dropna(subset=['target'], inplace=True)  # Remove last row with NaN target
    
    print(f"Target distribution: {df['target'].value_counts().to_dict()}")
    
    # Prepare data
    X = df[FEATURE_COLUMNS]
    y = df['target']
    
    # Split data
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, shuffle=False)
    
    # Check if training data is empty
    if len(X_train) == 0 or len(y_train) == 0:
        print("Error: Training data is empty after splitting.")
        return
    
    print(f"Training data shape: {X_train.shape}, Test data shape: {X_test.shape}")
    
    # Scale features
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)
    
    # Train model
    print("Training LogisticRegression model...")
    model = LogisticRegression(random_state=42, class_weight='balanced')
    model.fit(X_train_scaled, y_train)
    
    # Evaluate model
    y_pred = model.predict(X_test_scaled)
    print(f"Model Accuracy: {accuracy_score(y_test, y_pred):.4f}")
    print(classification_report(y_test, y_pred))
    
    # Save model & scaler
    model_dir = os.path.join(os.path.dirname(__file__), 'models')
    os.makedirs(model_dir, exist_ok=True)
    
    model_path = os.path.join(model_dir, 'basic_predictor.joblib')
    scaler_path = os.path.join(model_dir, 'scaler.joblib')
    
    joblib.dump(model, model_path)
    print(f"Model saved to {model_path}")
    
    joblib.dump(scaler, scaler_path)
    print(f"Scaler saved to {scaler_path}")

if __name__ == "__main__":
    print("Starting model training process...")
    
    hist_df = asyncio.run(fetch_data_for_training())
    
    if hist_df is not None and not hist_df.empty:
        train_and_save_model(hist_df)
    else:
        print("Failed to fetch data, cannot train model.")
    
    print("Training process finished.")