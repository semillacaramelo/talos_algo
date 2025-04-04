
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

# Fix imports to work both when run directly and as a module
import sys
from pathlib import Path

# Add the project root to the path if running the script directly
if __name__ == "__main__":
    project_root = str(Path(__file__).parent.parent)
    if project_root not in sys.path:
        sys.path.append(project_root)

from data.data_handler import get_historical_data
from models.signal_model import engineer_features, FEATURE_COLUMNS
from utils.logger import setup_logger
from config.settings import INSTRUMENT, TIMEFRAME_SECONDS

# Set up logger
logger = setup_logger()

async def fetch_training_data():
    """Fetch historical data for training."""
    try:
        from api.deriv_api_handler import DerivAPIWrapper
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
            
        # Create target variable with minimum threshold to filter out noise
        # Calculate percent change for next candle
        feature_df['next_pct_change'] = feature_df['close'].pct_change(-1)  # Next candle's percent change
        
        # Define threshold for significant movement (e.g., 0.05% which is 0.0005)
        threshold = 0.0005
        
        # Define target based on threshold
        # 1 for significant increase, 0 for significant decrease, drop small changes
        feature_df['target'] = feature_df['next_pct_change'].apply(
            lambda x: 1 if x > threshold else (0 if x < -threshold else np.nan)
        )
        
        # Drop rows with small price changes (not significant)
        feature_df = feature_df.dropna(subset=['target'])
        
        # Convert target to integer
        feature_df['target'] = feature_df['target'].astype(int)
        
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
        # Time series cross-validation (no shuffle to maintain time series integrity)
        # We'll use a walk-forward approach, which is more appropriate for time series data
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, shuffle=False
        )
        
        # Scale features
        scaler = StandardScaler()
        X_train_scaled = scaler.fit_transform(X_train)
        X_test_scaled = scaler.transform(X_test)
        
        # Import additional models for ensemble
        from sklearn.ensemble import GradientBoostingClassifier, ExtraTreesClassifier, VotingClassifier
        from sklearn.model_selection import GridSearchCV, TimeSeriesSplit
        from sklearn.metrics import roc_auc_score, precision_recall_curve, auc
        
        # Initialize multiple base models with different strengths
        models = {
            'rf': RandomForestClassifier(random_state=42, n_jobs=-1),
            'gb': GradientBoostingClassifier(random_state=42),
            'et': ExtraTreesClassifier(random_state=42, n_jobs=-1)
        }
        
        # Use TimeSeriesSplit for more appropriate validation of time series data
        tscv = TimeSeriesSplit(n_splits=5)
        
        # Define hyperparameters for RandomForest (our primary model)
        rf_param_grid = {
            'n_estimators': [200, 300],
            'max_depth': [15, 20, 25],
            'min_samples_split': [2, 5],
            'class_weight': ['balanced', None]
        }
        
        # Initialize GridSearchCV with time series cross-validation
        grid_search = GridSearchCV(
            estimator=models['rf'],
            param_grid=rf_param_grid, 
            cv=tscv,  # Use time series cross-validation
            scoring='roc_auc',  # AUC is better for imbalanced data
            n_jobs=-1,  # Use all available cores
            verbose=1
        )
        
        # Fit the grid search to find best parameters
        logger.info("Starting hyperparameter optimization with GridSearchCV...")
        grid_search.fit(X_train_scaled, y_train)
        
        # Get best RandomForest model
        best_rf_model = grid_search.best_estimator_
        logger.info(f"Best parameters found: {grid_search.best_params_}")
        
        # Train GradientBoosting with default parameters
        models['gb'].fit(X_train_scaled, y_train)
        
        # Train ExtraTrees with default parameters
        models['et'].fit(X_train_scaled, y_train)
        
        # Create a voting ensemble of the three models
        # Use soft voting (based on predicted probabilities)
        voting_model = VotingClassifier(
            estimators=[
                ('rf', best_rf_model),
                ('gb', models['gb']),
                ('et', models['et'])
            ],
            voting='soft'
        )
        
        # Train the voting ensemble
        voting_model.fit(X_train_scaled, y_train)
        
        # Evaluate models on test set
        models_to_evaluate = {
            'Random Forest': best_rf_model,
            'Gradient Boosting': models['gb'],
            'Extra Trees': models['et'],
            'Voting Ensemble': voting_model
        }
        
        best_auc = 0
        best_model = None
        
        for name, model in models_to_evaluate.items():
            # Get predictions
            y_pred = model.predict(X_test_scaled)
            y_pred_proba = model.predict_proba(X_test_scaled)[:,1]
            
            # Calculate metrics
            accuracy = accuracy_score(y_test, y_pred)
            roc_auc = roc_auc_score(y_test, y_pred_proba)
            
            # Calculate precision-recall AUC
            precision, recall, _ = precision_recall_curve(y_test, y_pred_proba)
            pr_auc = auc(recall, precision)
            
            logger.info(f"\n{name} Evaluation:")
            logger.info(f"Accuracy: {accuracy:.4f}")
            logger.info(f"ROC AUC: {roc_auc:.4f}")
            logger.info(f"PR AUC: {pr_auc:.4f}")
            logger.info("\nClassification Report:\n" + 
                       classification_report(y_test, y_pred))
            
            # Keep track of best model based on ROC AUC
            if roc_auc > best_auc:
                best_auc = roc_auc
                best_model = model
        
        # Use the voting ensemble as our final model
        final_model = voting_model
        
        # If we have a high-performing single model, consider using it instead
        # This is a fallback in case the ensemble doesn't perform well
        if best_auc > 0.6 and best_model != voting_model:
            logger.info(f"Using {list(models_to_evaluate.keys())[list(models_to_evaluate.values()).index(best_model)]} as final model due to superior performance")
            final_model = best_model
        
        # Feature importance (from RandomForest since ensemble doesn't have feature_importances_)
        feature_importances = pd.DataFrame(
            best_rf_model.feature_importances_,
            index=X.columns,
            columns=['importance']
        ).sort_values('importance', ascending=False)
        
        logger.info("\nFeature Importances:\n" + str(feature_importances.head(10)))
        
        # Save model and scaler
        model_path = os.path.join('src', 'models', 'basic_predictor.joblib')
        scaler_path = os.path.join('src', 'models', 'scaler.joblib')
        
        joblib.dump(final_model, model_path)
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
