# Nasdaq Decline Analysis Backend

FastAPI backend for analyzing Nasdaq Composite Index decline periods.

## Setup

1. Create virtual environment:

```bash
python -m venv venv
source venv/bin/activate  # On macOS/Linux
# or
venv\Scripts\activate  # On Windows
```

2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Run the server:

```bash
python main.py
# or
uvicorn main:app --reload
```

The API will be available at http://localhost:8000

## API Documentation

Once the server is running, visit:

- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## API Endpoints

### GET /api/nasdaq/historical

Get historical Nasdaq data with optional date range filtering.

Query Parameters:

- `start_date` (optional): Start date in YYYY-MM-DD format
- `end_date` (optional): End date in YYYY-MM-DD format

### GET /api/nasdaq/declines

Get decline periods (peak-to-trough) with >10% drop.

Query Parameters:

- `start_date` (optional): Start date in YYYY-MM-DD format
- `end_date` (optional): End date in YYYY-MM-DD format
- `threshold` (optional): Minimum decline percentage (default: 0.10)

### GET /api/nasdaq/latest

Get the most recent data point and current decline status.

### POST /api/nasdaq/update

Trigger data update (download latest data from Yahoo Finance).

## Data Model

### NasdaqDaily

- `date`: datetime
- `open`: float
- `high`: float
- `low`: float
- `close`: float
- `volume`: int

### DeclinePeriod

- `start_date`: datetime (peak date)
- `end_date`: datetime (trough date, None if ongoing)
- `peak_value`: float
- `trough_value`: float
- `decline_percentage`: float
- `alert_levels`: List[float] (e.g., [10, 15, 20])
- `is_ongoing`: bool
