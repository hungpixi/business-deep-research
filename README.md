# 🧠 Business Deep Research — AI Startup Planner

<div align="center">

**AI agent tạo kế hoạch kinh doanh chi tiết — áp dụng 12 MBA frameworks, real-time Google Search, auto scorecard.**

> *"AI tạo sản phẩm. **Con người** vận hành dịch vụ."*

[![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)](https://python.org)
[![Next.js](https://img.shields.io/badge/Next.js-15-black.svg)](https://nextjs.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.100+-green.svg)](https://fastapi.tiangolo.com)
[![Gemini](https://img.shields.io/badge/Gemini-2.5_Pro-purple.svg)](https://ai.google.dev)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

</div>

---

## 🎯 Tại sao không chỉ dùng ChatGPT?

| Tính năng | ChatGPT/Claude | Business Deep Research |
|---|:---:|:---:|
| 🔍 Real-time Google Search grounding | ❌ | ✅ |
| 📐 12 MBA Frameworks có thể chỉnh sửa | ❌ | ✅ |
| 📊 Auto Scorecard chấm điểm ý tưởng | ❌ | ✅ |
| ⚖️ So sánh 2+ ideas cùng lúc | ❌ | ✅ |
| 🎤 1-click → Pitch Deck / GTM / Tài chính | ❌ | ✅ |
| 📋 4 Output Formats khác nhau | ❌ | ✅ |
| 📚 Knowledge Base chỉnh sửa real-time | ❌ | ✅ |
| 🔀 Antigravity Proxy — không rate limit | ❌ | ✅ |

---

## ⚡ Cài Đặt Nhanh (Chỉ 1 Lệnh)

### Windows (PowerShell)

```powershell
irm https://raw.githubusercontent.com/hungpixi/business-deep-research/main/install.ps1 | iex
```

### macOS / Linux

```bash
curl -fsSL https://raw.githubusercontent.com/hungpixi/business-deep-research/main/install.sh | sh
```

> Script tự động: kiểm tra prerequisites → tải workflows & skills → clone repo → cấu hình API → cài dependencies → build frontend → tạo desktop shortcut.

⚠️ **Windows:** Gặp lỗi ExecutionPolicy? Chạy lệnh này trước:
```powershell
Set-ExecutionPolicy RemoteSigned -Scope CurrentUser
```

---

## 🎮 Slash Commands (Antigravity IDE)

Sau khi cài, mở IDE và gõ:

| Lệnh | Mô tả |
|---|---|
| `/research [ý tưởng]` | 🔬 Deep research 5 bước → Business Plan hoàn chỉnh |
| `/pitch` | 🎤 Tạo Pitch Deck 12 slides (Sequoia format) |
| `/compare [A] vs [B]` | ⚖️ So sánh 2+ ý tưởng, scorecard song song |
| `/webui` | 🌐 Mở Web UI tại localhost:5000 |
| `/bdr-update` | 🔄 Cập nhật lên version mới |
| `/bdr-help` | ❓ Xem tất cả commands |

**Ví dụ:**
```
/research AI chatbot CSKH cho SME Việt Nam
/compare AI chatbot vs AI content marketing cho SME
/pitch
```

---

## 🏗️ Kiến trúc & Tư duy

### Pipeline 5 bước

```
Ý tưởng startup
    │
    ▼
┌──────────────────────────────────────┐
│ Step 1: Nghiên cứu Thị trường       │ ← Google Search Grounding
│         & Đối thủ cạnh tranh        │   (Batched queries, cached 24h)
├──────────────────────────────────────┤
│ Step 2: Chiến lược & Go-to-Market   │ ← MBA Frameworks
│         (SWOT, Porter's, Blue Ocean) │   (Knowledge base .md files)
├──────────────────────────────────────┤
│ Step 3: Tài chính & Chấm điểm      │ ← Financial projections
│         (ROI, Break-even, Unit Eco.) │   (Auto scorecard 5 metrics)
├──────────────────────────────────────┤
│ Step 4: Devil's Advocate            │ ← Critical review
│         (Phản biện & Rủi ro)        │   (Counter-arguments)
├──────────────────────────────────────┤
│ Step 5: Tổng hợp Business Plan      │ ← Full report generation
│         (Markdown + citations)       │   (Download / Copy)
└──────────────────────────────────────┘
    │
    ▼
📊 Scorecard + 🚀 Quick Actions (Pitch Deck, GTM 90d, Tài chính, Đối thủ, Rủi ro)
```

### Điểm khác biệt so với các tool có sẵn

1. **Grounded, không hallucinate** — Mọi data đều từ Google Search thực, có citation nguồn
2. **Framework-driven** — Không trả lời chung chung, áp MBA frameworks cụ thể vào từng phần
3. **Editable knowledge** — Sửa framework .md files → thay đổi cách AI phân tích
4. **Anti-rate-limit** — Tích hợp [Antigravity Manager](https://github.com/lbjlaq/Antigravity-Manager) proxy
5. **Vietnamese-first** — Tối ưu cho thị trường Việt Nam, số liệu VND, đối thủ local

---

## 🚀 Quick Start

### 1. Clone & Setup

```bash
git clone https://github.com/hungpixi/business-deep-research.git
cd business-deep-research
```

### 2. Cấu hình API

```bash
cp .env.example .env
# Sửa .env: thêm GEMINI_API_KEY (bắt buộc)
```

### 3. One-click chạy

**Windows:**
```bash
start.bat
```

**Mac/Linux:**
```bash
chmod +x start.sh && ./start.sh
```

Mở http://localhost:5000 🎉

---

## 🔀 Setup Antigravity Tools (Recommended — No Rate Limit!)

Pipeline gọi Gemini API nhiều lần → dễ bị rate limit 429. **Antigravity Manager** là proxy local giúp bypass hoàn toàn:

### Bước 1: Cài Antigravity Manager

Download tại: **https://github.com/lbjlaq/Antigravity-Manager**

```bash
# Windows (PowerShell)
irm https://raw.githubusercontent.com/lbjlaq/Antigravity-Manager/main/install.ps1 | iex

# Hoặc tải file .exe từ Releases
```

### Bước 2: Cấu hình Antigravity

1. Mở Antigravity Manager → Tab **"API Proxy"**
2. Bật **"Dịch vụ"** (nút xanh ở góc phải)
3. Copy **API Key** (dạng `sk-xxxx...`)
4. Port mặc định: **8045**

### Bước 3: Thêm vào `.env`

```env
PROXY_API_KEY=sk-your_antigravity_key_here
PROXY_BASE_URL=http://localhost:8045/v1
PROXY_MODEL=gemini-2.5-pro
```

### Kết quả:

```
  🔀 Routing via Antigravity proxy → gemini-2.5-pro
```

Phần phân tích nặng (Step 2-5) sẽ route qua proxy → **không bị 429**, search grounding vẫn dùng direct API.

---

## 🎛️ Tính năng Web UI

### Output Formats

| Format | Mô tả |
|---|---|
| 📋 Full Plan | Business plan chi tiết 12 frameworks |
| 🎤 Pitch Deck | Outline slide deck cho investor (Sequoia format) |
| ⚡ Lean Canvas | Tập trung MVP & đo lường nhanh |
| 🚀 Go-to-Market | Chiến lược ra thị trường 90 ngày |

### Quick Actions (sau khi phân tích xong)

- 🎤 **Pitch Deck** — Outline slides theo Sequoia format
- 📅 **Go-to-Market 90d** — Kế hoạch tuần/tháng chi tiết
- 💰 **Tài chính chi tiết** — Revenue projection 12 tháng
- 🎯 **Phân tích đối thủ** — Bảng so sánh 3-5 competitors
- ⚠️ **Rủi ro & Giải pháp** — Top 5 risks + mitigation

### 12 MBA Frameworks

```
lean_canvas          business_model_canvas    tam_sam_som
swot_tows            competitive_analysis     porters_five_forces
blue_ocean           financial_projections    investment_analysis
ansoff_matrix        bcg_matrix               value_chain
pestel (bonus)
```

Tất cả đều là `.md` files có thể **chỉnh sửa trực tiếp** trong Web UI → Knowledge Base tab.

---

## 📂 Cấu trúc Project

```
business-deep-research/
├── install.ps1             # ⚡ One-command installer (Windows)
├── install.sh              # ⚡ One-command installer (Mac/Linux)
├── VERSION                 # Kit version tracking
├── workflows/              # 🎮 Antigravity slash commands
│   ├── research.md         # /research — Deep research 5 bước
│   ├── pitch.md            # /pitch — Pitch Deck Sequoia
│   ├── compare.md          # /compare — So sánh ý tưởng
│   ├── webui.md            # /webui — Mở Web UI
│   ├── bdr-update.md       # /bdr-update — Cập nhật kit
│   └── bdr-help.md         # /bdr-help — Help
├── bdr_skills/             # 🧠 AI Skills
│   ├── bdr-research-engine/  # Pipeline + search strategy
│   └── bdr-knowledge-base/   # MBA frameworks usage
├── app.py                  # FastAPI backend + SSE streaming
├── pipeline.py             # 5-step analysis pipeline
├── config.py               # Industries, markets, frameworks config
├── utils.py                # File loading utilities
├── tools/
│   ├── gemini_search.py    # Google Search + Antigravity proxy
│   ├── search_cache.py     # 24h search cache (SQLite)
│   └── output_validator.py # Output quality checker
├── knowledge/
│   ├── frameworks/         # 14 MBA framework .md files (editable)
│   ├── industries/         # Industry knowledge
│   └── markets/            # Market knowledge (Vietnam, SEA, ...)
├── web/                    # Next.js frontend
│   ├── app/
│   │   ├── page.js         # Chat UI + Scorecard + Quick Actions
│   │   ├── layout.js       # Root layout
│   │   └── globals.css     # Dark theme design system
│   └── package.json
├── start.bat               # Windows one-click run
├── start.sh                # Mac/Linux one-click run
├── .env.example            # Template config
└── requirements.txt        # Python dependencies
```

---

## 🛠️ Tech Stack

| Layer | Technology | Lý do chọn |
|---|---|---|
| Backend | **FastAPI** | Async + SSE native, nhanh hơn Flask 3x |
| Frontend | **Next.js 15** | Static export, React hooks |
| AI | **Gemini 2.5 Pro** | Google Search grounding, 1M token context |
| Proxy | **Antigravity Manager** | Bypass rate limit, multi-account rotation |
| Search | **Google Search Grounding** | Real-time data, citations |
| Cache | **SQLite** | 24h TTL, zero config |

---

## 📊 Hướng phát triển

- [x] ⚡ Startup Kit — cài 1 lệnh, slash commands trong IDE
- [ ] Export PDF / DOCX
- [ ] Multi-language output (EN, JP, KR)
- [ ] Team collaboration (shared reports)
- [ ] Custom framework builder (drag & drop)
- [ ] Webhook integration (Slack, Discord)
- [ ] Docker one-click deploy

---

## 🤝 Bạn muốn AI Agent tương tự?

| Bạn cần | Chúng tôi đã làm ✅ |
|---|---|
| AI phân tích thị trường | Business Deep Research Agent |
| AI tạo content marketing | Em Content — Auto content pipeline |
| AI quản lý xuất nhập khẩu | Sourcing Agent — Tìm xưởng, báo giá |
| AI trade tự động | Trading Bot — MT5 integration |

<div align="center">

### Comarai — AI Automation Agency

> *"Bán thời gian làm việc nhàm chán cho AI, giữ thời gian cho việc quan trọng."*

**4 nhân viên AI chạy 24/7:**
🤖 Em Sale · 📝 Em Content · 📊 Em Marketing · 📈 Em Trade

[![Yêu cầu Demo](https://img.shields.io/badge/Yêu_cầu_Demo-comarai.com-blue?style=for-the-badge)](https://comarai.com)
[![Zalo](https://img.shields.io/badge/Zalo-0834422439-green?style=for-the-badge)](https://zalo.me/0834422439)
[![Email](https://img.shields.io/badge/Email-Contact-red?style=for-the-badge)](mailto:hungphamphunguyen@gmail.com)

**GitHub:** [github.com/hungpixi](https://github.com/hungpixi)

</div>

---

## 📝 License

MIT — Tự do sử dụng, fork, chỉnh sửa. Credit appreciated.

Built with ❤️ by [hungpixi](https://github.com/hungpixi) × [Comarai](https://comarai.com)
