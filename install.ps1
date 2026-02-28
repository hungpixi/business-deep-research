# ╔══════════════════════════════════════════════════════════╗
# ║  🧠 BDR — Business Deep Research Kit Installer          ║
# ║  by hungpixi × Comarai (https://comarai.com)            ║
# ╚══════════════════════════════════════════════════════════╝

$RepoBase = "https://raw.githubusercontent.com/hungpixi/business-deep-research/main"
$RepoGit = "https://github.com/hungpixi/business-deep-research.git"

# === File lists ===
$Workflows = @(
    "research.md", "pitch.md", "compare.md",
    "webui.md", "bdr-update.md", "bdr-help.md"
)

$Skills = @(
    "bdr-research-engine",
    "bdr-knowledge-base"
)

# === Detect paths ===
$AntigravityGlobal = "$env:USERPROFILE\.gemini\antigravity\global_workflows"
$SkillsDir = "$env:USERPROFILE\.gemini\antigravity\skills"
$BdrHome = "$env:USERPROFILE\.bdr"
$BdrVersionFile = "$env:USERPROFILE\.gemini\bdr_version"

# === Get version ===
try {
    $CurrentVersion = (Invoke-WebRequest -Uri "$RepoBase/VERSION" -UseBasicParsing).Content.Trim()
} catch {
    $CurrentVersion = "1.0.0"
}

# === Banner ===
Write-Host ""
Write-Host "╔══════════════════════════════════════════════════════════╗" -ForegroundColor Cyan
Write-Host "║  🧠 BDR — Business Deep Research Kit v$CurrentVersion              ║" -ForegroundColor Cyan
Write-Host "║  AI Deep Research Pipeline > ChatGPT chung chung         ║" -ForegroundColor Cyan
Write-Host "║  by hungpixi × Comarai (https://comarai.com)             ║" -ForegroundColor Cyan
Write-Host "╚══════════════════════════════════════════════════════════╝" -ForegroundColor Cyan
Write-Host ""

# === Check existing version ===
if (Test-Path $BdrVersionFile) {
    $OldVersion = Get-Content $BdrVersionFile
    Write-Host "📦 Phiên bản hiện tại: $OldVersion" -ForegroundColor Yellow
    Write-Host "📦 Phiên bản mới: $CurrentVersion" -ForegroundColor Green
    Write-Host ""
}

# === Choose install mode ===
Write-Host "📋 Chọn chế độ cài đặt:" -ForegroundColor White
Write-Host "   1. Global (mặc định) — Dùng được ở MỌI workspace" -ForegroundColor Green
Write-Host "   2. Workspace — Chỉ dùng trong project hiện tại" -ForegroundColor Yellow
Write-Host ""
$mode = Read-Host "Chọn (1 hoặc 2, Enter = 1)"
if ($mode -eq "2") {
    $InstallMode = "workspace"
    $WorkflowsDir = ".\.agents\workflows"
    $SkillsInstallDir = ".\.agents\skills"
    Write-Host "📂 Cài vào Workspace: $PWD" -ForegroundColor Yellow
} else {
    $InstallMode = "global"
    $WorkflowsDir = $AntigravityGlobal
    $SkillsInstallDir = $SkillsDir
    Write-Host "📂 Cài Global: $AntigravityGlobal" -ForegroundColor Green
}
Write-Host ""

# === Check prerequisites ===
Write-Host "🔍 Kiểm tra prerequisites..." -ForegroundColor Cyan

$prereqOk = $true

# Check Git
if (Get-Command git -ErrorAction SilentlyContinue) {
    Write-Host "   ✅ Git" -ForegroundColor Green
} else {
    Write-Host "   ❌ Git — Cần cài: https://git-scm.com" -ForegroundColor Red
    $prereqOk = $false
}

# Check Python
if (Get-Command python -ErrorAction SilentlyContinue) {
    $pyVer = python --version 2>&1
    Write-Host "   ✅ Python ($pyVer)" -ForegroundColor Green
} else {
    Write-Host "   ❌ Python 3.10+ — Cần cài: https://python.org" -ForegroundColor Red
    $prereqOk = $false
}

# Check Node
if (Get-Command node -ErrorAction SilentlyContinue) {
    $nodeVer = node --version 2>&1
    Write-Host "   ✅ Node.js ($nodeVer)" -ForegroundColor Green
} else {
    Write-Host "   ❌ Node.js 18+ — Cần cài: https://nodejs.org" -ForegroundColor Red
    $prereqOk = $false
}

# Check npm
if (Get-Command npm -ErrorAction SilentlyContinue) {
    Write-Host "   ✅ npm" -ForegroundColor Green
} else {
    Write-Host "   ❌ npm" -ForegroundColor Red
    $prereqOk = $false
}

if (-not $prereqOk) {
    Write-Host ""
    Write-Host "❌ Thiếu prerequisites. Cài đặt rồi chạy lại nhé!" -ForegroundColor Red
    exit 1
}
Write-Host ""

# ══════════════════════════════════════════════════
# 1. CÀI WORKFLOWS
# ══════════════════════════════════════════════════

if (-not (Test-Path $WorkflowsDir)) {
    New-Item -ItemType Directory -Force -Path $WorkflowsDir | Out-Null
    Write-Host "📂 Đã tạo thư mục workflows: $WorkflowsDir" -ForegroundColor Green
}

Write-Host "⏳ Đang tải workflows..." -ForegroundColor Cyan
$success = 0
foreach ($wf in $Workflows) {
    try {
        Invoke-WebRequest -Uri "$RepoBase/workflows/$wf" -OutFile "$WorkflowsDir\$wf" -ErrorAction Stop
        Write-Host "   ✅ $wf" -ForegroundColor Green
        $success++
    } catch {
        Write-Host "   ❌ $wf" -ForegroundColor Red
    }
}
Write-Host "   📋 $success/$($Workflows.Count) workflows installed" -ForegroundColor Cyan
Write-Host ""

# ══════════════════════════════════════════════════
# 2. CÀI SKILLS
# ══════════════════════════════════════════════════

Write-Host "⏳ Đang tải skills..." -ForegroundColor Cyan
foreach ($skill in $Skills) {
    $skillDir = "$SkillsInstallDir\$skill"
    if (-not (Test-Path $skillDir)) {
        New-Item -ItemType Directory -Force -Path $skillDir | Out-Null
    }
    try {
        Invoke-WebRequest -Uri "$RepoBase/bdr_skills/$skill/SKILL.md" -OutFile "$skillDir\SKILL.md" -ErrorAction Stop
        Write-Host "   ✅ $skill" -ForegroundColor Green
        $success++
    } catch {
        Write-Host "   ❌ $skill" -ForegroundColor Red
    }
}
Write-Host ""

# ══════════════════════════════════════════════════
# 3. CLONE REPO (cho Web UI + Pipeline code)
# ══════════════════════════════════════════════════

Write-Host "⏳ Đang tải Web UI & Pipeline..." -ForegroundColor Cyan

$cloneOk = $true
if (Test-Path $BdrHome) {
    Write-Host "   📂 $BdrHome đã tồn tại — đang cập nhật..." -ForegroundColor Yellow
    Push-Location $BdrHome
    git pull --quiet 2>$null
    Pop-Location
    Write-Host "   ✅ Đã cập nhật repo" -ForegroundColor Green
} else {
    git clone --quiet $RepoGit $BdrHome 2>$null
    if ($LASTEXITCODE -eq 0) {
        Write-Host "   ✅ Đã clone repo vào $BdrHome" -ForegroundColor Green
    } else {
        Write-Host "   ❌ Clone failed — kiểm tra kết nối mạng" -ForegroundColor Red
        Write-Host "   ⚠️ Bỏ qua Web UI setup. Workflows vẫn hoạt động bình thường." -ForegroundColor Yellow
        $cloneOk = $false
    }
}
Write-Host ""

# ══════════════════════════════════════════════════
# 4. CẤU HÌNH .ENV
# ══════════════════════════════════════════════════

if ($cloneOk) {
    $envFile = "$BdrHome\.env"
    if (-not (Test-Path $envFile)) {
        Write-Host "🔑 Cấu hình API Keys:" -ForegroundColor Cyan
        Write-Host "   (Nhấn Enter để bỏ qua — có thể cấu hình sau trong ~/.bdr/.env)" -ForegroundColor Gray
        Write-Host ""
        
        $geminiKey = Read-Host "   GEMINI_API_KEY (bắt buộc cho Web UI)"
        $tavilyKey = Read-Host "   TAVILY_API_KEY (optional)"
        $proxyKey = Read-Host "   PROXY_API_KEY - Antigravity Manager (optional)"
        
        $envContent = @"
# === Gemini API ===
GEMINI_API_KEY=$geminiKey
GEMINI_MODEL_FAST=gemini-3.0-flash
GEMINI_MODEL_PRO=gemini-3.1-pro

# === Tavily Search (optional) ===
TAVILY_API_KEY=$tavilyKey

# === Antigravity Tools Proxy (recommended — avoids rate limit) ===
# Download: https://github.com/lbjlaq/Antigravity-Manager
PROXY_API_KEY=$proxyKey
PROXY_BASE_URL=http://localhost:8045/v1
PROXY_MODEL=gemini-3.1-pro

# === Output ===
OUTPUT_DIR=./output
"@
        
        Set-Content -Path $envFile -Value $envContent -Encoding UTF8
        Write-Host ""
        Write-Host "   ✅ Đã tạo .env" -ForegroundColor Green
    } else {
        Write-Host "🔑 .env đã tồn tại — giữ nguyên" -ForegroundColor Yellow
    }
    Write-Host ""

    # ══════════════════════════════════════════════════
    # 5. CÀI DEPENDENCIES
    # ══════════════════════════════════════════════════

    Write-Host "⏳ Đang cài Python dependencies..." -ForegroundColor Cyan
    Push-Location $BdrHome
    pip install -r requirements.txt --quiet --no-input 2>$null
    if ($LASTEXITCODE -eq 0) {
        Write-Host "   ✅ Python deps OK" -ForegroundColor Green
    } else {
        Write-Host "   ⚠️ Có lỗi cài Python deps — chạy 'pip install -r ~/.bdr/requirements.txt' sau" -ForegroundColor Yellow
    }

    Write-Host "⏳ Đang cài & build Next.js frontend..." -ForegroundColor Cyan
    if (-not (Test-Path "web\out\index.html")) {
        Push-Location web
        npm install --silent 2>$null
        npm run build --silent 2>$null
        Pop-Location
        if (Test-Path "web\out\index.html") {
            Write-Host "   ✅ Frontend built" -ForegroundColor Green
        } else {
            Write-Host "   ⚠️ Frontend build failed — chạy 'cd ~/.bdr/web && npm run build' sau" -ForegroundColor Yellow
        }
    } else {
        Write-Host "   ✅ Frontend đã build sẵn" -ForegroundColor Green
    }
    Pop-Location
    Write-Host ""
} else {
    Write-Host "⏩ Bỏ qua Web UI setup (clone failed)" -ForegroundColor Yellow
    Write-Host ""
}

# ══════════════════════════════════════════════════
# 6. TẠO DESKTOP SHORTCUT
# ══════════════════════════════════════════════════

if ($cloneOk) {
    Write-Host "🖥️ Tạo Desktop shortcut?" -ForegroundColor Cyan
    $createShortcut = Read-Host "   Tạo shortcut 'BDR Web UI' trên Desktop? (y/N)"
if ($createShortcut -eq "y" -or $createShortcut -eq "Y") {
    $desktop = [Environment]::GetFolderPath("Desktop")
    $shortcutPath = "$desktop\BDR Web UI.lnk"
    
    $shell = New-Object -ComObject WScript.Shell
    $shortcut = $shell.CreateShortcut($shortcutPath)
    $shortcut.TargetPath = "$BdrHome\start.bat"
    $shortcut.WorkingDirectory = $BdrHome
    $shortcut.Description = "Business Deep Research — Web UI"
    $shortcut.Save()
    
    Write-Host "   ✅ Shortcut tạo tại: $shortcutPath" -ForegroundColor Green
    }
}
Write-Host ""

# ══════════════════════════════════════════════════
# 7. LƯU VERSION
# ══════════════════════════════════════════════════

if (-not (Test-Path "$env:USERPROFILE\.gemini")) {
    New-Item -ItemType Directory -Force -Path "$env:USERPROFILE\.gemini" | Out-Null
}
Set-Content -Path $BdrVersionFile -Value $CurrentVersion -Encoding UTF8

# ══════════════════════════════════════════════════
# 8. CẬP NHẬT GEMINI.MD (Global Rules)
# ══════════════════════════════════════════════════

$GeminiMd = "$env:USERPROFILE\.gemini\GEMINI.md"
$BdrMarker = "<!-- BDR-KIT -->"

$BdrInstructions = @"

$BdrMarker
## BDR — Business Deep Research Kit v$CurrentVersion

Bạn có quyền truy cập BDR Kit. Khi user gõ các lệnh sau, hãy đọc workflow tương ứng:

| Lệnh | Workflow | Mô tả |
|---|---|---|
| /research | research.md | Deep research 5 bước cho ý tưởng startup |
| /pitch | pitch.md | Tạo Pitch Deck (Sequoia format) |
| /compare | compare.md | So sánh 2+ ý tưởng startup |
| /webui | webui.md | Mở Web UI |
| /bdr-update | bdr-update.md | Cập nhật BDR Kit |
| /bdr-help | bdr-help.md | Hiển thị help |

BDR App Location: $BdrHome
BDR Web UI: http://localhost:5000 (chạy start.bat hoặc python app.py)

**Quan trọng:** Khi chạy /research, LUÔN search web để có data thực, áp MBA frameworks cụ thể, viết tiếng Việt.
$BdrMarker
"@

if (Test-Path $GeminiMd) {
    $existingContent = Get-Content $GeminiMd -Raw
    if ($existingContent -match [regex]::Escape($BdrMarker)) {
        # Remove old BDR section and add new
        $pattern = "(?s)$([regex]::Escape($BdrMarker)).*?$([regex]::Escape($BdrMarker))"
        $existingContent = $existingContent -replace $pattern, ""
        $existingContent = $existingContent.TrimEnd() + "`n" + $BdrInstructions
        Set-Content -Path $GeminiMd -Value $existingContent -Encoding UTF8
    } else {
        Add-Content -Path $GeminiMd -Value $BdrInstructions -Encoding UTF8
    }
} else {
    Set-Content -Path $GeminiMd -Value "# Global AI Rules`n$BdrInstructions" -Encoding UTF8
}
Write-Host "✅ Đã cập nhật GEMINI.md" -ForegroundColor Green

# ══════════════════════════════════════════════════
# DONE!
# ══════════════════════════════════════════════════

Write-Host ""
Write-Host "╔══════════════════════════════════════════════════════════╗" -ForegroundColor Green
Write-Host "║  ✅ BDR Kit v$CurrentVersion đã cài thành công!                    ║" -ForegroundColor Green
Write-Host "╚══════════════════════════════════════════════════════════╝" -ForegroundColor Green
Write-Host ""
Write-Host "🚀 BẮT ĐẦU NGAY:" -ForegroundColor White
Write-Host ""
Write-Host "   Mở Antigravity IDE và gõ:" -ForegroundColor Gray
Write-Host ""
Write-Host '   /research AI chatbot CSKH cho SME Việt Nam' -ForegroundColor Cyan
Write-Host ""
Write-Host "📋 Các lệnh khác:" -ForegroundColor White
Write-Host "   /pitch          Tạo Pitch Deck" -ForegroundColor Gray
Write-Host "   /compare        So sánh ý tưởng" -ForegroundColor Gray
Write-Host "   /webui          Mở Web UI" -ForegroundColor Gray
Write-Host "   /bdr-help       Xem tất cả lệnh" -ForegroundColor Gray
Write-Host ""
Write-Host "🌐 Comarai — AI Automation Agency" -ForegroundColor DarkGray
Write-Host "   https://comarai.com | Zalo: 0834422439" -ForegroundColor DarkGray
Write-Host ""
