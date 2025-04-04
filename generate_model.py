#!/usr/bin/env python3
"""
Utility script to generate a compatible machine learning model.
This will create a new model using the current numpy/scikit-learn versions.
"""

from src.models.dummy_model import create_dummy_model

if __name__ == "__main__":
    print("Creating new compatible machine learning model and scaler...")
    model, scaler = create_dummy_model()
    print("Done! The model and scaler have been saved to the src/models directory.")