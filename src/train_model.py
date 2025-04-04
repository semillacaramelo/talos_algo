
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
        
        # Fetch multiple chunks of historical data to get more data than the API limit allows in a single request
        total_data_chunks = []
        
        # Fetch 10000 bars in total (2 chunks of 5000 bars each)
        for i in range(2):
            logger.info(f"Fetching historical data chunk {i+1}/2...")
            
            # Fetch 5000 bars of historical data
            chunk_data = await get_historical_data(
                api=api.api,
                instrument=INSTRUMENT,
                granularity=TIMEFRAME_SECONDS,
                count=5000
            )
            
            if not chunk_data.empty:
                total_data_chunks.append(chunk_data)
                
                # If we need to fetch more, use the earliest timestamp as reference for next fetch
                if i < 1 and not chunk_data.empty:
                    # Sleep briefly to avoid API rate limits
                    await asyncio.sleep(1)
        
        await api.disconnect()
        
        # Combine all data chunks
        if total_data_chunks:
            # Concatenate all chunks and sort by time
            all_data = pd.concat(total_data_chunks)
            all_data = all_data.drop_duplicates(subset=['time'])
            all_data = all_data.sort_values(by='time')
            
            logger.info(f"Successfully fetched {len(all_data)} historical data points")
            return all_data
        else:
            logger.error("Failed to fetch any historical data chunks")
            return pd.DataFrame()
        
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
        
        # Find the best hyperparameters for model
        from sklearn.model_selection import GridSearchCV
        
        # Initialize a base RandomForest model
        base_model = RandomForestClassifier(random_state=42, n_jobs=-1)
        
        # Define hyperparameters to search
        param_grid = {
            'n_estimators': [100, 200, 300],
            'max_depth': [None, 10, 20, 30],
            'min_samples_split': [2, 5, 10],
            'min_samples_leaf': [1, 2, 4],
            'class_weight': ['balanced', 'balanced_subsample', None]
        }
        
        # Initialize GridSearchCV
        grid_search = GridSearchCV(
            estimator=base_model,
            param_grid=param_grid, 
            cv=3,  # 3-fold cross-validation
            scoring='accuracy',
            n_jobs=-1,  # Use all available cores
            verbose=1
        )
        
        # Fit the grid search to find best parameters
        logger.info("Starting hyperparameter optimization with GridSearchCV...")
        grid_search.fit(X_train_scaled, y_train)
        
        # Get best model
        best_model = grid_search.best_estimator_
        logger.info(f"Best parameters found: {grid_search.best_params_}")
        
        # Evaluate model on test set
        y_pred = best_model.predict(X_test_scaled)
        accuracy = accuracy_score(y_test, y_pred)
        logger.info(f"Model Accuracy: {accuracy:.4f}")
        logger.info("\nClassification Report:\n" + 
                   classification_report(y_test, y_pred))
        
        # Feature importance
        feature_importances = pd.DataFrame(
            best_model.feature_importances_,
            index=X.columns,
            columns=['importance']
        ).sort_values('importance', ascending=False)
        
        logger.info("\nFeature Importances:\n" + str(feature_importances.head(10)))
        
        # Save model and scaler
        model_path = os.path.join('src', 'models', 'basic_predictor.joblib')
        scaler_path = os.path.join('src', 'models', 'scaler.joblib')
        
        joblib.dump(best_model, model_path)
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
