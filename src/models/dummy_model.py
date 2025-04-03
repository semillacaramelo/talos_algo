import joblib
import os
from sklearn.linear_model import LogisticRegression
import numpy as np # Import numpy for consistent data types

# Create a dummy model
dummy_model = LogisticRegression()

# --- FIX: Provide dummy data with BOTH classes (0 and 1) ---
# Dummy features (X): Need at least one sample per class
dummy_X = np.array([[0, 0], [1, 1]]) 
# Dummy labels (y): Corresponding labels for each sample
dummy_y = np.array([0, 1]) 
# ---------------------------------------------------------

# Fit with the corrected dummy data
dummy_model.fit(dummy_X, dummy_y)

# Ensure directory exists
model_dir = os.path.join('src', 'models')
os.makedirs(model_dir, exist_ok=True)
model_path = os.path.join(model_dir, 'basic_predictor.joblib')

# Save the dummy model
joblib.dump(dummy_model, model_path)
print(f"Dummy model saved to {model_path}")