import pandas as pd
import numpy as np
import joblib 
from datetime import datetime, timedelta
import os

# Define file paths
MODEL_PATH = 'models/stock_model.h5'
SCALER_PATH = 'models/scaler.pkl'
SEQUENCE_LENGTH = 60 

def load_ml_assets():
    """Loads the pre-trained model and scaler."""
    try:
        # Note: In production, uncomment the real loading lines
        # if os.path.exists(MODEL_PATH) and os.path.exists(SCALER_PATH):
        #     model = joblib.load(MODEL_PATH)
        #     scaler = joblib.load(SCALER_PATH)
        #     return model, scaler
        
        print(f"Placeholder: Model assets logic initialized.")
        return "MODEL_PLACEHOLDER", "SCALER_PLACEHOLDER"
    except Exception as e:
        print(f"Error loading ML assets: {e}")
        return None, None

# Load assets when the module starts
MODEL, SCALER = load_ml_assets()

def generate_forecast(historical_df: pd.DataFrame, days_to_forecast: int):
    """
    Generates a stock price forecast.
    """
    if MODEL is None or SCALER is None:
        raise Exception("ML model assets failed to load.")

    # --- 1. Preprocessing ---
    # Hum ensure karte hain ki last close price numeric ho
    last_close = float(historical_df['Close'].iloc[-1])
    
    # Date formatting handle karna
    last_date_str = historical_df['Date'].iloc[-1]
    if isinstance(last_date_str, str):
        current_date = datetime.strptime(last_date_str, '%Y-%m-%d').date()
    else:
        current_date = last_date_str.date()
    
    # --- 2. Prediction Loop ---
    forecast_results = []
    
    for i in range(1, days_to_forecast + 1):
        future_date = current_date + timedelta(days=i)
        
        # Random Walk Logic (Jab tak real model replace nahi hota)
        # 0.02 means 2% tak ka fluctuation
        prediction = last_close * (1 + (np.random.rand() - 0.5) * 0.02)
        last_close = prediction 
        
        # Frontend expect kar raha hai: 'Date' aur 'Price' (Capital Letters)
        forecast_results.append({
            "Date": future_date.strftime('%Y-%m-%d'),
            "Price": round(float(prediction), 2)
        })

    return forecast_results