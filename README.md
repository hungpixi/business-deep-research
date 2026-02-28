# 🧠 Business Deep Research — AI Startup Planner

<div align="center">

**Gõ 1 dòng. Nhận Business Plan 5000+ từ — có data thật, có framework, có phản biện.**

> *Không phải AI trả lời chung chung. Đây là pipeline 5 bước — search thật, framework thật, số liệu thật.*

[![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=flat-square&logo=python&logoColor=white)](https://python.org)
[![Next.js](https://img.shields.io/badge/Next.js-15-000000?style=flat-square&logo=nextdotjs)](https://nextjs.org)
[![Gemini](https://img.shields.io/badge/Gemini-2.5_Pro-8E75B2?style=flat-square&logo=googlegemini&logoColor=white)](https://ai.google.dev)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow?style=flat-square)](LICENSE)
[![Version](https://img.shields.io/badge/v1.0.0-blue?style=flat-square&label=BDR%20Kit)](https://github.com/hungpixi/business-deep-research)

</div>

---

## ⚡ Cài Đặt (1 Lệnh)

<table>
<tr>
<td width="50%">

**Windows (PowerShell)**

```powershell
irm https://raw.githubusercontent.com/hungpixi/business-deep-research/main/install.ps1 | iex
```

</td>
<td width="50%">

**macOS / Linux**

```bash
curl -fsSL https://raw.githubusercontent.com/hungpixi/business-deep-research/main/install.sh | bash
```

</td>
</tr>
</table>

> **Script tự động:** check prerequisites → tải workflows → clone repo → cấu hình API → cài deps → build frontend → tạo desktop shortcut.

<details>
<summary>⚠️ Gặp lỗi ExecutionPolicy trên Windows?</summary>

```powershell
Set-ExecutionPolicy RemoteSigned -Scope CurrentUser
```
</details>

<details>
<summary>📦 Hoặc cài thủ công (không dùng installer)</summary>

```bash
git clone https://github.com/hungpixi/business-deep-research.git
cd business-deep-research
cp .env.example .env          # Thêm GEMINI_API_KEY vào đây
pip install -r requirements.txt
cd web && npm install && npm run build && cd ..
python app.py                  # Mở http://localhost:5000
```
</details>

---

## 🎮 Slash Commands

Sau khi cài, mở **Antigravity IDE** và gõ:

```
/research AI chatbot CSKH cho SME Việt Nam
```

AI sẽ tự động chạy pipeline 5 bước → trả về business plan hoàn chỉnh.

| Lệnh | Mô tả |
|---|---|
| `/research [ý tưởng]` | 🔬 Deep research 5 bước → Business Plan 5000+ từ |
| `/pitch` | 🎤 Pitch Deck 12 slides (Sequoia format) + Speaker Notes |
| `/compare [A] vs [B]` | ⚖️ So sánh 2+ ý tưởng, scorecard song song |
| `/webui` | 🌐 Mở Web UI tại localhost:5000 |
| `/bdr-update` | 🔄 Cập nhật BDR Kit |
| `/bdr-help` | ❓ Xem tất cả commands |

---

## 🎯 Tại sao không dùng ChatGPT?

| | ChatGPT / Claude | BDR |
|---|:---:|:---:|
| 🔍 Google Search grounding (data thực, có URL) | ❌ | ✅ |
| 📐 14 MBA frameworks (chỉnh sửa được) | ❌ | ✅ |
| 📊 Auto scorecard + GO/NO-GO verdict | ❌ | ✅ |
| 😈 Devil's Advocate tự động phản biện | ❌ | ✅ |
| ⚖️ So sánh 2+ ideas cùng framework | ❌ | ✅ |
| 🎤 1-click Pitch Deck (Sequoia format) | ❌ | ✅ |
| 📚 Knowledge Base real-time editable | ❌ | ✅ |
| 🔀 Antigravity Proxy — bypass rate limit | ❌ | ✅ |
| 💰 **Chi phí** | $20/tháng | **Free** (API key) |

---

## 🏗️ Pipeline 5 Bước

```
    /research [ý tưởng]
            │
            ▼
┌───────────────────────────────────────────────┐
│  Step 1  📊  Nghiên Cứu Thị Trường           │
│  Google Search → market size, CAGR, trends    │
│  Batched queries, cached 24h                  │
├───────────────────────────────────────────────┤
│  Step 2  📐  Chiến Lược & Go-to-Market        │
│  14 MBA frameworks: SWOT, Porter, Blue Ocean  │
│  Lean Canvas, PESTEL, TAM/SAM/SOM, ...        │
├───────────────────────────────────────────────┤
│  Step 3  💰  Tài Chính & Scorecard            │
│  3 scenarios, P&L, cash flow, unit economics  │
│  Auto scorecard → GO / CONDITIONAL / NO-GO    │
├───────────────────────────────────────────────┤
│  Step 4  😈  Devil's Advocate                 │
│  Phản biện: assumptions, blind spots, stress  │
│  "Nếu bạn là đối thủ, bạn sẽ attack gì?"    │
├───────────────────────────────────────────────┤
│  Step 5  📝  Tổng Hợp Business Plan           │
│  13 sections, 5000+ words, citations          │
│  Download → /pitch → present!                 │
└───────────────────────────────────────────────┘
```

---

## 🧠 Điểm Khác Biệt

### 1. Grounded — Không Hallucinate
Mọi số liệu đều từ Google Search thực. Có `[Source](URL)`. Không bịa.

### 2. Framework-driven — Không Chung Chung
Áp **14 MBA frameworks** cụ thể. SWOT có TOWS matrix. Porter's có score 1-5. Financial có 3 scenarios.

### 3. Editable Knowledge Base
Sửa file `.md` trong `knowledge/frameworks/` → AI phân tích theo cách **bạn muốn**.

### 4. Bootstrap-aware
Vốn < 100 triệu? AI tự điều chỉnh — không đề cập gọi vốn, focus 1 người vận hành, organic marketing.

### 5. Devil's Advocate Thật
Không khen xã giao. 6 phần phản biện bắt buộc: assumptions, cross-check, đối thủ phản công, worst case, blind spots, stress test.

---

## 🔀 Antigravity Proxy (Recommended)

Pipeline gọi Gemini API ~15-20 lần/phiên → dễ bị **rate limit 429**. Antigravity Manager bypass hoàn toàn:

<details>
<summary>📖 Hướng dẫn setup (3 bước)</summary>

**1. Cài Antigravity Manager**
```
Download: https://github.com/lbjlaq/Antigravity-Manager
```

**2. Bật Proxy**
- Mở Antigravity Manager → Tab **API Proxy** → Bật **Dịch vụ**
- Copy **API Key** (dạng `sk-xxxx...`)

**3. Thêm vào `.env`**
```env
PROXY_API_KEY=sk-your_key_here
PROXY_BASE_URL=http://localhost:8045/v1
PROXY_MODEL=gemini-2.5-pro
```

Kết quả: `🔀 Routing via Antigravity proxy` — không bị 429.
</details>

---

## 🎛️ Web UI Features

| Feature | Mô tả |
|---|---|
| 📋 **4 Output Formats** | Full Plan · Pitch Deck · Lean Canvas · Go-to-Market |
| 🚀 **Quick Actions** | Pitch · GTM 90d · Tài chính · Đối thủ · Rủi ro |
| 📚 **Knowledge Base** | Edit 14 framework .md files real-time |
| 📊 **Scorecard** | Auto score + GO/NO-GO verdict |
| 🏭 **7 ngành** | Tech · F&B · Tourism · Education · Trading · E-com · XNK |
| 🌍 **3 thị trường** | Việt Nam · SEA · International |

---

## 📂 Project Structure

```
business-deep-research/
├── install.ps1 / install.sh    # ⚡ One-command installer
├── VERSION                     # Kit version (1.0.0)
├── workflows/                  # 🎮 Antigravity slash commands (6 files)
├── bdr_skills/                 # 🧠 AI Skills (2 skills)
├── app.py                      # FastAPI backend + SSE
├── pipeline.py                 # 5-step analysis engine
├── config.py                   # Industries, markets, frameworks
├── tools/
│   ├── gemini_search.py        # Search + Antigravity proxy
│   ├── search_cache.py         # 24h SQLite cache
│   └── output_validator.py     # Quality checker
├── knowledge/
│   ├── frameworks/ (14 files)  # MBA framework templates
│   ├── industries/             # Industry knowledge
│   └── markets/                # VN, SEA, International
├── web/                        # Next.js 15 frontend
├── start.bat / start.sh        # One-click run
└── .env.example                # Config template
```

---

## 🛠️ Tech Stack

| Layer | Tech | Tại sao |
|---|---|---|
| Backend | **FastAPI** | Async SSE native, 3x faster than Flask |
| Frontend | **Next.js 15** | Static export, React Server Components |
| AI | **Gemini 2.5 Pro** | Google Search grounding, 1M token |
| Proxy | **Antigravity Manager** | Bypass rate limit, multi-account |
| Cache | **SQLite** | 24h TTL, zero config |

---

## 📊 Roadmap

- [x] ⚡ **v1.0** — Startup Kit (1 lệnh cài, 6 slash commands, 2 AI skills)
- [ ] 📄 Export PDF / DOCX
- [ ] 🌐 Multi-language (EN, JP, KR)
- [ ] 👥 Team collaboration
- [ ] 🧩 Custom framework builder
- [ ] 🔔 Webhook (Slack, Discord)
- [ ] 🐳 Docker one-click deploy

---

## 🤝 Bạn muốn AI Agent tương tự?

| Bạn cần | Chúng tôi đã làm ✅ |
|---|---|
| AI phân tích thị trường | **Business Deep Research** — Bạn đang xem |
| AI tạo content marketing | **Em Content** — Auto content pipeline |
| AI quản lý xuất nhập khẩu | **Sourcing Agent** — Tìm xưởng, báo giá |
| AI trade tự động | **Trading Bot** — MT5 integration |

<div align="center">

### 🏢 Comarai — AI Automation Agency

> *"Bán thời gian làm việc nhàm chán cho AI. Giữ thời gian cho việc quan trọng."*

**4 nhân viên AI chạy 24/7:** 🤖 Em Sale · 📝 Em Content · 📊 Em Marketing · 📈 Em Trade

[![Yêu cầu Demo](https://img.shields.io/badge/🌐_Yêu_cầu_Demo-comarai.com-0066FF?style=for-the-badge)](https://comarai.com)
[![Zalo](https://img.shields.io/badge/💬_Zalo-0834422439-00B900?style=for-the-badge)](https://zalo.me/0834422439)
[![Email](https://img.shields.io/badge/📧_Email-Contact-EA4335?style=for-the-badge)](mailto:hungphamphunguyen@gmail.com)

**GitHub:** [github.com/hungpixi](https://github.com/hungpixi)

</div>

---

<div align="center">

**MIT License** — Tự do sử dụng, fork, chỉnh sửa. Credit appreciated.

Built with ❤️ by [hungpixi](https://github.com/hungpixi) × [Comarai](https://comarai.com)

</div>
