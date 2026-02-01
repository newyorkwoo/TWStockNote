# Nasdaq Composite Index Decline Analysis System - AI Agent Skills

## Project Overview
A full-stack application for analyzing and visualizing Nasdaq Composite Index decline periods from 2000 to present. The system identifies decline phases (peak-to-trough), alerts on declines >10%, and provides additional alerts for every subsequent 5% drop.

## Tech Stack
- **Frontend**: Vue 3 + Vite + JavaScript + Tailwind CSS + Lightweight Charts
- **Backend**: Python + FastAPI
- **Data Source**: yfinance (Yahoo Finance API)
- **Database**: SQLite or PostgreSQL (for storing historical data)

## Core Features
1. Daily automatic data download from yfinance
2. Decline phase detection (>10% from peak to trough)
3. K-line chart visualization with decline period highlighting
4. Alert system (10%, 15%, 20%, etc.)
5. Date range selector for historical data filtering

## Agent Skills & Guidelines

### 1. Python Backend Development
**Skill: Data Collection & Processing**
- Use `yfinance` to download Nasdaq Composite Index (^IXIC) data
- Implement daily scheduled data updates
- Store historical data with proper timestamps
- Calculate rolling highs to identify peaks
- Detect decline phases (peak-to-trough) with >10% drop threshold

**Skill: API Development**
- Create FastAPI endpoints:
  - `GET /api/nasdaq/historical?start_date&end_date` - Get historical data
  - `GET /api/nasdaq/declines?start_date&end_date` - Get decline periods
  - `GET /api/nasdaq/latest` - Get latest data point
  - `POST /api/nasdaq/update` - Trigger data update
- Implement CORS for frontend communication
- Add request validation and error handling

**Skill: Decline Analysis Algorithm**
```python
# Key logic for decline detection:
# 1. Track rolling maximum (peak)
# 2. Calculate current drawdown from peak
# 3. If drawdown > 10%, mark as decline phase
# 4. Track alert thresholds (10%, 15%, 20%, etc.)
# 5. Identify trough (local minimum before recovery)
```

### 2. Frontend Development
**Skill: Vue 3 Component Structure**
- `App.vue` - Main application container
- `ChartView.vue` - Lightweight Charts integration
- `DateRangePicker.vue` - Date selection component
- `DeclineAlert.vue` - Alert display component
- `Statistics.vue` - Summary statistics panel

**Skill: Lightweight Charts Integration**
- Initialize candlestick series for K-line display
- Add price markers for peak/trough points
- Highlight decline periods with background shading
- Implement custom price lines for alert thresholds
- Add tooltips showing decline percentage

**Skill: State Management**
- Use Vue 3 Composition API with `ref`, `reactive`, `computed`
- Manage chart data state
- Handle date range selection state
- Track current decline alerts

**Skill: API Integration**
```javascript
// Fetch data pattern:
const fetchNasdaqData = async (startDate, endDate) => {
  const response = await fetch(
    `/api/nasdaq/historical?start_date=${startDate}&end_date=${endDate}`
  );
  return response.json();
};
```

### 3. Data Visualization
**Skill: Chart Configuration**
- Configure candlestick colors (red for down, green for up)
- Add volume histogram below main chart
- Set up time scale with proper formatting
- Implement zoom and pan functionality
- Add crosshair for data inspection

**Skill: Decline Period Marking**
```javascript
// Add rectangular background for decline periods
chart.addAreaSeries({
  topColor: 'rgba(255, 82, 82, 0.2)',
  bottomColor: 'rgba(255, 82, 82, 0.1)',
  lineColor: 'rgba(255, 82, 82, 0.8)',
  lineWidth: 2,
});
```

### 4. Alert System
**Skill: Alert Logic**
- Monitor real-time price changes
- Compare against peak values
- Trigger alerts at threshold crossings (10%, 15%, 20%, 25%, etc.)
- Display alert notifications with sound/visual indicators
- Log alert history

### 5. Data Model
**Python Models:**
```python
class NasdaqDaily:
    date: datetime
    open: float
    high: float
    low: float
    close: float
    volume: int

class DeclinePeriod:
    start_date: datetime  # Peak date
    end_date: datetime    # Trough date
    peak_value: float
    trough_value: float
    decline_percentage: float
    alert_levels: List[float]  # [10, 15, 20, ...]
```

### 6. Code Style Guidelines
**Python:**
- Use type hints
- Follow PEP 8
- Use async/await for I/O operations
- Add docstrings for functions
- Use Pydantic for data validation

**JavaScript/Vue:**
- Use ESLint with Vue 3 recommended rules
- Prefer Composition API over Options API
- Use `const` for immutable values
- Add JSDoc comments for complex functions
- Follow Vue 3 style guide

**Tailwind CSS:**
- Use utility classes
- Create custom components for repeated patterns
- Use responsive design classes (sm:, md:, lg:)
- Maintain consistent spacing scale

### 7. File Structure
