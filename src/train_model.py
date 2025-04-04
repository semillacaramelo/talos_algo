
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

async def fetch_training_data(timeframe_minutes=None, total_candles=10000):
    """
    Fetch historical data for training with support for multiple timeframes.
    
    Args:
        timeframe_minutes (int, optional): Timeframe in minutes (1, 5, 15, 30, 60, etc.)
                                         If None, uses the default from settings.py
        total_candles (int): Total number of candles to fetch
        
    Returns:
        pd.DataFrame: Historical OHLC data
    """
    try:
        from api.deriv_api_handler import DerivAPIWrapper
        api = DerivAPIWrapper()
        await api.connect()
        
        # Determine granularity in seconds
        if timeframe_minutes is None:
            # Use the default from settings.py
            granularity = TIMEFRAME_SECONDS
            timeframe_minutes = granularity // 60
        else:
            # Convert timeframe in minutes to seconds
            granularity = timeframe_minutes * 60
        
        # Log the selected timeframe
        logger.info(f"Fetching data with {timeframe_minutes}-minute timeframe ({granularity} seconds)")
        
        # Calculate how many chunks we need
        chunk_size = 5000  # API limit per request
        chunks_needed = (total_candles + chunk_size - 1) // chunk_size  # Ceiling division
        
        # Fetch multiple chunks of historical data
        total_data_chunks = []
        
        # Fetch the required number of candles in chunks
        for i in range(chunks_needed):
            logger.info(f"Fetching historical data chunk {i+1}/{chunks_needed}...")
            
            # Determine the number of candles to fetch in this chunk
            remaining = total_candles - (i * chunk_size)
            candles_to_fetch = min(chunk_size, remaining)
            
            # Fetch historical data with the specified granularity
            chunk_data = await get_historical_data(
                api=api.api,
                instrument=INSTRUMENT,
                granularity=granularity,
                count=candles_to_fetch
            )
            
            if not chunk_data.empty:
                total_data_chunks.append(chunk_data)
                
                # If we need to fetch more, sleep briefly to avoid API rate limits
                if i < chunks_needed - 1:
                    await asyncio.sleep(1)
        
        await api.disconnect()
        
        # Combine all data chunks
        if total_data_chunks:
            # Concatenate all chunks and sort by time
            all_data = pd.concat(total_data_chunks)
            all_data = all_data.drop_duplicates(subset=['time'])
            all_data = all_data.sort_values(by='time')
            
            # Store the timeframe information as an attribute
            all_data.attrs['timeframe_minutes'] = timeframe_minutes
            
            # Save raw data for future reference
            try:
                import os
                data_dir = os.path.join('src', 'data', 'historical')
                os.makedirs(data_dir, exist_ok=True)
                data_path = os.path.join(data_dir, f'historical_data_{timeframe_minutes}min.csv')
                all_data.to_csv(data_path, index=False)
                logger.info(f"Raw historical data saved to {data_path}")
            except Exception as e:
                logger.warning(f"Could not save historical data: {e}")
            
            logger.info(f"Successfully fetched {len(all_data)} historical data points for {timeframe_minutes}-minute timeframe")
            return all_data
        else:
            logger.error("Failed to fetch any historical data chunks")
            return pd.DataFrame()
        
    except Exception as e:
        logger.exception("Error fetching training data")
        return pd.DataFrame()

def prepare_features_and_target(df):
    """Prepare features and target variable with adaptive threshold."""
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
        
        # ===== ADAPTIVE THRESHOLD BASED ON MARKET VOLATILITY =====
        # Calculate percent change for next candle
        feature_df['next_pct_change'] = feature_df['close'].pct_change(-1)  # Next candle's percent change
        
        # Calculate rolling volatility (standard deviation of returns)
        feature_df['rolling_volatility'] = feature_df['close'].pct_change().rolling(window=20).std()
        
        # Adaptive threshold: use a multiplier of the local volatility
        # This makes the threshold higher in volatile periods and lower in calm periods
        volatility_multiplier = 0.5  # Can be tuned
        
        # Calculate adaptive threshold for each row
        feature_df['adaptive_threshold'] = feature_df['rolling_volatility'] * volatility_multiplier
        
        # Ensure minimum threshold to avoid noise during very low volatility
        min_threshold = 0.0004  # Lower bound for threshold
        feature_df['adaptive_threshold'] = feature_df['adaptive_threshold'].clip(lower=min_threshold)
        
        # Calculate the average threshold for reporting
        avg_threshold = feature_df['adaptive_threshold'].mean()
        logger.info(f"Using adaptive threshold with average value of {avg_threshold:.6f}")
        
        # Define target based on adaptive threshold
        # Create a new column with the target value
        feature_df['target'] = feature_df.apply(
            lambda row: 1 if row['next_pct_change'] > row['adaptive_threshold'] 
                      else (0 if row['next_pct_change'] < -row['adaptive_threshold'] 
                      else np.nan),
            axis=1
        )
        
        # Check class balance before filtering
        total_before = len(feature_df)
        pos_before = feature_df['next_pct_change'][feature_df['next_pct_change'] > 0].count()
        neg_before = feature_df['next_pct_change'][feature_df['next_pct_change'] < 0].count()
        logger.info(f"Before threshold: {pos_before} positive, {neg_before} negative out of {total_before} samples")
        
        # Drop rows with small price changes (not significant enough compared to local volatility)
        feature_df = feature_df.dropna(subset=['target'])
        
        # Check class balance after filtering
        total_after = len(feature_df)
        pos_after = feature_df['target'].sum()
        neg_after = total_after - pos_after
        filtered_pct = (1 - (total_after / total_before)) * 100
        logger.info(f"After adaptive threshold: {pos_after} positive, {neg_after} negative out of {total_after} samples")
        logger.info(f"Filtered out {filtered_pct:.1f}% of samples as noise")
        
        # Convert target to integer
        feature_df['target'] = feature_df['target'].astype(int)
        
        # Remove last row (might have NaN target if we look ahead)
        feature_df = feature_df[:-1]
        
        # Select features and target using updated FEATURE_COLUMNS
        X = feature_df[FEATURE_COLUMNS]
        y = feature_df['target']
        
        # Save the adaptive threshold statistics for use in prediction
        threshold_stats = {
            'avg_threshold': avg_threshold,
            'min_threshold': min_threshold,
            'volatility_multiplier': volatility_multiplier
        }
        
        # Save threshold statistics to a file for later use in live trading
        threshold_path = os.path.join('src', 'models', 'threshold_stats.joblib')
        joblib.dump(threshold_stats, threshold_path)
        logger.info(f"Threshold statistics saved to {threshold_path}")
        
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
        
        # Import additional models and feature selection tools
        from sklearn.ensemble import GradientBoostingClassifier, ExtraTreesClassifier, VotingClassifier
        from sklearn.model_selection import GridSearchCV, TimeSeriesSplit
        from sklearn.metrics import roc_auc_score, precision_recall_curve, auc
        from sklearn.feature_selection import SelectFromModel, mutual_info_classif, RFE
        
        # ===== FEATURE SELECTION =====
        logger.info("Performing feature selection to improve model performance...")
        
        # Method 1: Mutual Information Feature Selection 
        # Captures non-linear relationships, good for financial data
        mi_scores = mutual_info_classif(X_train_scaled, y_train, random_state=42)
        mi_features = pd.DataFrame({'feature': X.columns, 'mi_score': mi_scores})
        mi_features = mi_features.sort_values('mi_score', ascending=False)
        logger.info("\nTop 10 features by Mutual Information:")
        logger.info(mi_features.head(10))
        
        # Keep top 60% of features with highest MI scores
        top_mi_features = mi_features.head(int(len(mi_features) * 0.6))['feature'].values
        
        # Method 2: RandomForest Feature Importance
        initial_rf = RandomForestClassifier(n_estimators=100, random_state=42, n_jobs=-1)
        initial_rf.fit(X_train_scaled, y_train)
        rf_selector = SelectFromModel(initial_rf, threshold='median')
        rf_selector.fit(X_train_scaled, y_train)
        rf_selected_features = X.columns[rf_selector.get_support()]
        
        # Method 3: Recursive Feature Elimination with GradientBoosting
        rfe_model = GradientBoostingClassifier(n_estimators=100, random_state=42)
        rfe = RFE(estimator=rfe_model, n_features_to_select=int(X.shape[1] * 0.5), step=1)
        rfe.fit(X_train_scaled, y_train)
        rfe_selected_features = X.columns[rfe.support_]
        
        # Combine the selected features from all methods (union)
        all_selected_features = list(set(top_mi_features) | 
                                    set(rf_selected_features) | 
                                    set(rfe_selected_features))
        
        logger.info(f"\nSelected {len(all_selected_features)} features out of {X.shape[1]}:")
        logger.info(all_selected_features)
        
        # Filter to use only selected features
        X_train_selected = X_train[all_selected_features]
        X_test_selected = X_test[all_selected_features]
        
        # Re-scale with only selected features
        scaler_selected = StandardScaler()
        X_train_selected_scaled = scaler_selected.fit_transform(X_train_selected)
        X_test_selected_scaled = scaler_selected.transform(X_test_selected)
        
        # ===== MODEL TRAINING WITH SELECTED FEATURES =====
        
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
        grid_search.fit(X_train_selected_scaled, y_train)
        
        # Get best RandomForest model
        best_rf_model = grid_search.best_estimator_
        logger.info(f"Best parameters found: {grid_search.best_params_}")
        
        # Train GradientBoosting with default parameters
        models['gb'].fit(X_train_selected_scaled, y_train)
        
        # Train ExtraTrees with default parameters
        models['et'].fit(X_train_selected_scaled, y_train)
        
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
        voting_model.fit(X_train_selected_scaled, y_train)
        
        # Evaluate models on test set
        models_to_evaluate = {
            'Random Forest': best_rf_model,
            'Gradient Boosting': models['gb'],
            'Extra Trees': models['et'],
            'Voting Ensemble': voting_model
        }
        
        best_auc = 0
        best_model = None
        
        # Compare performance on both original and selected features
        logger.info("\n===== COMPARISON: ORIGINAL VS SELECTED FEATURES =====")
        
        # Evaluate on original features
        voting_model_original = VotingClassifier(
            estimators=[
                ('rf', RandomForestClassifier(**grid_search.best_params_, random_state=42)),
                ('gb', GradientBoostingClassifier(random_state=42)),
                ('et', ExtraTreesClassifier(random_state=42))
            ],
            voting='soft'
        )
        voting_model_original.fit(X_train_scaled, y_train)
        
        y_pred_original = voting_model_original.predict(X_test_scaled)
        y_pred_proba_original = voting_model_original.predict_proba(X_test_scaled)[:,1]
        
        # Original features metrics
        accuracy_original = accuracy_score(y_test, y_pred_original)
        roc_auc_original = roc_auc_score(y_test, y_pred_proba_original)
        precision_original, recall_original, _ = precision_recall_curve(y_test, y_pred_proba_original)
        pr_auc_original = auc(recall_original, precision_original)
        
        logger.info("\nOriginal Features (All Features) Performance:")
        logger.info(f"Accuracy: {accuracy_original:.4f}")
        logger.info(f"ROC AUC: {roc_auc_original:.4f}")
        logger.info(f"PR AUC: {pr_auc_original:.4f}")
        
        # Evaluate individual models on selected features
        for name, model in models_to_evaluate.items():
            # Get predictions
            y_pred = model.predict(X_test_selected_scaled)
            y_pred_proba = model.predict_proba(X_test_selected_scaled)[:,1]
            
            # Calculate metrics
            accuracy = accuracy_score(y_test, y_pred)
            roc_auc = roc_auc_score(y_test, y_pred_proba)
            
            # Calculate precision-recall AUC
            precision, recall, _ = precision_recall_curve(y_test, y_pred_proba)
            pr_auc = auc(recall, precision)
            
            logger.info(f"\n{name} Evaluation (Selected Features):")
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
            index=X_train_selected.columns,
            columns=['importance']
        ).sort_values('importance', ascending=False)
        
        logger.info("\nFeature Importances (Selected Features):\n" + str(feature_importances.head(10)))
        
        # Save model, scaler, and selected features
        model_path = os.path.join('src', 'models', 'basic_predictor.joblib')
        scaler_path = os.path.join('src', 'models', 'scaler.joblib')
        features_path = os.path.join('src', 'models', 'selected_features.joblib')
        
        joblib.dump(final_model, model_path)
        joblib.dump(scaler_selected, scaler_path)
        joblib.dump(all_selected_features, features_path)
        
        logger.info(f"Model saved to {model_path}")
        logger.info(f"Scaler saved to {scaler_path}")
        logger.info(f"Selected features saved to {features_path}")
        
        return True
        
    except Exception as e:
        logger.exception("Error in model training pipeline")
        return False

async def main(timeframe_minutes=None):
    """
    Main training pipeline.
    
    Args:
        timeframe_minutes (int, optional): Timeframe in minutes to use for training.
                                           If None, uses the default from settings.py
    """
    logger.info("Starting model training pipeline...")
    
    if timeframe_minutes is not None:
        logger.info(f"Using custom timeframe: {timeframe_minutes} minutes")
    
    # Fetch data with specified timeframe (or default if None)
    df = await fetch_training_data(timeframe_minutes=timeframe_minutes)
    if df.empty:
        logger.error("Failed to fetch training data")
        return
    
    # Get the actual timeframe used (might be from default settings)
    actual_timeframe = df.attrs.get('timeframe_minutes', timeframe_minutes)
    if actual_timeframe:
        logger.info(f"Training model with {actual_timeframe}-minute timeframe data")
    
    # Prepare features and target
    X, y = prepare_features_and_target(df)
    if X is None or y is None:
        logger.error("Failed to prepare features and target")
        return
    
    # Train and save model
    # Save timeframe info to include in model metadata
    model_metadata = {
        'timeframe_minutes': actual_timeframe,
        'data_points': len(df),
        'features': list(X.columns),
        'training_date': pd.Timestamp.now().strftime('%Y-%m-%d %H:%M:%S')
    }
    
    success = train_and_save_model(X, y)
    if success:
        # Save model metadata
        try:
            metadata_path = os.path.join('src', 'models', 'model_metadata.joblib')
            joblib.dump(model_metadata, metadata_path)
            logger.info(f"Model metadata saved to {metadata_path}")
        except Exception as e:
            logger.warning(f"Could not save model metadata: {e}")
            
        logger.info("Model training pipeline completed successfully")
    else:
        logger.error("Model training pipeline failed")

if __name__ == "__main__":
    import argparse
    
    # Set up command-line argument parser
    parser = argparse.ArgumentParser(description='Train machine learning model for trading bot')
    parser.add_argument('--timeframe', type=int, default=None, 
                        choices=[1, 5, 15, 30, 60, 120, 240, 480, 1440],
                        help='Timeframe in minutes (1, 5, 15, 30, 60 minutes, etc.)')
    parser.add_argument('--compare', action='store_true',
                        help='Train models on multiple timeframes and compare performance')
    
    args = parser.parse_args()
    
    if args.compare:
        # Train models on multiple timeframes and compare
        timeframes = [1, 5, 15, 60]  # 1min, 5min, 15min, 1hr
        logger.info(f"Training models on multiple timeframes for comparison: {timeframes}")
        
        # Dictionary to store results
        results = {}
        
        # Train a model for each timeframe
        for tf in timeframes:
            logger.info(f"\n{'='*50}\nTraining model for {tf}-minute timeframe\n{'='*50}")
            asyncio.run(main(timeframe_minutes=tf))
            
        logger.info("\nCompleted training models on all timeframes.")
    else:
        # Train on a single timeframe
        asyncio.run(main(timeframe_minutes=args.timeframe))
