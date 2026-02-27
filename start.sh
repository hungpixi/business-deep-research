#!/bin/bash
echo ""
echo "╔══════════════════════════════════════════════════════════════╗"
echo "║                                                              ║"
echo "║   🚀 BUSINESS DEEP RESEARCH — Web UI                        ║"
echo "║   AI tạo sản phẩm. Con người vận hành dịch vụ.              ║"
echo "║                                                              ║"
echo "╚══════════════════════════════════════════════════════════════╝"
echo ""

# Install Python dependencies
echo "[1/3] Installing Python dependencies..."
pip install -r requirements.txt --quiet 2>/dev/null
echo "     ✅ Python deps OK"

# Check if Next.js is built
if [ ! -f "web/out/index.html" ]; then
    echo "[2/3] Building Next.js frontend..."
    cd web
    npm install --silent 2>/dev/null
    npm run build 2>/dev/null
    cd ..
    echo "     ✅ Frontend built"
else
    echo "[2/3] Frontend already built ✅"
fi

# Start Flask
echo "[3/3] Starting server..."
echo ""
echo "════════════════════════════════════════════════════════════════"
echo "  🌐 http://localhost:5000"
echo "  📡 API: http://localhost:5000/api/config"
echo "  Press Ctrl+C to stop"
echo "════════════════════════════════════════════════════════════════"
echo ""

python app.py
