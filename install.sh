#!/bin/bash
# ╔══════════════════════════════════════════════════════════╗
# ║  🧠 BDR — Business Deep Research Kit Installer          ║
# ║  by hungpixi × Comarai (https://comarai.com)            ║
# ╚══════════════════════════════════════════════════════════╝

REPO_BASE="https://raw.githubusercontent.com/hungpixi/business-deep-research/main"
REPO_GIT="https://github.com/hungpixi/business-deep-research.git"

# === File lists ===
WORKFLOWS=(
    "research.md" "pitch.md" "compare.md"
    "webui.md" "bdr-update.md" "bdr-help.md"
)

SKILLS=(
    "bdr-research-engine"
    "bdr-knowledge-base"
)

# === Paths ===
ANTIGRAVITY_GLOBAL="$HOME/.gemini/antigravity/global_workflows"
SKILLS_DIR="$HOME/.gemini/antigravity/skills"
BDR_HOME="$HOME/.bdr"
BDR_VERSION_FILE="$HOME/.gemini/bdr_version"
GEMINI_MD="$HOME/.gemini/GEMINI.md"

# === Colors ===
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
GRAY='\033[0;90m'
WHITE='\033[1;37m'
NC='\033[0m'

# === Get version ===
CURRENT_VERSION=$(curl -fsSL "$REPO_BASE/VERSION" 2>/dev/null || echo "1.0.0")
CURRENT_VERSION=$(echo "$CURRENT_VERSION" | tr -d '\r\n ')

# === Banner ===
echo ""
echo -e "${CYAN}╔══════════════════════════════════════════════════════════╗${NC}"
echo -e "${CYAN}║  🧠 BDR — Business Deep Research Kit v$CURRENT_VERSION              ║${NC}"
echo -e "${CYAN}║  AI Deep Research Pipeline > ChatGPT chung chung         ║${NC}"
echo -e "${CYAN}║  by hungpixi × Comarai (https://comarai.com)             ║${NC}"
echo -e "${CYAN}╚══════════════════════════════════════════════════════════╝${NC}"
echo ""

# === Check existing version ===
if [ -f "$BDR_VERSION_FILE" ]; then
    OLD_VERSION=$(cat "$BDR_VERSION_FILE")
    echo -e "${YELLOW}📦 Phiên bản hiện tại: $OLD_VERSION${NC}"
    echo -e "${GREEN}📦 Phiên bản mới: $CURRENT_VERSION${NC}"
    echo ""
fi

# === Choose install mode ===
echo -e "${WHITE}📋 Chọn chế độ cài đặt:${NC}"
echo -e "${GREEN}   1. Global (mặc định) — Dùng được ở MỌI workspace${NC}"
echo -e "${YELLOW}   2. Workspace — Chỉ dùng trong project hiện tại${NC}"
echo ""
read -p "Chọn (1 hoặc 2, Enter = 1): " mode
if [ "$mode" = "2" ]; then
    INSTALL_MODE="workspace"
    WORKFLOWS_DIR="./.agents/workflows"
    SKILLS_INSTALL_DIR="./.agents/skills"
    echo -e "${YELLOW}📂 Cài vào Workspace: $PWD${NC}"
else
    INSTALL_MODE="global"
    WORKFLOWS_DIR="$ANTIGRAVITY_GLOBAL"
    SKILLS_INSTALL_DIR="$SKILLS_DIR"
    echo -e "${GREEN}📂 Cài Global: $ANTIGRAVITY_GLOBAL${NC}"
fi
echo ""

# === Check prerequisites ===
echo -e "${CYAN}🔍 Kiểm tra prerequisites...${NC}"
prereq_ok=true

if command -v git &>/dev/null; then
    echo -e "   ${GREEN}✅ Git${NC}"
else
    echo -e "   ${RED}❌ Git — Cần cài: https://git-scm.com${NC}"
    prereq_ok=false
fi

if command -v python3 &>/dev/null; then
    py_ver=$(python3 --version 2>&1)
    echo -e "   ${GREEN}✅ $py_ver${NC}"
    PYTHON_CMD="python3"
elif command -v python &>/dev/null; then
    py_ver=$(python --version 2>&1)
    echo -e "   ${GREEN}✅ $py_ver${NC}"
    PYTHON_CMD="python"
else
    echo -e "   ${RED}❌ Python 3.10+ — Cần cài: https://python.org${NC}"
    prereq_ok=false
    PYTHON_CMD="python3"
fi

if command -v node &>/dev/null; then
    node_ver=$(node --version 2>&1)
    echo -e "   ${GREEN}✅ Node.js ($node_ver)${NC}"
else
    echo -e "   ${RED}❌ Node.js 18+ — Cần cài: https://nodejs.org${NC}"
    prereq_ok=false
fi

if command -v npm &>/dev/null; then
    echo -e "   ${GREEN}✅ npm${NC}"
else
    echo -e "   ${RED}❌ npm${NC}"
    prereq_ok=false
fi

if [ "$prereq_ok" = false ]; then
    echo ""
    echo -e "${RED}❌ Thiếu prerequisites. Cài đặt rồi chạy lại nhé!${NC}"
    exit 1
fi
echo ""

# ══════════════════════════════════════════════════
# 1. CÀI WORKFLOWS
# ══════════════════════════════════════════════════

mkdir -p "$WORKFLOWS_DIR"
echo -e "${CYAN}⏳ Đang tải workflows...${NC}"
success=0
for wf in "${WORKFLOWS[@]}"; do
    if curl -fsSL "$REPO_BASE/workflows/$wf" -o "$WORKFLOWS_DIR/$wf" 2>/dev/null; then
        echo -e "   ${GREEN}✅ $wf${NC}"
        ((success++))
    else
        echo -e "   ${RED}❌ $wf${NC}"
    fi
done
echo -e "   ${CYAN}📋 $success/${#WORKFLOWS[@]} workflows installed${NC}"
echo ""

# ══════════════════════════════════════════════════
# 2. CÀI SKILLS
# ══════════════════════════════════════════════════

echo -e "${CYAN}⏳ Đang tải skills...${NC}"
for skill in "${SKILLS[@]}"; do
    skill_dir="$SKILLS_INSTALL_DIR/$skill"
    mkdir -p "$skill_dir"
    if curl -fsSL "$REPO_BASE/bdr_skills/$skill/SKILL.md" -o "$skill_dir/SKILL.md" 2>/dev/null; then
        echo -e "   ${GREEN}✅ $skill${NC}"
    else
        echo -e "   ${RED}❌ $skill${NC}"
    fi
done
echo ""

# ══════════════════════════════════════════════════
# 3. CLONE REPO
# ══════════════════════════════════════════════════

echo -e "${CYAN}⏳ Đang tải Web UI & Pipeline...${NC}"
clone_ok=true
if [ -d "$BDR_HOME" ]; then
    echo -e "   ${YELLOW}📂 $BDR_HOME đã tồn tại — đang cập nhật...${NC}"
    cd "$BDR_HOME" && git pull --quiet 2>/dev/null && cd - >/dev/null
    echo -e "   ${GREEN}✅ Đã cập nhật repo${NC}"
else
    if git clone --quiet "$REPO_GIT" "$BDR_HOME" 2>/dev/null; then
        echo -e "   ${GREEN}✅ Đã clone repo vào $BDR_HOME${NC}"
    else
        echo -e "   ${RED}❌ Clone failed — kiểm tra kết nối mạng${NC}"
        echo -e "   ${YELLOW}⚠️ Bỏ qua Web UI setup. Workflows vẫn hoạt động.${NC}"
        clone_ok=false
    fi
fi
echo ""

# ══════════════════════════════════════════════════
# 4. CẤU HÌNH .ENV
# ══════════════════════════════════════════════════

if [ "$clone_ok" = true ]; then
    ENV_FILE="$BDR_HOME/.env"
    if [ ! -f "$ENV_FILE" ]; then
        echo -e "${CYAN}🔑 Cấu hình API Keys:${NC}"
        echo -e "${GRAY}   (Nhấn Enter để bỏ qua — có thể cấu hình sau trong ~/.bdr/.env)${NC}"
        echo ""
        
        read -p "   GEMINI_API_KEY (bắt buộc cho Web UI): " gemini_key
        read -p "   TAVILY_API_KEY (optional): " tavily_key
        read -p "   PROXY_API_KEY - Antigravity Manager (optional): " proxy_key
        
        cat > "$ENV_FILE" << EOF
# === Gemini API ===
GEMINI_API_KEY=$gemini_key
GEMINI_MODEL_FAST=gemini-3.0-flash
GEMINI_MODEL_PRO=gemini-3.1-pro

# === Tavily Search (optional) ===
TAVILY_API_KEY=$tavily_key

# === Antigravity Tools Proxy (recommended — avoids rate limit) ===
# Download: https://github.com/lbjlaq/Antigravity-Manager
PROXY_API_KEY=$proxy_key
PROXY_BASE_URL=http://localhost:8045/v1
PROXY_MODEL=gemini-3.1-pro

# === Output ===
OUTPUT_DIR=./output
EOF
        
        echo ""
        echo -e "   ${GREEN}✅ Đã tạo .env${NC}"
    else
        echo -e "${YELLOW}🔑 .env đã tồn tại — giữ nguyên${NC}"
    fi
    echo ""

    # ══════════════════════════════════════════════════
    # 5. CÀI DEPENDENCIES
    # ══════════════════════════════════════════════════

    echo -e "${CYAN}⏳ Đang cài Python dependencies...${NC}"
    cd "$BDR_HOME"
    $PYTHON_CMD -m pip install -r requirements.txt --quiet --no-input 2>/dev/null
    if [ $? -eq 0 ]; then
        echo -e "   ${GREEN}✅ Python deps OK${NC}"
    else
        echo -e "   ${YELLOW}⚠️ Lỗi cài Python deps — chạy 'pip install -r ~/.bdr/requirements.txt' sau${NC}"
    fi

    echo -e "${CYAN}⏳ Đang cài & build Next.js frontend...${NC}"
    if [ ! -f "web/out/index.html" ]; then
        cd web
        npm install --silent 2>/dev/null
        npm run build --silent 2>/dev/null
        cd ..
        if [ -f "web/out/index.html" ]; then
            echo -e "   ${GREEN}✅ Frontend built${NC}"
        else
            echo -e "   ${YELLOW}⚠️ Frontend build failed — chạy 'cd ~/.bdr/web && npm run build' sau${NC}"
        fi
    else
        echo -e "   ${GREEN}✅ Frontend đã build sẵn${NC}"
    fi
    cd - >/dev/null
    echo ""
else
    echo -e "${YELLOW}⏩ Bỏ qua Web UI setup (clone failed)${NC}"
    echo ""
fi

# ══════════════════════════════════════════════════
# 6. LƯU VERSION
# ══════════════════════════════════════════════════

mkdir -p "$HOME/.gemini"
echo "$CURRENT_VERSION" > "$BDR_VERSION_FILE"

# ══════════════════════════════════════════════════
# 7. CẬP NHẬT GEMINI.MD
# ══════════════════════════════════════════════════

BDR_MARKER="<!-- BDR-KIT -->"

BDR_INSTRUCTIONS="
$BDR_MARKER
## BDR — Business Deep Research Kit v$CURRENT_VERSION

Bạn có quyền truy cập BDR Kit. Khi user gõ các lệnh sau, hãy đọc workflow tương ứng:

| Lệnh | Workflow | Mô tả |
|---|---|---|
| /research | research.md | Deep research 5 bước cho ý tưởng startup |
| /pitch | pitch.md | Tạo Pitch Deck (Sequoia format) |
| /compare | compare.md | So sánh 2+ ý tưởng startup |
| /webui | webui.md | Mở Web UI |
| /bdr-update | bdr-update.md | Cập nhật BDR Kit |
| /bdr-help | bdr-help.md | Hiển thị help |

BDR App Location: $BDR_HOME
BDR Web UI: http://localhost:5000

**Quan trọng:** Khi chạy /research, LUÔN search web để có data thực, áp MBA frameworks cụ thể, viết tiếng Việt.
$BDR_MARKER"

if [ -f "$GEMINI_MD" ]; then
    # Remove old BDR section if exists
    if grep -q "$BDR_MARKER" "$GEMINI_MD"; then
        # Remove old BDR section (macOS + Linux compatible)
        if [[ "$OSTYPE" == "darwin"* ]]; then
            sed -i '' "/$BDR_MARKER/,/$BDR_MARKER/d" "$GEMINI_MD"
        else
            sed -i "/$BDR_MARKER/,/$BDR_MARKER/d" "$GEMINI_MD"
        fi
    fi
    echo "$BDR_INSTRUCTIONS" >> "$GEMINI_MD"
else
    echo "# Global AI Rules" > "$GEMINI_MD"
    echo "$BDR_INSTRUCTIONS" >> "$GEMINI_MD"
fi
echo -e "${GREEN}✅ Đã cập nhật GEMINI.md${NC}"

# ══════════════════════════════════════════════════
# DONE!
# ══════════════════════════════════════════════════

echo ""
echo -e "${GREEN}╔══════════════════════════════════════════════════════════╗${NC}"
echo -e "${GREEN}║  ✅ BDR Kit v$CURRENT_VERSION đã cài thành công!                    ║${NC}"
echo -e "${GREEN}╚══════════════════════════════════════════════════════════╝${NC}"
echo ""
echo -e "${WHITE}🚀 BẮT ĐẦU NGAY:${NC}"
echo ""
echo -e "${GRAY}   Mở Antigravity IDE và gõ:${NC}"
echo ""
echo -e "${CYAN}   /research AI chatbot CSKH cho SME Việt Nam${NC}"
echo ""
echo -e "${WHITE}📋 Các lệnh khác:${NC}"
echo -e "${GRAY}   /pitch          Tạo Pitch Deck${NC}"
echo -e "${GRAY}   /compare        So sánh ý tưởng${NC}"
echo -e "${GRAY}   /webui          Mở Web UI${NC}"
echo -e "${GRAY}   /bdr-help       Xem tất cả lệnh${NC}"
echo ""
echo -e "${GRAY}🌐 Comarai — AI Automation Agency${NC}"
echo -e "${GRAY}   https://comarai.com | Zalo: 0834422439${NC}"
echo ""
