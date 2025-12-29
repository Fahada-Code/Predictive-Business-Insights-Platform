from fastapi import APIRouter, HTTPException, Query, UploadFile, File
from app.utils.forecasting import generate_forecast
import os
import shutil
from typing import Optional

router = APIRouter()

# Data directory path
DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "data")
os.makedirs(DATA_DIR, exist_ok=True)

@router.post("/forecast", tags=["Forecasting"])
async def get_forecast(
    file: UploadFile = File(...),
    days: int = Query(30, description="Number of days to forecast"),
    seasonality_mode: str = Query('additive', enum=['additive', 'multiplicative']),
    growth: str = Query('linear', enum=['linear', 'flat']), # 'logistic' requires saturation columns, sticking to simpler ones for now unless requested
    daily_seasonality: bool = False,
    weekly_seasonality: bool = False,
    yearly_seasonality: bool = False
):
    """
    Generate a forecast using the Prophet model based on uploaded CSV data.
    """
    if not file.filename.endswith('.csv') and not file.filename.endswith('.txt'):
        raise HTTPException(status_code=400, detail="Invalid file type. Please upload a CSV file.")

    # Save the uploaded file
    file_location = os.path.join(DATA_DIR, f"uploaded_{file.filename}")
    try:
        with open(file_location, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to save file: {str(e)}")

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
            "message": f"Forecast generated for next {days} days",
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
