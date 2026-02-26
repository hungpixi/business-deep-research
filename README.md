# 🚀 Business Deep Research Agent v4

> AI-powered business plan generator sử dụng Gemini API + Google Search Grounding để tạo kế hoạch kinh doanh chi tiết, có dẫn chứng thực tế và phản biện thẳng thắn.

[![Python](https://img.shields.io/badge/Python-3.11+-blue.svg)](https://python.org)
[![Gemini API](https://img.shields.io/badge/Gemini-2.0_Flash-orange.svg)](https://ai.google.dev)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

## 🎯 Vấn đề cần giải quyết

Các tool tạo business plan hiện tại (ChatGPT, Gemini chat) có 3 vấn đề lớn:

1. **Không có dữ liệu thực** — sinh ra số liệu chung chung, không verify được
2. **Thiếu phản biện** — luôn khen ý tưởng, không chỉ ra rủi ro thật sự
3. **Không nhất quán** — pricing, tên dự án thay đổi mỗi lần chạy

## 💡 Giải pháp: Pipeline 5 bước

```
📋 Questionnaire → 📊 Research → 📐 Strategy → 💰 Financial → 😈 Devil's Advocate → 📝 Synthesis
```

| Bước | Engine | Output |
|---|---|---|
| **1. Research** | Gemini Flash + Google Search grounding | Market data + competitor analysis với URL citations |
| **2. Strategy** | Gemini Pro + MBA frameworks (12 frameworks) | SWOT, Porter, PESTEL, Blue Ocean, Lean Canvas |
| **3. Financial** | Gemini Pro + context injection | 3 scenarios (Pessimistic/Base/Optimistic) monthly |
| **4. Devil's Advocate** | Gemini Pro (dedicated critical review) | Top 5 dangerous assumptions, worst case, blind spots |
| **5. Synthesis** | Gemini Pro + cross-validation | 48KB+ business plan, 13 sections, ~490 dòng |

## 🧠 Quá trình tư duy & Điểm khác biệt

### So với Deep Research của Google
| | Google Deep Research | Business Deep Research Agent |
|---|---|---|
| **Mục đích** | General research | **Chuyên biệt cho business plan** |
| **Framework** | Không | **12 MBA frameworks** (Harvard, FTU, UEH) |
| **Scoring** | Không | **Decision matrix 10 tiêu chí** (GO/NO-GO) |
| **Devil's Advocate** | Không | ✅ Phản biện thẳng thắn |
| **Context control** | Không | ✅ `context.json` lock pricing/name/constraints |
| **Bootstrap mode** | Không | ✅ Auto-detect khi vốn < 100M VND |

### So với ChatGPT / Gemini chat thông thường
| | Chat thông thường | Business Deep Research Agent |
|---|---|---|
| **Data** | Kiến thức cũ, không search | **Real-time Google Search** với URL citations |
| **Consistency** | Mỗi lần ra kết quả khác | ✅ **Context file** lock input |
| **Financial model** | 1 scenario chung chung | ✅ **3 scenarios monthly**, P&L, Cash Flow |
| **Bias** | Confirm bias (luôn khen) | ✅ **Devil's Advocate** tìm lỗi, phản biện |
| **Sources** | Không có | ✅ **Inline [1](url) citations** |

### Bài học từ quá trình phát triển (v1 → v4)

**v1 (CrewAI):** Dùng CrewAI abstraction → output chung chung, không có URL, thiếu data.
> *Bài học: Abstraction layers giảm control. Cần trực tiếp điều khiển prompt.*

**v2 (Direct Gemini):** Bỏ CrewAI, dùng trực tiếp Gemini API → tốt hơn nhưng không nhất quán.
> *Bài học: Mỗi step chạy riêng rẽ → pricing mâu thuẫn giữa các sections.*

**v3 (Batched + Rate Limited):** Gộp 4 queries → 1 call, thêm retry logic → giảm 429 errors.
> *Bài học: Free tier rate limit rất nghiêm ngặt. Cần cache và batch.*

**v4 (Full Pipeline):** Thêm questionnaire, Devil's Advocate, context injection, output validator.
> *Bài học: User context là critical. Không có nó, AI sẽ tự sáng tạo (và mâu thuẫn).*

## 🚀 Quick Start

### 1. Clone & Install
```bash
git clone https://github.com/hungpixi/business-deep-research.git
cd business-deep-research
pip install -r requirements.txt
```

### 2. Setup API Key
```bash
cp .env.example .env
# Edit .env và thêm GEMINI_API_KEY
```

### 3. Chạy

```bash
# Interactive mode (hỏi 5 câu trước khi chạy)
python main.py --idea "AI chatbot cho SME Việt Nam, vốn 50 triệu" --industry tech_startup

# Với context file (lock pricing, tên, constraints)
python main.py --idea "..." --context context.json --no-interactive

# Dry run (test API key)
python main.py --idea "test" --dry-run

# Clear search cache
python main.py --clear-cache
```

### 4. Ngành hỗ trợ
```
tech_startup     → Startup Công Nghệ
trading_finance  → Trading & Tài Chính
fnb              → F&B (Nhà Hàng / Quán Cà Phê)
education        → Giáo Dục (Mầm Non)
tourism          → Du Lịch & Lữ Hành
ecommerce        → Thương Mại Điện Tử
export_import    → Xuất Nhập Khẩu
```

## 📁 Cấu trúc dự án

```
business-deep-research/
├── main.py                 # CLI entry point
├── pipeline.py             # 5-step pipeline orchestrator
├── config.py               # API keys, industry/market configs
├── utils.py                # Helper functions
├── context.json            # Sample context file
├── tools/
│   ├── gemini_search.py    # Gemini + Google Search + URL resolver
│   ├── search_cache.py     # File-based search cache (24h TTL)
│   └── output_validator.py # Cross-validation checker
├── knowledge/
│   ├── frameworks/         # 12 MBA frameworks (BMC, SWOT, Porter...)
│   ├── industries/         # Industry templates (tech, F&B, tourism...)
│   └── markets/            # Market context (Vietnam, SEA, International)
└── output/                 # Generated business plans (gitignored)
```

## 🔧 Technical Highlights

### Rate Limiting & Retry Logic
```python
# Token bucket rate limiter (2 RPM for free tier)
# Exponential backoff: 15s → 30s → 60s → 120s
_rate_limiter = RateLimiter(max_per_minute=2)
_retry_with_backoff(func, max_retries=4, base_delay=15.0)
```

### Google Search Grounding + Inline Citations
```python
# Official API docs pattern: groundingSupports + groundingChunks
# Chèn [1](url) vào đúng vị trí trong text
tools=[types.Tool(google_search=types.GoogleSearch())]
```

### URL Resolver
```python
# vertexaisearch.cloud.google.com/grounding-api-redirect/... → direct URL
def resolve_url(redirect_url):
    resp = requests.head(url, allow_redirects=True, timeout=5)
    return resp.url
```

### Context Injection
```python
# User constraints → injected into ALL prompts
# Đảm bảo pricing, tên dự án, constraints nhất quán across 5 steps
```

## 📊 Sample Output

Business plan output (~48KB):
- **13 sections** với tables chi tiết
- **2 customer personas** (demographics, pains, gains, willingness to pay)
- **3 revenue scenarios** monthly (Pessimistic/Base/Optimistic)
- **Decision matrix** 10 tiêu chí (GO/CONDITIONAL GO/NO-GO)
- **Devil's Advocate** — phản biện thẳng thắn, worst case, blind spots
- **Inline citations** [1](url) từ Google Search

## 🗺️ Roadmap & Hướng phát triển

- [ ] **Async parallel pipeline** — search steps chạy đồng thời
- [ ] **Streaming output** — từng section ra file ngay khi hoàn thành
- [ ] **Industry-specific search queries** — tách queries ra JSON per industry
- [ ] **PDF export** — from Markdown to styled PDF
- [ ] **Web UI** — Next.js frontend thay vì CLI
- [ ] **Multi-language** — English, Vietnamese, Chinese
- [ ] **Comparison mode** — so sánh 2-3 ý tưởng cùng lúc

## 📝 License

MIT License

## 👨‍💻 Author

**Phạm Phú Nguyễn Hưng** — [@hungpixi](https://github.com/hungpixi)

> Built with 🧠 AI-assisted development. Code là AI giúp, tư duy là của founder.
