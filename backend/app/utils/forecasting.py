import pandas as pd
from prophet import Prophet
import os
from typing import Optional

def generate_forecast(
    file_path: str,
    days: int = 30,
    seasonality_mode: str = 'additive',
    growth: str = 'linear',
    daily_seasonality: bool = False,
    weekly_seasonality: bool = False,
    yearly_seasonality: bool = False,
    holidays: Optional[pd.DataFrame] = None
) -> pd.DataFrame:
    """
    Loads time-series data from a CSV file, trains a Prophet model with custom settings,
    and forecasts the next N days.
    """
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Data file not found at {file_path}")

    # Load data
    try:
        df = pd.read_csv(file_path)
    except Exception as e:
        raise ValueError(f"Failed to read CSV: {str(e)}")
    
    # Ensure required columns exist
    if 'ds' not in df.columns or 'y' not in df.columns:
        raise ValueError("CSV must contain 'ds' (date) and 'y' (value) columns.")

    # Convert ds to datetime
    try:
        df['ds'] = pd.to_datetime(df['ds'])
    except Exception:
        raise ValueError("Could not parse 'ds' column as dates.")
        
    if df['ds'].dt.tz is not None:
        df['ds'] = df['ds'].dt.tz_localize(None)

    # Initialize Prophet model with custom parameters
    m = Prophet(
        seasonality_mode=seasonality_mode,
        growth=growth,
        daily_seasonality=daily_seasonality,
        weekly_seasonality=weekly_seasonality,
        yearly_seasonality=yearly_seasonality,
        holidays=holidays
    )
    
    m.fit(df)

    # Create future dataframe
    future = m.make_future_dataframe(periods=days)

    # Forecast
    forecast = m.predict(future)

    # Return relevant columns
    return forecast[['ds', 'yhat', 'yhat_lower', 'yhat_upper']]
