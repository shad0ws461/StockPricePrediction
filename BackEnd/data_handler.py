import yfinance as yf
import pandas as pd
from datetime import datetime, timedelta

def fetch_historical_data(ticker: str, days_to_look_back: int = 365) -> pd.DataFrame:
    try:
        end_date = (datetime.now() + timedelta(days=1)).strftime('%Y-%m-%d')
        start_date = (datetime.now() - timedelta(days=days_to_look_back)).strftime('%Y-%m-%d')
        
        # 1. Download data with auto_adjust=True
        data = yf.download(ticker, start=start_date, end=end_date, progress=False, auto_adjust=True)

        if data.empty:
            raise ValueError(f"No data found for: {ticker}")

        # 2. Fix for Multi-index columns (Naye yfinance versions mein hota hai)
        if isinstance(data.columns, pd.MultiIndex):
            data.columns = data.columns.get_level_values(0)

        # 3. Handle 'Close' name variation
        # Naye versions mein auto_adjust se 'Close' aksar sirf 'Close' hi rehta hai
        if 'Close' not in data.columns:
            # Agar 'Close' nahi mila toh pehla column try karein (aksar wahi price hota hai)
            data.rename(columns={data.columns[0]: 'Close'}, inplace=True)

        data.dropna(inplace=True) 
        data = data.reset_index()
        
        # 4. 'Date' column ensure karein
        if 'Date' not in data.columns:
            data.rename(columns={data.index.name: 'Date'}, inplace=True)

        # Sirf zaroori data return karein
        return data[['Date', 'Close']]

    except Exception as e:
        print(f"Data Fetch Error: {e}")
        return None