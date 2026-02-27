#!/bin/bash
# ═══════════════════════════════════════════════
# Deploy Business Deep Research to VPS (1GB RAM)
# Tested on: Ubuntu 22.04 / Debian 12
# VPS: Vultr $5/mo (1 vCPU, 1GB RAM)
# ═══════════════════════════════════════════════
set -e

DOMAIN="${1:-}"
EMAIL="${2:-}"

echo "╔═══════════════════════════════════════╗"
echo "║  Business Deep Research — VPS Deploy  ║"
echo "╚═══════════════════════════════════════╝"
echo ""

# === 1. System Updates + Swap (critical for 1GB RAM) ===
echo "📦 [1/6] System setup + swap..."
sudo apt-get update -qq
sudo apt-get install -y -qq curl git

# Add 1GB swap if not exist
if [ ! -f /swapfile ]; then
    echo "  → Creating 1GB swap..."
    sudo fallocate -l 1G /swapfile
    sudo chmod 600 /swapfile
    sudo mkswap /swapfile
    sudo swapon /swapfile
    echo '/swapfile none swap sw 0 0' | sudo tee -a /etc/fstab
    echo "  ✅ Swap created (1GB)"
else
    echo "  ✅ Swap already exists"
fi

# === 2. Install Docker ===
echo "🐳 [2/6] Installing Docker..."
if ! command -v docker &> /dev/null; then
    curl -fsSL https://get.docker.com | sudo sh
    sudo usermod -aG docker $USER
    echo "  ✅ Docker installed"
else
    echo "  ✅ Docker already installed"
fi

# === 3. Clone / Pull repo ===
echo "📥 [3/6] Getting code..."
APP_DIR="$HOME/business-deep-research"
if [ -d "$APP_DIR" ]; then
    cd "$APP_DIR"
    git pull
    echo "  ✅ Code updated"
else
    git clone https://github.com/hungpixi/business-deep-research.git "$APP_DIR"
    cd "$APP_DIR"
    echo "  ✅ Code cloned"
fi

# === 4. Setup .env ===
echo "🔑 [4/6] Checking .env..."
if [ ! -f .env ]; then
    cp .env.example .env
    echo ""
    echo "  ⚠️  EDIT .env FILE NOW:"
    echo "  nano $APP_DIR/.env"
    echo ""
    echo "  Required: GEMINI_API_KEY"
    echo "  Optional: PROXY_API_KEY (for Antigravity)"
    echo ""
    read -p "  Press Enter after editing .env..."
fi

# === 5. Build & Start ===
echo "🚀 [5/6] Building & starting (this takes 2-3 min)..."

# Use docker compose (v2) or docker-compose (v1)
if docker compose version &> /dev/null; then
    COMPOSE="docker compose"
else
    COMPOSE="docker-compose"
fi

$COMPOSE down 2>/dev/null || true
$COMPOSE up --build -d

echo "  ✅ App running on port 5000"

# === 6. Optional: Nginx + SSL ===
if [ -n "$DOMAIN" ] && [ -n "$EMAIL" ]; then
    echo "🔒 [6/6] Setting up Nginx + SSL for $DOMAIN..."
    
    sudo apt-get install -y -qq nginx certbot python3-certbot-nginx
    
    # Nginx config
    sudo tee /etc/nginx/sites-available/deep-research > /dev/null << NGINX
server {
    listen 80;
    server_name $DOMAIN;
    
    location / {
        proxy_pass http://127.0.0.1:5000;
        proxy_set_header Host \$host;
        proxy_set_header X-Real-IP \$remote_addr;
        proxy_buffering off;
        proxy_cache off;
        # SSE support
        proxy_set_header Connection '';
        proxy_http_version 1.1;
        chunked_transfer_encoding off;
    }
}
NGINX

    sudo ln -sf /etc/nginx/sites-available/deep-research /etc/nginx/sites-enabled/
    sudo rm -f /etc/nginx/sites-enabled/default
    sudo nginx -t && sudo systemctl reload nginx
    
    # SSL
    sudo certbot --nginx -d "$DOMAIN" --email "$EMAIL" --agree-tos --non-interactive
    echo "  ✅ SSL setup complete: https://$DOMAIN"
else
    echo "📌 [6/6] No domain specified. Access via: http://YOUR_IP:5000"
    echo "   To add domain later: ./deploy.sh yourdomain.com you@email.com"
fi

echo ""
echo "╔═══════════════════════════════════════╗"
echo "║  ✅ Deploy complete!                  ║"
echo "║  App: http://$(curl -s ifconfig.me):5000  ║"
echo "╚═══════════════════════════════════════╝"
echo ""
echo "📋 Commands:"
echo "  Logs:    $COMPOSE logs -f"
echo "  Stop:    $COMPOSE down"
echo "  Restart: $COMPOSE up -d"
echo "  Update:  git pull && $COMPOSE up --build -d"
