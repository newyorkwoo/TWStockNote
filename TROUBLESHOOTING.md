# 故障排除指南

## 問題 1: 載入資料失敗 - Request failed with status code 500

### 原因

時區（timezone）比較錯誤。當比較 offset-naive 和 offset-aware datetime 對象時，Python 會拋出異常。

### 解決方案

已在 `backend/data_service.py` 中修復，使用 `.replace(tzinfo=None)` 移除時區信息後再比較日期。

### 修復的代碼

```python
if start_date:
    start_dt = datetime.fromisoformat(start_date).replace(tzinfo=None)
    filtered_data = [d for d in filtered_data if d.date.replace(tzinfo=None) >= start_dt]

if end_date:
    end_dt = datetime.fromisoformat(end_date).replace(tzinfo=None)
    filtered_data = [d for d in filtered_data if d.date.replace(tzinfo=None) <= end_dt]
```

## 問題 2: 後端端口已被佔用

### 症狀

```
ERROR: [Errno 48] error while attempting to bind on address ('0.0.0.0', 8000): address already in use
```

### 解決方案

1. 查找佔用端口的進程：

```bash
lsof -ti:8000
```

2. 終止舊進程：

```bash
pkill -f "python.*main.py"
```

3. 重新啟動：

```bash
cd backend
./venv/bin/python3 main.py
```

## 問題 3: 前端連接失敗

### 症狀

前端無法連接到後端 API，顯示網絡錯誤。

### 檢查步驟

1. 確認後端正在運行：

```bash
curl http://localhost:8000/
```

2. 確認前端正在運行：

```bash
curl http://localhost:3000/
```

3. 使用診斷腳本：

```bash
./diagnose.sh
```

## 快速修復命令

### 完全重啟系統

```bash
# 停止所有服務
pkill -f "python.*main.py"
pkill -f "vite"

# 啟動後端
cd backend
nohup ./venv/bin/python3 main.py > /tmp/backend.log 2>&1 &

# 啟動前端
cd ../frontend
nohup npm run dev > /tmp/frontend.log 2>&1 &

# 檢查狀態
cd ..
./diagnose.sh
```

### 查看日誌

```bash
# 後端日誌
tail -f /tmp/backend.log

# 前端日誌
tail -f /tmp/frontend.log
```

## 常見錯誤代碼

### HTTP 500 - Internal Server Error

- **原因**: 後端代碼錯誤、數據格式問題、時區比較錯誤
- **解決**: 檢查後端日誌，查看具體錯誤信息

### HTTP 404 - Not Found

- **原因**: API 端點路徑錯誤
- **解決**: 確認 API 路徑正確，參考 API 文檔

### HTTP 502 - Bad Gateway

- **原因**: 後端服務未運行
- **解決**: 啟動後端服務

### Connection Refused

- **原因**: 服務未啟動或端口錯誤
- **解決**: 檢查服務狀態和端口配置

## 驗證系統正常運行

### 1. 測試後端 API

```bash
# 根端點
curl http://localhost:8000/

# 最新數據
curl http://localhost:8000/api/nasdaq/latest

# 歷史數據
curl 'http://localhost:8000/api/nasdaq/historical?start_date=2024-01-01&end_date=2024-01-05'

# 下跌期間
curl 'http://localhost:8000/api/nasdaq/declines?start_date=2022-01-01'
```

### 2. 測試前端

在瀏覽器中打開：

- http://localhost:3000

應該看到：

- 統計面板顯示最新數據
- K線圖正常載入
- 日期選擇器可用
- 沒有控制台錯誤

## 預防措施

### 1. 使用診斷腳本

定期運行診斷腳本檢查系統狀態：

```bash
./diagnose.sh
```

### 2. 正確啟動服務

使用虛擬環境的 Python：

```bash
./venv/bin/python3 main.py  # ✅ 正確
python main.py              # ❌ 可能使用錯誤的 Python
```

### 3. 檢查端口佔用

啟動前檢查端口是否已被佔用：

```bash
lsof -i:8000  # 後端
lsof -i:3000  # 前端
```

### 4. 定期更新數據

使用 API 更新數據：

```bash
curl -X POST http://localhost:8000/api/nasdaq/update
```

## 聯繫與支持

如果遇到其他問題：

1. 查看日誌文件（`/tmp/backend.log` 和 `/tmp/frontend.log`）
2. 運行診斷腳本（`./diagnose.sh`）
3. 檢查 GitHub Issues
4. 查閱項目文檔（README.md）

## 重要文件位置

- 後端主文件: `backend/main.py`
- 數據服務: `backend/data_service.py`
- 前端主應用: `frontend/src/App.vue`
- API 配置: `frontend/src/api/nasdaq.js`
- 後端日誌: `/tmp/backend.log`
- 前端日誌: `/tmp/frontend.log`
- 數據緩存: `backend/nasdaq_data.json`
