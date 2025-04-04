
import os
import logging
import asyncio
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, accuracy_score
import joblib

from src.data.data_handler import get_historical_data
from src.models.signal_model import engineer_features, FEATURE_COLUMNS
from src.utils.logger import setup_logger
from config.settings import INSTRUMENT, TIMEFRAME_SECONDS

# Set up logger
logger = setup_logger()

async def fetch_training_data():
    """Fetch historical data for training."""
    try:
        from src.api.deriv_api_handler import DerivAPIWrapper
        api = DerivAPIWrapper()
        await api.connect()
        
        # Fetch 5000 bars of historical data
        historical_data = await get_historical_data(
            api=api.api,
            instrument=INSTRUMENT,
            granularity=TIMEFRAME_SECONDS,
            count=5000
        )
        
        await api.disconnect()
        return historical_data
        
    except Exception as e:
        logger.exception("Error fetching training data")
        return pd.DataFrame()

def prepare_features_and_target(df):
    """Prepare features and target variable."""
    try:
        # Engineer features using existing function
        feature_df = engineer_features(df.copy())
        
        if feature_df.empty:
            logger.error("Feature engineering resulted in empty DataFrame")
            return None, None
        
        # Log feature head to verify calculated features
        logger.info("Feature data sample:")
        logger.info(feature_df[FEATURE_COLUMNS].head())
        
        # Log null value counts to check for issues
        logger.info("Null values in features:")
        logger.info(feature_df[FEATURE_COLUMNS].isnull().sum())
            
        # Create target variable (next candle direction)
        # 1 for price increase, 0 for decrease or no change
        feature_df['target'] = (feature_df['close'].shift(-1) > feature_df['close']).astype(int)
        
        # Remove last row (has NaN target)
        feature_df = feature_df.iloc[:-1]
        
        # Select features and target using updated FEATURE_COLUMNS
        X = feature_df[FEATURE_COLUMNS]
        y = feature_df['target']
        
        return X, y
        
    except Exception as e:
        logger.exception("Error preparing features and target")
        return None, None

def train_and_save_model(X, y):
    """Train RandomForest model and save it with its scaler."""
    try:
        # Train/test split (no shuffle to maintain time series integrity)
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, shuffle=False
        )
        
        # Scale features
        scaler = StandardScaler()
        X_train_scaled = scaler.fit_transform(X_train)
        X_test_scaled = scaler.transform(X_test)
        
        # Initialize and train model
        model = RandomForestClassifier(
            n_estimators=100,
            random_state=42,
            class_weight='balanced',
            n_jobs=-1
        )
        
        model.fit(X_train_scaled, y_train)
        
        # Evaluate model
        y_pred = model.predict(X_test_scaled)
        accuracy = accuracy_score(y_test, y_pred)
        logger.info(f"Model Accuracy: {accuracy:.4f}")
        logger.info("\nClassification Report:\n" + 
                   classification_report(y_test, y_pred))
        
        # Save model and scaler
        model_path = os.path.join('src', 'models', 'basic_predictor.joblib')
        scaler_path = os.path.join('src', 'models', 'scaler.joblib')
        
        joblib.dump(model, model_path)
        joblib.dump(scaler, scaler_path)
        
        logger.info(f"Model saved to {model_path}")
        logger.info(f"Scaler saved to {scaler_path}")
        
        return True
        
    except Exception as e:
        logger.exception("Error in model training pipeline")
        return False

async def main():
    """Main training pipeline."""
    logger.info("Starting model training pipeline...")
    
    # Fetch data
    df = await fetch_training_data()
    if df.empty:
        logger.error("Failed to fetch training data")
        return
    
    # Prepare features and target
    X, y = prepare_features_and_target(df)
    if X is None or y is None:
        logger.error("Failed to prepare features and target")
        return
    
    # Train and save model
    success = train_and_save_model(X, y)
    if success:
        logger.info("Model training pipeline completed successfully")
    else:
        logger.error("Model training pipeline failed")

if __name__ == "__main__":
    asyncio.run(main())
