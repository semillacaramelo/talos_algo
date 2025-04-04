import os
import joblib
import numpy as np
import pandas as pd
import pandas_ta as ta
from typing import Tuple, Optional

# Feature columns used by the model
FEATURE_COLUMNS = [
    'price_diff', 'ma_diff', 'rsi', 'atr',
    'STOCHk_14_3_3', 'STOCHd_14_3_3',
    'MACD_12_26_9', 'MACDh_12_26_9', 'MACDs_12_26_9'
]

def train_or_load_model() -> Tuple[Optional[object], Optional[object]]:
    model_path = os.path.join(os.path.dirname(__file__), 'basic_predictor.joblib')
    scaler_path = os.path.join(os.path.dirname(__file__), 'scaler.joblib')

    try:
        model = joblib.load(model_path)
        scaler = joblib.load(scaler_path)
        print("Successfully loaded ML model and scaler")
        return model, scaler
    except:
        print("Error loading model or scaler")
        return None, None

def engineer_features(df: pd.DataFrame) -> pd.DataFrame:
    # Price change
    df['price_diff'] = df['close'].pct_change()

    # Moving average difference
    ma_period = 20
    df['ma'] = df['close'].rolling(window=ma_period).mean()
    df['ma_diff'] = (df['close'] - df['ma']) / df['close']

    # RSI
    df['rsi'] = ta.rsi(df['close'], length=14)

    # ATR
    df['atr'] = ta.atr(df['high'], df['low'], df['close'], length=14)

    # Stochastic Oscillator
    stoch = ta.stoch(df['high'], df['low'], df['close'], k=14, d=3, append=True)
    df = pd.concat([df, stoch], axis=1)

    # MACD
    macd = ta.macd(df['close'], fast=12, slow=26, signal=9, append=True)
    df = pd.concat([df, macd], axis=1)

    # Drop NaN values after calculating all features
    df.dropna(inplace=True)

    return df

def generate_signal(df: pd.DataFrame, model_obj, scaler_obj) -> int:
    try:
        df = engineer_features(df.copy())
        if df.empty or model_obj is None or scaler_obj is None:
            return 0

        features = df[FEATURE_COLUMNS].iloc[-1:].values
        scaled_features = scaler_obj.transform(features)
        prediction = model_obj.predict(scaled_features)[0]

        return 1 if prediction == 1 else -1
    except Exception as e:
        print(f"Error generating signal: {str(e)}")
        return 0

#Retain the original function, adapting it to use the new functions.
def generate_signals_for_dataset(model_obj, scaler_obj, df):
    """Generate signals for entire dataset."""
    result_signals = pd.Series(0, index=df.index)

    if model_obj is None:
        print("ML model not loaded")
        return result_signals

    try:
        feature_df = engineer_features(df.copy())

        if feature_df.empty:
            print("Empty dataset after feature engineering")
            return result_signals

        missing_columns = [col for col in FEATURE_COLUMNS if col not in feature_df.columns]
        if missing_columns:
            print(f"Missing features: {missing_columns}")
            return result_signals

        signals = feature_df.apply(lambda row: generate_signal(pd.DataFrame([row]), model_obj, scaler_obj), axis=1)
        result_signals.update(signals)

        return result_signals

    except Exception as e:
        print(f"Error generating dataset signals: {e}")
        return result_signals