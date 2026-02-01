"""
Data models for Nasdaq Decline Analysis System
"""
from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, Field


class NasdaqDaily(BaseModel):
    """Daily Nasdaq Composite Index data"""
    date: datetime
    open: float
    high: float
    low: float
    close: float
    volume: int
    
    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }


class DeclinePeriod(BaseModel):
    """Represents a decline period (peak to trough)"""
    start_date: datetime  # Peak date
    end_date: Optional[datetime] = None  # Trough date (None if ongoing)
    peak_value: float
    trough_value: Optional[float] = None
    decline_percentage: float
    alert_levels: List[float] = Field(default_factory=list)  # [10, 15, 20, ...]
    is_ongoing: bool = True
    
    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }


class HistoricalDataRequest(BaseModel):
    """Request model for historical data"""
    start_date: Optional[str] = None
    end_date: Optional[str] = None


class HistoricalDataResponse(BaseModel):
    """Response model for historical data"""
    data: List[NasdaqDaily]
    total_count: int


class DeclinePeriodsResponse(BaseModel):
    """Response model for decline periods"""
    periods: List[DeclinePeriod]
    total_count: int


class LatestDataResponse(BaseModel):
    """Response model for latest data point"""
    latest: NasdaqDaily
    current_decline: Optional[DeclinePeriod] = None
