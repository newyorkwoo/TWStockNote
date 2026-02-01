"""
Data service for downloading and managing Nasdaq data
"""
import yfinance as yf
import pandas as pd
from datetime import datetime, timedelta
from typing import List, Optional, Tuple
from models import NasdaqDaily, DeclinePeriod
import json
import os
from functools import lru_cache
import numpy as np


class NasdaqDataService:
    """Service for managing Nasdaq Composite Index data"""
    
    def __init__(self, data_file: str = "nasdaq_data.json"):
        self.ticker = "^IXIC"  # Nasdaq Composite Index
        self.data_file = data_file
        self.data_cache: List[NasdaqDaily] = []
        self._decline_cache = {}  # Cache for decline periods
        self._load_cache()
    
    def _load_cache(self):
        """Load cached data from file"""
        if os.path.exists(self.data_file):
            try:
                with open(self.data_file, 'r') as f:
                    data = json.load(f)
                    self.data_cache = [NasdaqDaily(**item) for item in data]
                print(f"Loaded {len(self.data_cache)} records from cache")
            except Exception as e:
                print(f"Error loading cache: {e}")
                self.data_cache = []
    
    def _save_cache(self):
        """Save data to cache file"""
        try:
            with open(self.data_file, 'w') as f:
                data = [item.model_dump(mode='json') for item in self.data_cache]
                json.dump(data, f, default=str)
            print(f"Saved {len(self.data_cache)} records to cache")
        except Exception as e:
            print(f"Error saving cache: {e}")
    
    async def download_data(
        self, 
        start_date: Optional[str] = None, 
        end_date: Optional[str] = None
    ) -> List[NasdaqDaily]:
        """
        Download Nasdaq data from Yahoo Finance
        
        Args:
            start_date: Start date in YYYY-MM-DD format (default: 2000-01-01)
            end_date: End date in YYYY-MM-DD format (default: today)
        
        Returns:
            List of NasdaqDaily objects
        """
        if not start_date:
            start_date = "2000-01-01"
        if not end_date:
            end_date = datetime.now().strftime("%Y-%m-%d")
        
        print(f"Downloading Nasdaq data from {start_date} to {end_date}")
        
        try:
            ticker = yf.Ticker(self.ticker)
            df = ticker.history(start=start_date, end=end_date)
            
            data_list: List[NasdaqDaily] = []
            
            for index, row in df.iterrows():
                data_list.append(NasdaqDaily(
                    date=index.to_pydatetime(),
                    open=float(row['Open']),
                    high=float(row['High']),
                    low=float(row['Low']),
                    close=float(row['Close']),
                    volume=int(row['Volume'])
                ))
            
            # Update cache
            self.data_cache = data_list
            self._save_cache()
            
            print(f"Downloaded {len(data_list)} records")
            return data_list
            
        except Exception as e:
            print(f"Error downloading data: {e}")
            raise
    
    async def get_historical_data(
        self,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None
    ) -> List[NasdaqDaily]:
        """Get historical data from cache or download if needed"""
        
        # If cache is empty, download all data
        if not self.data_cache:
            return await self.download_data(start_date, end_date)
        
        # Use binary search for efficient date filtering (cache is sorted by date)
        filtered_data = self.data_cache
        
        if start_date or end_date:
            start_idx = 0
            end_idx = len(self.data_cache)
            
            if start_date:
                start_dt = datetime.fromisoformat(start_date).replace(tzinfo=None)
                # Binary search for start index
                left, right = 0, len(self.data_cache)
                while left < right:
                    mid = (left + right) // 2
                    if self.data_cache[mid].date.replace(tzinfo=None) < start_dt:
                        left = mid + 1
                    else:
                        right = mid
                start_idx = left
            
            if end_date:
                end_dt = datetime.fromisoformat(end_date).replace(tzinfo=None)
                # Binary search for end index
                left, right = start_idx, len(self.data_cache)
                while left < right:
                    mid = (left + right) // 2
                    if self.data_cache[mid].date.replace(tzinfo=None) <= end_dt:
                        left = mid + 1
                    else:
                        right = mid
                end_idx = left
            
            filtered_data = self.data_cache[start_idx:end_idx]
        
        return filtered_data
    
    async def get_latest_data(self) -> Optional[NasdaqDaily]:
        """Get the most recent data point"""
        if not self.data_cache:
            data = await self.download_data()
            return data[-1] if data else None
        
        return self.data_cache[-1]
    
    def detect_decline_periods(
        self, 
        data: List[NasdaqDaily],
        threshold: float = 0.10,
        recovery_from_trough_threshold: float = 0.20
    ) -> List[DeclinePeriod]:
        """
        Detect decline periods (local peak-to-trough with >threshold% drop)
        
        end_date is the TROUGH DATE (lowest point before significant recovery)
        
        Algorithm:
        1. Track rolling maximum (local peak)
        2. When price drops >threshold% from local peak, start tracking decline
        3. Track the lowest trough during decline
        4. When price recovers >recovery_from_trough_threshold from trough, end the decline
        5. The period recorded is from peak_date to trough_date (not recovery date)
        
        This approach identifies each significant decline independently, rather than 
        waiting for recovery to historical peaks, which allows capturing multiple 
        decline periods even when overall market hasn't fully recovered.
        
        Args:
            data: List of NasdaqDaily objects
            threshold: Minimum decline percentage to start tracking (default: 0.10 = 10%)
            recovery_from_trough_threshold: Recovery from trough to end tracking (default: 0.20 = 20%)
        
        Returns:
            List of DeclinePeriod objects where end_date = trough date
        """
        if not data:
            return []
        
        # Use NumPy for faster numerical operations
        prices = np.array([d.close for d in data])
        
        decline_periods: List[DeclinePeriod] = []
        current_peak = data[0].close
        peak_date = data[0].date
        in_decline = False
        decline_start_peak = 0.0
        decline_start_date = None
        lowest_trough = float('inf')
        trough_date = None
        
        for point in data:
            price = point.close
            
            if in_decline:
                # Track the lowest trough
                if price < lowest_trough:
                    lowest_trough = price
                    trough_date = point.date
                
                # Check if recovered significantly from trough (not from peak)
                recovery_from_trough = (price - lowest_trough) / lowest_trough
                
                if recovery_from_trough >= recovery_from_trough_threshold:
                    # Significant recovery from trough - save the decline period (peak to trough)
                    decline_pct = ((decline_start_peak - lowest_trough) / decline_start_peak) * 100
                    
                    # Calculate alert levels
                    alert_levels = []
                    for level in range(10, int(decline_pct) + 1, 5):
                        alert_levels.append(float(level))
                    
                    decline_periods.append(DeclinePeriod(
                        start_date=decline_start_date,
                        end_date=trough_date,  # End date is TROUGH date, not recovery date
                        peak_value=decline_start_peak,
                        trough_value=lowest_trough,
                        decline_percentage=decline_pct,
                        alert_levels=alert_levels,
                        is_ongoing=False
                    ))
                    
                    # Reset and start tracking new peak from current price
                    in_decline = False
                    current_peak = price
                    peak_date = point.date
                    continue
            
            # Update peak if new high (when not in decline)
            if not in_decline and price > current_peak:
                current_peak = price
                peak_date = point.date
            
            # Check if we should enter decline phase
            drawdown = (current_peak - price) / current_peak
            if not in_decline and drawdown >= threshold:
                # Start tracking decline
                in_decline = True
                decline_start_peak = current_peak
                decline_start_date = peak_date
                lowest_trough = price
                trough_date = point.date
        
        # Add ongoing decline if exists
        if in_decline:
            decline_pct = ((decline_start_peak - lowest_trough) / decline_start_peak) * 100
            alert_levels = []
            for level in range(10, int(decline_pct) + 1, 5):
                alert_levels.append(float(level))
            
            decline_periods.append(DeclinePeriod(
                start_date=decline_start_date,
                end_date=trough_date,  # End date is TROUGH date
                peak_value=decline_start_peak,
                trough_value=lowest_trough,
                decline_percentage=decline_pct,
                alert_levels=alert_levels,
                is_ongoing=True
            ))
        
        return decline_periods
