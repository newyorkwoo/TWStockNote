# Nasdaq Decline Analysis - Frontend

Vue 3 + Vite frontend for Nasdaq Composite Index decline analysis.

## Features

- 📈 Interactive K-line chart with Lightweight Charts
- 🎯 Decline period detection and visualization
- 🚨 Alert system for 10%, 15%, 20%+ declines
- 📅 Date range selector with preset options
- 📊 Real-time statistics dashboard
- 🎨 Modern UI with Tailwind CSS

## Setup

1. Install dependencies:

```bash
npm install
```

2. Run development server:

```bash
npm run dev
```

The app will be available at http://localhost:3000

3. Build for production:

```bash
npm run build
```

## Project Structure

```
src/
├── api/
│   └── nasdaq.js          # API service
├── components/
│   ├── ChartView.vue      # Lightweight Charts integration
│   ├── DateRangePicker.vue # Date range selector
│   ├── DeclineAlert.vue   # Alert display
│   └── Statistics.vue     # Statistics panel
├── App.vue                # Main application
├── main.js                # Application entry
└── style.css              # Global styles
```

## Configuration

The API base URL can be configured via environment variable:

Create `.env` file:

```
VITE_API_URL=http://localhost:8000/api
```

## Technologies

- **Vue 3**: Composition API
- **Vite**: Build tool
- **Tailwind CSS**: Utility-first CSS
- **Lightweight Charts**: Financial charting
- **Axios**: HTTP client
