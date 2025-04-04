import numpy as np
import pandas as pd
import joblib
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler

# Create a simple dummy model and scaler for initial setup
def create_dummy_model():
    # Create a simple model that always predicts 0 (no trade)
    model = RandomForestClassifier(n_estimators=10, random_state=42)
    
    # Create some dummy training data with the expected features
    X = np.random.rand(100, 8)  # 8 features
    y = np.zeros(100)  # All 0 predictions
    
    # Fit the model
    model.fit(X, y)
    
    # Create and fit a scaler
    scaler = StandardScaler()
    scaler.fit(X)
    
    # Save both objects
    joblib.dump(model, 'src/models/basic_predictor.joblib')
    joblib.dump(scaler, 'src/models/scaler.joblib')
    
    print("Created and saved dummy model and scaler")
    
    return model, scaler

if __name__ == "__main__":
    create_dummy_model()