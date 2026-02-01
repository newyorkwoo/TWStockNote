"""
FastAPI application for Nasdaq Decline Analysis System
"""
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZipMiddleware
from datetime import datetime
from typing import Optional
from models import (
    HistoricalDataResponse,
    DeclinePeriodsResponse,
    LatestDataResponse
)
from data_service import NasdaqDataService

app = FastAPI(
    title="Nasdaq Decline Analysis API",
    description="API for analyzing Nasdaq Composite Index decline periods",
    version="1.0.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify exact origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Add GZip compression for faster data transfer
app.add_middleware(GZipMiddleware, minimum_size=1000)

# Initialize data service
data_service = NasdaqDataService()


@app.on_event("startup")
async def startup_event():
    """Initialize data on startup"""
    print("Starting Nasdaq Decline Analysis API...")
    # Download data if cache is empty
    if not data_service.data_cache:
        try:
            await data_service.download_data()
        except Exception as e:
            print(f"Warning: Could not download initial data: {e}")


@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "Nasdaq Decline Analysis API",
        "version": "1.0.0",
        "endpoints": {
            "historical_data": "/api/nasdaq/historical",
            "decline_periods": "/api/nasdaq/declines",
            "latest_data": "/api/nasdaq/latest",
            "update_data": "/api/nasdaq/update"
        }
    }


@app.get("/api/nasdaq/historical", response_model=HistoricalDataResponse)
async def get_historical_data(
    start_date: Optional[str] = None,
    end_date: Optional[str] = None
):
    """
    Get historical Nasdaq data
    
    Args:
        start_date: Start date in YYYY-MM-DD format (optional)
        end_date: End date in YYYY-MM-DD format (optional)
    
    Returns:
        Historical data with total count
    """
    try:
        data = await data_service.get_historical_data(start_date, end_date)
        return HistoricalDataResponse(
            data=data,
            total_count=len(data)
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/nasdaq/declines", response_model=DeclinePeriodsResponse)
async def get_decline_periods(
    start_date: Optional[str] = None,
    end_date: Optional[str] = None,
    threshold: float = 0.10
):
    """
    Get decline periods with >threshold% drop
    
    Args:
        start_date: Start date in YYYY-MM-DD format (optional)
        end_date: End date in YYYY-MM-DD format (optional)
        threshold: Minimum decline percentage (default: 0.10 = 10%)
    
    Returns:
        List of decline periods with total count
    """
    try:
        # Get historical data (with optimized binary search filtering)
        data = await data_service.get_historical_data(start_date, end_date)
        
        # Create cache key for decline periods
        cache_key = f"{start_date}_{end_date}_{threshold}"
        
        # Check cache
        if not hasattr(data_service, '_decline_cache'):
            data_service._decline_cache = {}
        
        if cache_key in data_service._decline_cache:
            periods = data_service._decline_cache[cache_key]
        else:
            # Detect decline periods
            periods = data_service.detect_decline_periods(data, threshold)
            
            # Cache result
            data_service._decline_cache[cache_key] = periods
            
            # Limit cache size
            if len(data_service._decline_cache) > 100:
                keys = list(data_service._decline_cache.keys())
                for key in keys[:50]:
                    del data_service._decline_cache[key]
        
        return DeclinePeriodsResponse(
            periods=periods,
            total_count=len(periods)
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/nasdaq/latest", response_model=LatestDataResponse)
async def get_latest_data():
    """
    Get the most recent data point and current decline status
    
    Returns:
        Latest data point and current decline period (if any)
    """
    try:
        latest = await data_service.get_latest_data()
        
        if not latest:
            raise HTTPException(status_code=404, detail="No data available")
        
        # Check if currently in a decline period
        all_data = await data_service.get_historical_data()
        decline_periods = data_service.detect_decline_periods(all_data)
        
        current_decline = None
        if decline_periods and decline_periods[-1].is_ongoing:
            current_decline = decline_periods[-1]
        
        return LatestDataResponse(
            latest=latest,
            current_decline=current_decline
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/nasdaq/update")
async def update_data():
    """
    Trigger data update (download latest data from Yahoo Finance)
    
    Returns:
        Update status and number of records updated
    """
    try:
        # Download data from the last cached date to today
        data = await data_service.download_data()
        
        return {
            "status": "success",
            "message": "Data updated successfully",
            "records_count": len(data),
            "last_date": data[-1].date.isoformat() if data else None
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
