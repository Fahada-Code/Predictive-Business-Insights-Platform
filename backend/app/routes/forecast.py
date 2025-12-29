from fastapi import APIRouter, HTTPException, Query, UploadFile, File
from app.utils.forecasting import generate_forecast
import os
import shutil
import pandas as pd
import io
from typing import Optional

router = APIRouter()

# Data directory path
DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "data")
os.makedirs(DATA_DIR, exist_ok=True)

def normalize_columns(df: pd.DataFrame) -> pd.DataFrame:
    """
    Standardize column names to 'ds' and 'y' using smart detection.
    """
    # 1. Detect Date Column
    date_col = None
    if 'ds' in df.columns:
        date_col = 'ds'
    else:
        # Case-insensitive search for 'date' or 'ds' or 'timestamp'
        for col in df.columns:
            if col.lower() in ['date', 'ds', 'timestamp', 'time']:
                date_col = col
                break
    
    if not date_col:
        raise ValueError("Could not detect a date column (looking for 'ds', 'date', 'timestamp').")

    # 2. Detect Target Column
    target_col = None
    if 'y' in df.columns:
        target_col = 'y'
    else:
        # Potential targets (excluding date column)
        potential_targets = [c for c in df.columns if c != date_col]
        
        # Check for explicit 'y' match first
        for col in potential_targets:
            if col.lower() == 'y':
                target_col = col
                break
        
        if not target_col:
            # Check for generic value names
            common_names = ['value', 'sales', 'revenue', 'quantity', 'amount', 'close', 'price']
            for col in potential_targets:
                if col.lower() in common_names:
                    target_col = col
                    break
            
            # If still not found, pick the first numeric column
            if not target_col:
                numeric_cols = df[potential_targets].select_dtypes(include=['number', 'float', 'int']).columns
                if len(numeric_cols) > 0:
                    target_col = numeric_cols[0]

    if not target_col:
        raise ValueError("Could not detect a numeric target column. Please ensure one exists.")

    # 3. Rename and Filter
    df = df.rename(columns={date_col: 'ds', target_col: 'y'})
    
    # Ensure y is numeric
    df['y'] = pd.to_numeric(df['y'], errors='coerce')
    df = df.dropna(subset=['y'])
    
    return df[['ds', 'y']]

@router.post("/forecast", tags=["Forecasting"])
async def get_forecast(
    file: UploadFile = File(...),
    days: int = Query(30, description="Number of days to forecast"),
    seasonality_mode: str = Query('additive', enum=['additive', 'multiplicative']),
    growth: str = Query('linear', enum=['linear', 'flat']),
    daily_seasonality: bool = False,
    weekly_seasonality: bool = False,
    yearly_seasonality: bool = False
):
    """
    Generate a forecast using the Prophet model based on uploaded CSV data.
    """
    # Read file content
    contents = await file.read()
    
    try:
        # Try reading as CSV
        df = pd.read_csv(io.BytesIO(contents))
    except Exception:
        # Try with different encoding if default fails
        try:
            df = pd.read_csv(io.BytesIO(contents), encoding='latin1')
        except Exception as e:
            raise HTTPException(status_code=400, detail="Invalid CSV file. Could not parse.")

    # Normalize columns
    try:
        df = normalize_columns(df)
    except ValueError as e:
         raise HTTPException(status_code=400, detail=str(e))

    # Save the standardized file
    # We save it so the utility can read it (or we could modify utility to accept DF)
    # Keeping the utility expecting a path for now to minimize refactoring risk elsewhere
    file_location = os.path.join(DATA_DIR, f"clean_{file.filename}")
    df.to_csv(file_location, index=False)

    try:
        # Generate forecast
        forecast_df = generate_forecast(
            file_path=file_location,
            days=days,
            seasonality_mode=seasonality_mode,
            growth=growth,
            daily_seasonality=daily_seasonality,
            weekly_seasonality=weekly_seasonality,
            yearly_seasonality=yearly_seasonality
        )
        
        # Return results
        result = forecast_df.tail(days).to_dict(orient="records")
        
        return {
            "message": f"Forecast generated successfully. Processed {len(df)} historical rows.",
            "row_count": len(df),
            "parameters": {
                "seasonality_mode": seasonality_mode,
                "growth": growth,
            },
            "data": result
        }
    except ValueError as ve:
        raise HTTPException(status_code=400, detail=str(ve))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Forecasting error: {str(e)}")
