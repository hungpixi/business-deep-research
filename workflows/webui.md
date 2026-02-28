---
description: Mở Web UI (localhost) để dùng giao diện đẹp
---

# WORKFLOW: /webui — Khởi Động Web UI

**Vai trò:** System Helper
**Mục tiêu:** Khởi động server và mở Web UI trong browser.

---

## Cách dùng

```
/webui
```

---

## Flow

### Bước 1: Tìm BDR installation

Kiểm tra theo thứ tự:
1. `~/.bdr/` (global install)
2. Workspace hiện tại (nếu có `app.py` + `web/`)

Nếu không tìm thấy:
```
❌ Chưa cài Business Deep Research.
👉 Chạy lệnh cài: irm https://raw.githubusercontent.com/hungpixi/business-deep-research/main/install.ps1 | iex
```

### Bước 2: Check .env

- Kiểm tra `.env` có `GEMINI_API_KEY` không
- Nếu thiếu → hỏi user nhập API key

### Bước 3: Start Server

**Windows:**
```powershell
# Cài deps nếu cần
pip install -r requirements.txt --quiet
# Build frontend nếu chưa có
if (!(Test-Path "web/out/index.html")) { cd web; npm install; npm run build; cd .. }
# Start
python app.py
```

**Mac/Linux:**
```bash
pip install -r requirements.txt --quiet
[ ! -f "web/out/index.html" ] && (cd web && npm install && npm run build && cd ..)
python app.py
```

### Bước 4: Mở Browser

```
✅ Server đang chạy!
🌐 Mở: http://localhost:5000
📡 API: http://localhost:5000/api/config
⏹️ Ctrl+C để dừng
```

Tự động mở browser tại http://localhost:5000.
