# Nasdaq Composite Index Decline Analysis System

完整的 Nasdaq 指數下跌分析系統，用於追蹤和視覺化 Nasdaq Composite Index 從 2000 年至今的下跌期間。

## 功能特色

- 📊 **自動資料收集**: 每日從 Yahoo Finance 下載最新數據
- 📉 **下跌期間檢測**: 自動識別 >10% 的峰值到谷底下跌
- 📈 **K線圖視覺化**: 使用 Lightweight Charts 顯示互動式圖表
- 🚨 **警報系統**: 在下跌 10%, 15%, 20% 等時觸發警報
- 📅 **日期範圍選擇器**: 靈活的歷史資料篩選
- 💹 **即時統計**: 顯示最新價格、當日變化和當前狀態

## 技術架構

### 前端

- **框架**: Vue 3 + Vite
- **語言**: JavaScript
- **樣式**: Tailwind CSS
- **圖表**: Lightweight Charts
- **HTTP 客戶端**: Axios

### 後端

- **框架**: Python + FastAPI
- **資料源**: yfinance (Yahoo Finance API)
- **資料庫**: JSON 檔案 (可擴展至 SQLite/PostgreSQL)
- **非同步**: async/await

## 快速開始

### 前置需求

- Python 3.8+
- Node.js 18+
- npm 或 yarn

### 安裝步驟

1. **Clone 專案**

```bash
git clone <repository-url>
cd TWStockNote
```

2. **設置後端**

```bash
cd backend
python -m venv venv
source venv/bin/activate  # macOS/Linux
# or venv\Scripts\activate  # Windows
pip install -r requirements.txt
```

3. **設置前端**

```bash
cd ../frontend
npm install
```

### 執行應用

#### 方式 1: 使用啟動腳本 (推薦)

```bash
./start.sh
```

這會自動啟動後端和前端，並在終端顯示相關資訊。

#### 方式 2: 手動啟動

1. **啟動後端 API** (在 `backend/` 目錄)

```bash
cd backend
./venv/bin/python3 main.py
# API 將運行在 http://localhost:8000
```

2. **啟動前端開發伺服器** (在新終端機的 `frontend/` 目錄)

```bash
cd frontend
npm run dev
# 前端將運行在 http://localhost:3000
```

3. **開啟瀏覽器**
   訪問 http://localhost:3000 查看應用

**API 文檔**: http://localhost:8000/docs (Swagger UI)

## API 端點

### GET /api/nasdaq/historical

獲取歷史 Nasdaq 資料

**查詢參數:**

- `start_date` (可選): YYYY-MM-DD 格式的開始日期
- `end_date` (可選): YYYY-MM-DD 格式的結束日期

### GET /api/nasdaq/declines

獲取下跌期間列表

**查詢參數:**

- `start_date` (可選): YYYY-MM-DD 格式的開始日期
- `end_date` (可選): YYYY-MM-DD 格式的結束日期
- `threshold` (可選): 最小下跌百分比 (預設: 0.10)

### GET /api/nasdaq/latest

獲取最新資料點和當前下跌狀態

### POST /api/nasdaq/update

觸發資料更新 (從 Yahoo Finance 下載最新資料)

## 專案結構

```
TWStockNote/
├── backend/
│   ├── main.py              # FastAPI 應用程式
│   ├── models.py            # Pydantic 資料模型
│   ├── data_service.py      # 資料服務和下跌檢測邏輯
│   ├── requirements.txt     # Python 依賴
│   └── README.md
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   │   ├── ChartView.vue        # 圖表組件
│   │   │   ├── DateRangePicker.vue  # 日期選擇器
│   │   │   ├── DeclineAlert.vue     # 警報顯示
│   │   │   └── Statistics.vue       # 統計面板
│   │   ├── api/
│   │   │   └── nasdaq.js            # API 服務
│   │   ├── App.vue                  # 主應用程式
│   │   ├── main.js                  # 入口點
│   │   └── style.css                # 全域樣式
│   ├── package.json
│   ├── vite.config.js
│   ├── tailwind.config.js
│   └── README.md
├── .github/
│   └── copilot-instructions.md      # 開發指南
└── README.md
```

## 下跌檢測演算法

系統使用以下邏輯來檢測下跌期間:

1. **追蹤滾動最大值 (峰值)**
2. **計算當前相對於峰值的回撤**
3. **如果回撤 > 10%，標記為下跌階段**
4. **追蹤警報閾值** (10%, 15%, 20%, 25%, ...)
5. **識別谷底** (恢復前的局部最小值)

## 開發指南

詳細的開發指南和 AI Agent 技能說明請參考 [.github/copilot-instructions.md](.github/copilot-instructions.md)

## 資料模型

### NasdaqDaily

```python
{
  "date": datetime,
  "open": float,
  "high": float,
  "low": float,
  "close": float,
  "volume": int
}
```

### DeclinePeriod

```python
{
  "start_date": datetime,      # 峰值日期
  "end_date": datetime,         # 谷底日期
  "peak_value": float,
  "trough_value": float,
  "decline_percentage": float,
  "alert_levels": List[float],  # [10, 15, 20, ...]
  "is_ongoing": bool
}
```

## 貢獻

歡迎提交 Issues 和 Pull Requests！

## 授權

MIT License

## 作者

Steven - 2026年2月1日
