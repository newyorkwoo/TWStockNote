#!/bin/bash
# 啟動腳本 - 同時啟動後端和前端

# 檢查是否安裝了依賴
echo "檢查專案依賴..."

# 檢查後端
if [ ! -d "backend/venv" ]; then
    echo "設置後端環境..."
    cd backend
    python3 -m venv venv
    ./venv/bin/pip install -r requirements.txt
    cd ..
fi

# 檢查前端
if [ ! -d "frontend/node_modules" ]; then
    echo "安裝前端依賴..."
    cd frontend
    npm install
    cd ..
fi

echo ""
echo "==================================="
echo "啟動 Nasdaq Decline Analysis System"
echo "==================================="
echo ""
echo "後端 API: http://localhost:8000"
echo "前端: http://localhost:3000"
echo ""
echo "按 Ctrl+C 停止所有服務"
echo ""

# 啟動後端 (背景執行)
echo "啟動後端..."
cd backend
./venv/bin/python3 main.py &
BACKEND_PID=$!
cd ..

# 等待後端啟動
sleep 3

# 啟動前端
echo "啟動前端..."
cd frontend
npm run dev &
FRONTEND_PID=$!
cd ..

# 等待使用者中斷
wait

# 清理
echo ""
echo "停止服務..."
kill $BACKEND_PID 2>/dev/null
kill $FRONTEND_PID 2>/dev/null
