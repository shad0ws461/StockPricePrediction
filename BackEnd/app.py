from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import pandas as pd
from data_handler import fetch_historical_data
from ml_service import generate_forecast
from fastapi.middleware.cors import CORSMiddleware

# Initialize the FastAPI application
app = FastAPI(
    title="Stock Forecast API",
    description="API for real-time stock price forecasting using an ML model."
)

# 1. CORS Middleware - Isse browser aapka request block nahi karega
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ✅ HOME ROUTE (Testing ke liye)
@app.get("/")
def home():
    return {"message": "Stock Prediction API is running!"}

# Data Structure for Request
class PredictionRequest(BaseModel):
    ticker: str
    days: int

# --- API Endpoint ---
@app.post("/api/predict")
async def predict_stock_price(request: PredictionRequest):
    ticker = request.ticker.upper()
    days = request.days

    # 1. Validation
    if not (1 <= days <= 30):
        raise HTTPException(
            status_code=400,
            detail="Forecast days must be between 1 and 30."
        )

    # 2. Fetch Historical Data (Corrected Argument Name)
    # Hum pichle 365 din ka data le rahe hain analysis ke liye
    historical_df = fetch_historical_data(ticker, days_to_look_back=365) 

    if historical_df is None or historical_df.empty:
        raise HTTPException(
            status_code=404,
            detail=f"Could not retrieve data for ticker: {ticker}. Use formats like AAPL or RELIANCE.NS"
        )

    # 3. Generate Forecast using the ML Model
    try:
        # ml_service.py ab 'Date' aur 'Price' keys return karega
        forecast_data = generate_forecast(historical_df, days)
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Model prediction failed: {str(e)}"
        )

    # 4. Data Preparation for Frontend
    if historical_df.index.name == 'Date' or 'Date' not in historical_df.columns:
        historical_df = historical_df.reset_index()
    
    # Date formatting (JSON compatible)
    historical_df['Date'] = pd.to_datetime(historical_df['Date']).dt.strftime('%Y-%m-%d')
    historical_records = historical_df.to_dict(orient='records')

    # 5. Final Response
    return {
        "status": "success",
        "ticker": ticker,
        "historical_data": historical_records,
        "forecast_data": forecast_data
    }