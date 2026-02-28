---
description: Cập nhật BDR Kit lên phiên bản mới nhất
---

# WORKFLOW: /bdr-update — Cập Nhật BDR Kit

**Vai trò:** System Updater
**Mục tiêu:** Kiểm tra và cập nhật BDR Kit lên version mới nhất.

---

## Cách dùng

```
/bdr-update
```

---

## Flow

### Bước 1: Check version hiện tại

Đọc file `~/.gemini/bdr_version` hoặc `~/.bdr/VERSION`.

### Bước 2: Check version mới

Fetch `https://raw.githubusercontent.com/hungpixi/business-deep-research/main/VERSION`

### Bước 3: So sánh

**Nếu đã mới nhất:**
```
✅ BDR Kit đã là phiên bản mới nhất (vX.X.X)
```

**Nếu có update:**
```
📦 Phiên bản hiện tại: vX.X.X
📦 Phiên bản mới: vX.X.X

🔄 Đang cập nhật...
```

### Bước 4: Cập nhật

Chạy lại install script:

**Windows:**
```powershell
irm https://raw.githubusercontent.com/hungpixi/business-deep-research/main/install.ps1 | iex
```

**Mac/Linux:**
```bash
curl -fsSL https://raw.githubusercontent.com/hungpixi/business-deep-research/main/install.sh | sh
```

### Bước 5: Xác nhận

```
✅ Đã cập nhật BDR Kit lên vX.X.X!
📋 Changelog: [link GitHub releases]
```
