import numpy as np
import pandas as pd
import joblib
import os
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler

# Create a simple dummy model and scaler for initial setup
def create_dummy_model():
    """Create a simple model for testing with current numpy version."""
    # Create a simple model that alternates between BUY/SELL for testing
    model = RandomForestClassifier(n_estimators=10, random_state=42)
    
    # Create some dummy training data with features from FEATURE_COLUMNS
    # Must match: 'price_change', 'ma_diff', 'rsi', 'atr', 'stoch_k', 'stoch_d', 'macd', 'macd_signal'
    X = np.random.rand(100, 8)  # 8 features from our FEATURE_COLUMNS
    
    # Use random predictions (0=SELL, 1=BUY) for testing purposes
    y = np.random.randint(0, 2, 100)  
    
    # Fit the model
    model.fit(X, y)
    
    # Create and fit a scaler
    scaler = StandardScaler()
    scaler.fit(X)
    
    # Get the directory of this file to save model in the models directory
    models_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Save both objects with relative paths
    model_path = os.path.join(models_dir, 'basic_predictor.joblib')
    scaler_path = os.path.join(models_dir, 'scaler.joblib')
    
    try:
        joblib.dump(model, model_path)
        joblib.dump(scaler, scaler_path)
        print(f"Created and saved dummy model to {model_path}")
        print(f"Created and saved dummy scaler to {scaler_path}")
    except Exception as e:
        print(f"Error saving dummy model: {e}")
    
    return model, scaler

if __name__ == "__main__":
    create_dummy_model()