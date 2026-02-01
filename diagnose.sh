#!/bin/bash
# 診斷腳本 - 檢查系統狀態

echo "=========================================="
echo "Nasdaq Decline Analysis System 診斷"
echo "=========================================="
echo ""

# 檢查後端
echo "1. 檢查後端 (Port 8000)..."
if curl -s http://localhost:8000/ > /dev/null 2>&1; then
    echo "   ✅ 後端正常運行"
    echo "   API 根端點回應:"
    curl -s http://localhost:8000/ | python3 -m json.tool 2>/dev/null || echo "   JSON 解析失敗"
else
    echo "   ❌ 後端未運行或無法連接"
    echo "   請執行: cd backend && ./venv/bin/python3 main.py"
fi

echo ""

# 檢查前端
echo "2. 檢查前端 (Port 3000)..."
if curl -s http://localhost:3000/ > /dev/null 2>&1; then
    echo "   ✅ 前端正常運行"
else
    echo "   ❌ 前端未運行或無法連接"
    echo "   請執行: cd frontend && npm run dev"
fi

echo ""

# 測試 API 端點
echo "3. 測試 API 端點..."
echo "   測試 /api/nasdaq/latest..."
if curl -s http://localhost:8000/api/nasdaq/latest > /dev/null 2>&1; then
    echo "   ✅ Latest API 正常"
else
    echo "   ❌ Latest API 失敗"
fi

echo "   測試 /api/nasdaq/historical..."
if curl -s 'http://localhost:8000/api/nasdaq/historical?start_date=2024-01-01&end_date=2024-01-05' > /dev/null 2>&1; then
    echo "   ✅ Historical API 正常"
else
    echo "   ❌ Historical API 失敗"
fi

echo "   測試 /api/nasdaq/declines..."
if curl -s 'http://localhost:8000/api/nasdaq/declines?start_date=2022-01-01' > /dev/null 2>&1; then
    echo "   ✅ Declines API 正常"
else
    echo "   ❌ Declines API 失敗"
fi

echo ""

# 檢查進程
echo "4. 檢查運行的進程..."
BACKEND_PID=$(ps aux | grep "python.*main.py" | grep -v grep | awk '{print $2}' | head -1)
FRONTEND_PID=$(ps aux | grep "vite" | grep -v grep | awk '{print $2}' | head -1)

if [ -n "$BACKEND_PID" ]; then
    echo "   ✅ 後端進程 (PID: $BACKEND_PID)"
else
    echo "   ❌ 後端進程未找到"
fi

if [ -n "$FRONTEND_PID" ]; then
    echo "   ✅ 前端進程 (PID: $FRONTEND_PID)"
else
    echo "   ❌ 前端進程未找到"
fi

echo ""
echo "=========================================="
echo "診斷完成"
echo "=========================================="
echo ""
echo "訪問地址:"
echo "  前端: http://localhost:3000"
echo "  後端: http://localhost:8000"
echo "  API 文檔: http://localhost:8000/docs"
echo ""
