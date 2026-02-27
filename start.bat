@echo off
chcp 65001 >nul
title Business Deep Research — Web UI

echo.
echo ╔══════════════════════════════════════════════════════════════╗
echo ║                                                              ║
echo ║   🚀 BUSINESS DEEP RESEARCH — Web UI                        ║
echo ║   AI tạo sản phẩm. Con người vận hành dịch vụ.              ║
echo ║                                                              ║
echo ╚══════════════════════════════════════════════════════════════╝
echo.

REM Install Python dependencies
echo [1/3] Installing Python dependencies...
pip install -r requirements.txt --quiet 2>nul
echo      ✅ Python deps OK

REM Check if Next.js is built
if not exist "web\out\index.html" (
    echo [2/3] Building Next.js frontend...
    cd web
    call npm install --silent 2>nul
    call npm run build 2>nul
    cd ..
    echo      ✅ Frontend built
) else (
    echo [2/3] Frontend already built ✅
)

REM Start Flask
echo [3/3] Starting server...
echo.
echo ════════════════════════════════════════════════════════════════
echo   🌐 Opening http://localhost:5000
echo   📡 API: http://localhost:5000/api/config
echo   Press Ctrl+C to stop
echo ════════════════════════════════════════════════════════════════
echo.

start http://localhost:5000
python app.py
