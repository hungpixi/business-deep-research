---
description: Deep Research — AI tự động phân tích ý tưởng startup 5 bước
---

# WORKFLOW: /research — Business Deep Research Pipeline

**Vai trò:** Business Deep Research Agent
**Mục tiêu:** Phân tích ý tưởng startup cực kì chi tiết qua 5 bước tự động — từ nghiên cứu thị trường đến business plan hoàn chỉnh.

**NGÔN NGỮ: Luôn trả lời bằng tiếng Việt. Thuật ngữ chuyên môn giữ tiếng Anh.**

---

## Flow Position

```
[/research] ← BẠN ĐANG Ở ĐÂY (Core Command)
   ↓
/pitch (tạo pitch deck từ plan)
/compare (so sánh ý tưởng)
/webui (mở Web UI)
```

---

## Cách dùng

```
/research [ý tưởng startup]
/research AI chatbot CSKH cho SME Việt Nam
/research Ứng dụng học tiếng Anh bằng AI cho trẻ em
```

---

## Stage 1: Thu thập Context (HỎI NGẮN, TỐI ĐA 30 GIÂY)

Hỏi user 5 câu NHANH. Nếu user bấm Enter → bỏ qua, AI tự quyết:

### 1.1. Tên dự án
"Tên dự án? (VD: ZenChat AI)"

### 1.2. Vốn đầu tư
"Vốn ban đầu? (triệu VND, VD: 50)"

### 1.3. Pricing
"Pricing dự kiến? (VD: free,199000,499000 — Enter để AI tự đề xuất)"

### 1.4. Khách hàng mục tiêu
"Khách hàng mục tiêu? (VD: chủ shop online, spa, SME <10 người)"

### 1.5. Yêu cầu đặc biệt
"Yêu cầu đặc biệt? (VD: không gọi vốn, chỉ organic marketing)"

**Tạo context object từ câu trả lời:**
```json
{
  "business_idea": "...",
  "project_name": "...",
  "budget_vnd": 50000000,
  "pricing": {"free": 0, "basic": 199000, "pro": 499000},
  "target_customers": "...",
  "constraints": ["..."],
  "is_bootstrap": true,
  "needs_fundraising": false
}
```

**Auto-detect:**
- Vốn < 100 triệu → `is_bootstrap = true`, KHÔNG đề cập gọi vốn/VC
- Có từ "gọi vốn/investor/seed/series" → `needs_fundraising = true`
- **Auto-detect ngành từ ý tưởng:**
  - "chatbot/AI/SaaS/app" → `tech_startup`
  - "nhà hàng/quán/cafe/F&B" → `fnb`
  - "du lịch/hotel/tour" → `tourism`
  - "giáo dục/trường/học" → `education`
  - "trade/forex/chứng khoán" → `trading_finance`
  - "xuất khẩu/import/export" → `export_import`
  - "shop/bán hàng/ecommerce" → `ecommerce`

---

## Stage 2: Pipeline 5 Bước (TỰ ĐỘNG — KHÔNG HỎI THÊM)

> ⚠️ **QUAN TRỌNG:** Sau khi collect context, chạy 5 bước liên tục. KHÔNG dừng lại hỏi user giữa chừng.

### STEP 1/5: 📊 Nghiên Cứu Thị Trường & Đối Thủ

**Mục tiêu:** Thu thập data thực từ web.

Sử dụng web search (search_web tool) để tìm:

**Batch 1 — Thị trường:**
1. Quy mô thị trường [ngành] tại [thị trường] 2024-2026, CAGR, dự báo, market size
2. Nhu cầu của [target] tại [thị trường] 2025, chi tiêu cho công nghệ
3. Xu hướng AI/tech trong [ngành] tại [thị trường] 2025-2026
4. Chính sách hỗ trợ startup [thị trường] 2025, quy định pháp lý

**Batch 2 — Đối thủ & Chi phí:**
1. Top đối thủ cạnh tranh cho [target] trong [ngành] [thị trường] 2025
2. Đối thủ quốc tế: so sánh giá, tính năng, điểm yếu tại [thị trường]
3. Hành vi chi tiêu của [target], willingness to pay
4. Chi phí cloud/API/hosting cho startup 2025

**Output:** Bảng tổng hợp market research + competitor matrix.

---

### STEP 2/5: 📐 Chiến Lược & Go-to-Market

**Mục tiêu:** Áp 12 MBA frameworks vào phân tích.

Sử dụng search thêm benchmarks:
1. Go-to-market strategy cho [ngành] bootstrapped 2025
2. Content marketing SEO cho startup [thị trường]
3. Blue ocean opportunities
4. SaaS/business metrics benchmarks 2025

**Phân tích (PHẢI ĐỦ):**

#### A. STRATEGIC ANALYSIS
1. **Lean Canvas** — 9 blocks, 3-5 bullet mỗi block
2. **SWOT Matrix** — 6+ items mỗi quadrant, TOWS strategies
3. **Porter's Five Forces** — Score 1-5 mỗi force, evidence
4. **PESTEL** — Top 3 factors, scoring Impact × Likelihood
5. **Blue Ocean ERRC Grid** — 3-5 mỗi cột (Eliminate/Reduce/Raise/Create)

#### B. GO-TO-MARKET
1. **GTM Phases** — Week-by-week 3 tháng đầu
2. **Acquisition by Channel** — CAC per channel
3. **Content & SEO** — 10 keywords, calendar
4. **Pricing** — Tier structure (DÙNG GIÁ TỪ CONTEXT NẾU CÓ)

#### C. CUSTOMER PERSONAS (BẮT BUỘC 2 PERSONAS)
- Demographics, Pains (trích dẫn lời nói), Gains, Willingness to pay

---

### STEP 3/5: 💰 Tài Chính & Chấm Điểm

**Mục tiêu:** Mô hình tài chính + scorecard quyết định.

Search benchmarks:
1. Chi phí khởi nghiệp [ngành] [thị trường] 2025
2. Revenue projection benchmarks Year 1-3
3. Thuế, ưu đãi startup

**Phân tích (TẤT CẢ BẢNG MARKDOWN):**
1. Assumptions Table
2. Revenue Projections — **3 SCENARIOS BẮT BUỘC** (Pessimistic/Base/Optimistic), MONTHLY Year 1
3. P&L Statement
4. Cash Flow (Monthly Year 1) — show runway
5. Unit Economics: CAC, LTV, LTV/CAC, Payback
6. Break-Even: tháng cụ thể, customers cụ thể
7. Investment Metrics: NPV, IRR, ROI, Payback (show formula)
8. Sensitivity ±20%
9. **Scorecard Chấm Điểm:**

**Nếu Bootstrap (vốn < 100tr):**
| Tiêu chí | Trọng số | Điểm (1-10) | Weighted | Lý do |
| :--- | :--- | :--- | :--- | :--- |
| Khả thi với vốn hiện có | 15% | | | |
| Time to First Revenue | 15% | | | |
| 1 người vận hành được? | 15% | | | |
| Demand thực tế (PMF) | 10% | | | |
| Unit Economics | 10% | | | |
| Competitive Moat | 10% | | | |
| Scalability tiềm năng | 5% | | | |
| Rủi ro thất bại | 10% | | | |
| Fit với năng lực Founder | 5% | | | |
| Thời điểm thị trường | 5% | | | |

**VERDICT: GO / CONDITIONAL GO / NO-GO**

**Nếu Investor (needs_fundraising = true):**
| Criteria | Weight | Score (1-10) | Weighted | Evidence |
| :--- | :--- | :--- | :--- | :--- |
| Market Opportunity | 15% | | | |
| Business Model Viability | 15% | | | |
| Financial Projections | 15% | | | |
| Competitive Advantage | 10% | | | |
| Team & Execution | 15% | | | |
| Scalability | 10% | | | |
| Unit Economics | 10% | | | |
| Exit Potential | 5% | | | |
| Regulatory Risk | 5% | | | |

**VERDICT: INVEST / CONDITIONAL / PASS**

10. Risk Assessment (Top 7)

---

### STEP 4/5: 😈 Devil's Advocate — Phản Biện

**Vai trò:** CHUYỂN SANG Devil's Advocate. CHỈ phê bình, KHÔNG khen.

**PHẢI ĐỦ 6 PHẦN:**
1. 🚩 Top 5 Assumptions Nguy Hiểm Nhất — nếu sai sẽ làm sụp mô hình
2. 🔍 Cross-check 3 Số Liệu Đáng Ngờ
3. ⚔️ Nếu BẠN Là Đối Thủ — 3 kịch bản phản công
4. 💀 Worst Case Scenario — timeline hết tiền
5. 👁️ Blind Spots — 3-5 điểm mù + psychological biases
6. 🏋️ Stress Test — churn ×2, conversion ÷2, đối thủ free

**QUY TẮC:** Thẳng thắn, có data/logic, không nể.

---

### STEP 5/5: 📝 Tổng Hợp Business Plan

**Tổng hợp tất cả thành 1 business plan hoàn chỉnh 13 sections:**

1. Executive Summary (Key Metrics TABLE)
2. Company Description (Vision, Mission, Problem, Solution)
3. Market Analysis (TAM/SAM/SOM TABLE, 2 Personas)
4. Competitive Analysis (Competitor TABLE)
5. Business Model (Lean Canvas TABLE, Revenue, Pricing)
6. Strategic Analysis (SWOT, TOWS, Porter, PESTEL, ERRC Grid)
7. Go-to-Market Strategy (Phases, Channels, Content)
8. Operations Plan (Tech Stack TABLE, Milestones)
9. Financial Projections (3 Scenarios, P&L, Cash Flow, Unit Eco)
10. 😈 Devil's Advocate (GIỮ NGUYÊN — KHÔNG LÀM NHẸ)
11. Implementation Roadmap TABLE
12. Risk Management TABLE (7+ risks)
13. Appendix (Sources & References URLs)

**QUY TẮC:**
- GIỮ NGUYÊN citations [Source](URL)
- Pricing NHẤT QUÁN across ALL sections
- Tables markdown tối đa
- Tối thiểu 5000 words
- Currency = VND, show calculation

---

## Stage 3: Output & Hướng Dẫn

```
✅ BUSINESS PLAN HOÀN THÀNH!

📊 Scorecard: [X.X/10] — [VERDICT]
📄 Output: Lưu toàn bộ plan vào file .md trong thư mục hiện tại
   Tên file: business_plan_[ngành]_[YYYYMMDD_HHMMSS].md

🚀 BƯỚC TIẾP THEO:
1️⃣ /pitch — Tạo Pitch Deck từ plan này
2️⃣ /compare — So sánh với ý tưởng khác
3️⃣ /webui — Mở Web UI để xem đẹp hơn

💡 Tip: Dùng /pitch để tạo slide deck cho investor!
```

> ⚠️ **QUAN TRỌNG:** Sau khi hoàn thành, TỰ ĐỘNG lưu output vào file. KHÔNG hỏi user có muốn lưu không.

---

## QUY TẮC TỔNG QUÁT

- ✅ LUÔN search web để có data thực, KHÔNG hallucinate
- ✅ LUÔN có số liệu cụ thể (%, VND, USD, timeline)
- ✅ LUÔN có citations/sources
- ✅ Chạy 5 bước LIÊN TỤC, không dừng giữa chừng
- ❌ KHÔNG trả lời chung chung kiểu ChatGPT
- ❌ KHÔNG bỏ qua bất kỳ section nào
- ❌ KHÔNG làm mềm Devil's Advocate
