"""
Business Plan Pipeline v4 — Full improvements.
Changes vs v3:
- Interactive questionnaire → context file trước khi generate
- Devil's Advocate critical review step (step 4/5)
- Financial cross-validation
- Enforce 2 personas + 3 scenarios
- Search caching (24h TTL)
- URL resolver for redirect links
- Output validator
"""
import json
import re
import sys
import time
from datetime import datetime
from pathlib import Path
from tools.gemini_search import gemini_batch_search, gemini_deep_research, gemini_analyze
from tools.output_validator import validate_output, format_validation_report
from utils import load_all_frameworks, load_industry, load_market
from config import INDUSTRY_FRAMEWORKS, INDUSTRIES, MARKETS


# ═══════════════════════════════════════════════
# PROGRESS TRACKER
# ═══════════════════════════════════════════════

class ProgressTracker:
    """Visual progress tracker for terminal output."""
    def __init__(self, total_steps: int = 5):
        self.total_steps = total_steps
        self.current_step = 0
        self.start_time = time.time()
        self.step_times = []
        self.step_names = [
            "Nghiên Cứu Thị Trường & Đối Thủ",
            "Chiến Lược & Go-to-Market",
            "Tài Chính & Chấm Điểm",
            "Devil's Advocate (Phản Biện)",
            "Tổng Hợp Business Plan",
        ]
    
    def _progress_bar(self, current, total, width=30):
        filled = int(width * current / total)
        bar = "█" * filled + "░" * (width - filled)
        percent = current / total * 100
        return f"[{bar}] {percent:.0f}%"
    
    def _elapsed(self):
        elapsed = time.time() - self.start_time
        mins = int(elapsed // 60)
        secs = int(elapsed % 60)
        return f"{mins:02d}:{secs:02d}"
    
    def start_step(self, step_num: int, name: str = ""):
        self.current_step = step_num
        step_start = time.time()
        self.step_times.append(step_start)
        
        step_name = name or self.step_names[step_num - 1]
        icons = ["📊", "📐", "💰", "😈", "📝"]
        icon = icons[step_num - 1] if step_num <= len(icons) else "🔄"
        
        print(f"\n{'━' * 60}")
        print(f"  {self._progress_bar(step_num - 1, self.total_steps)}  ⏱️ {self._elapsed()}")
        print(f"{'━' * 60}")
        print(f"  {icon} STEP {step_num}/{self.total_steps}: {step_name.upper()}")
        print(f"{'━' * 60}")
        
        # Show remaining steps
        for i in range(self.total_steps):
            if i < step_num - 1:
                print(f"    ✅ Step {i+1}: {self.step_names[i]}")
            elif i == step_num - 1:
                print(f"    ▶️ Step {i+1}: {self.step_names[i]} ← đang chạy")
            else:
                print(f"    ⬜ Step {i+1}: {self.step_names[i]}")
        print()
    
    def end_step(self, step_num: int):
        if self.step_times:
            step_duration = time.time() - self.step_times[-1]
            mins = int(step_duration // 60)
            secs = int(step_duration % 60)
            print(f"  ✅ Step {step_num} hoàn thành ({mins:02d}:{secs:02d})")
    
    def finish(self):
        total_elapsed = time.time() - self.start_time
        mins = int(total_elapsed // 60)
        secs = int(total_elapsed % 60)
        
        print(f"\n{'━' * 60}")
        print(f"  {self._progress_bar(self.total_steps, self.total_steps)}  ⏱️ {mins:02d}:{secs:02d}")
        print(f"{'━' * 60}")
        print(f"  🎉 TẤT CẢ 5 STEPS ĐÃ HOÀN THÀNH!")
        print(f"  ⏱️  Tổng thời gian: {mins} phút {secs} giây")
        print(f"{'━' * 60}")

_tracker = ProgressTracker()


# ═══════════════════════════════════════════════
# INTERACTIVE QUESTIONNAIRE (hỏi user trước khi chạy)
# ═══════════════════════════════════════════════

def interactive_questionnaire(idea: str, industry: str, market: str) -> dict:
    """Hỏi user chi tiết trước khi tạo plan. Trả về context dict."""
    print("\n" + "="*60)
    print("📋 TRƯỚC KHI BẮT ĐẦU — Hãy trả lời nhanh 5 câu hỏi")
    print("   (Enter để bỏ qua, agent sẽ tự quyết định)")
    print("="*60)
    
    ctx = {
        "business_idea": idea,
        "industry": industry,
        "market": market,
        "project_name": "",
        "pricing": {},
        "budget_vnd": 50_000_000,
        "team_size": 1,
        "constraints": [],
        "target_customers": "",
        "revenue_goal": "",
        "needs_fundraising": False,
        "is_bootstrap": True,
    }
    
    # Q1: Tên dự án
    name = input("\n1️⃣  Tên dự án (VD: ZenChat AI): ").strip()
    if name:
        ctx["project_name"] = name
    
    # Q2: Vốn đầu tư
    budget_str = input("2️⃣  Vốn ban đầu (triệu VND, VD: 50): ").strip()
    if budget_str:
        try:
            ctx["budget_vnd"] = int(budget_str) * 1_000_000
        except ValueError:
            pass
    
    # Q3: Pricing
    pricing_str = input("3️⃣  Pricing (VD: free,199000,499000 hoặc Enter để tự động): ").strip()
    if pricing_str:
        tiers = pricing_str.split(",")
        tier_names = ["free", "basic", "pro", "premium"]
        for i, t in enumerate(tiers):
            try:
                ctx["pricing"][tier_names[min(i, len(tier_names)-1)]] = int(t.strip())
            except ValueError:
                pass
    
    # Q4: Khách hàng mục tiêu
    target = input("4️⃣  Khách hàng mục tiêu (VD: chủ shop online, spa, SME <10 người): ").strip()
    if target:
        ctx["target_customers"] = target
    
    # Q5: Constraints / yêu cầu đặc biệt
    constraints = input("5️⃣  Yêu cầu đặc biệt (VD: không gọi vốn, chỉ organic marketing): ").strip()
    if constraints:
        ctx["constraints"] = [c.strip() for c in constraints.split(",")]
    
    # Auto-detect modes
    if ctx["budget_vnd"] < 100_000_000:
        ctx["is_bootstrap"] = True
    
    idea_lower = idea.lower()
    ctx["needs_fundraising"] = any(w in idea_lower for w in [
        "gọi vốn", "investor", "funding", "seed", "series", "vc", "angel"
    ])
    
    print(f"\n{'='*60}")
    print("✅ Context đã thiết lập:")
    if ctx["project_name"]:
        print(f"   📌 Tên: {ctx['project_name']}")
    print(f"   💰 Vốn: {ctx['budget_vnd'] / 1_000_000:.0f} triệu VND")
    if ctx["pricing"]:
        print(f"   💵 Pricing: {ctx['pricing']}")
    if ctx["target_customers"]:
        print(f"   🎯 Target: {ctx['target_customers']}")
    if ctx["constraints"]:
        print(f"   ⚠️ Constraints: {', '.join(ctx['constraints'])}")
    print(f"   🏃 Mode: {'BOOTSTRAP' if ctx['is_bootstrap'] else 'INVESTOR'}")
    print("="*60)
    
    return ctx


def load_context_file(path: str) -> dict:
    """Load context từ JSON file."""
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        print(f"  ⚠️ Cannot load context file: {e}")
        return {}


# ═══════════════════════════════════════════════
# SCORING PROMPTS
# ═══════════════════════════════════════════════

def _get_scoring_prompt(ctx: dict) -> str:
    if ctx.get("is_bootstrap") and not ctx.get("needs_fundraising"):
        return """
### Bảng Chấm Điểm Khởi Nghiệp Bootstrap (10 tiêu chí)
Đánh giá dưới góc nhìn FOUNDER TỰ THÂN VẬN ĐỘNG.

| Tiêu chí | Trọng số | Điểm (1-10) | Weighted | Lý do |
| :--- | :--- | :--- | :--- | :--- |
| **1. Khả thi với vốn hiện có** | 15% | | | |
| **2. Time to First Revenue** | 15% | | | |
| **3. 1 người vận hành được không?** | 15% | | | |
| **4. Demand thực tế (PMF Signal)** | 10% | | | |
| **5. Unit Economics** | 10% | | | |
| **6. Competitive Moat** | 10% | | | |
| **7. Scalability tiềm năng** | 5% | | | |
| **8. Rủi ro thất bại** | 10% | | | |
| **9. Fit với năng lực Founder** | 5% | | | |
| **10. Thời điểm thị trường** | 5% | | | |

**VERDICT: GO / CONDITIONAL GO / NO-GO**
KHÔNG đề cập gọi vốn, VC, nhà đầu tư.
"""
    else:
        return """
### Investment Decision Matrix (10 tiêu chí)
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
"""


def _context_to_prompt_notes(ctx: dict) -> str:
    """Convert user context → prompt constraints."""
    notes = []
    
    if ctx.get("project_name"):
        notes.append(f"- Tên dự án bắt buộc: **{ctx['project_name']}** (KHÔNG được đặt tên khác)")
    
    if ctx.get("pricing"):
        p = ctx["pricing"]
        pricing_str = ", ".join(f"{k}: {v:,} VND" for k, v in p.items())
        notes.append(f"- Pricing CỐ ĐỊNH: {pricing_str} (PHẢI dùng giá này trong TẤT CẢ sections)")
    
    if ctx.get("target_customers"):
        notes.append(f"- Khách hàng mục tiêu: {ctx['target_customers']}")
    
    if ctx.get("constraints"):
        for c in ctx["constraints"]:
            notes.append(f"- Constraint: {c}")
    
    budget = ctx.get("budget_vnd", 50_000_000)
    notes.append(f"- Vốn ban đầu: {budget:,.0f} VND ({budget / 1_000_000:.0f} triệu)")
    
    if ctx.get("is_bootstrap") and not ctx.get("needs_fundraising"):
        notes.append("- Mode: BOOTSTRAP — KHÔNG đề cập gọi vốn, VC, nhà đầu tư")
    
    return "\n".join(notes) if notes else ""


# ═══════════════════════════════════════════════
# PIPELINE STEPS
# ═══════════════════════════════════════════════

def step_research(business_idea: str, industry: str, market: str, ctx: dict) -> str:
    """Step 1: Market Research + Competitors (2 batch calls)."""
    _tracker.start_step(1)
    
    ind_name = INDUSTRIES.get(industry, industry)
    mkt_name = MARKETS.get(market, market)
    target = ctx.get("target_customers", "SME")
    advantages = ctx.get("competitive_advantages", [])
    idea_keywords = business_idea[:100]
    
    print("  🔎 Batch 1: Nghiên cứu thị trường...")
    batch1 = [
        f"Quy mô thị trường {ind_name} tại {mkt_name} 2024-2026, CAGR, dự báo tăng trưởng, market size",
        f"Nhu cầu của {target} tại {mkt_name} 2025, chi tiêu cho công nghệ giáo dục, chuyển đổi số",
        f"Xu hướng AI trong {ind_name} tại {mkt_name} 2025 2026: {idea_keywords}, adoption rate benchmark",
        f"Chính sách hỗ trợ startup công nghệ {mkt_name} 2025, quy định pháp lý EdTech, bảo vệ dữ liệu",
    ]
    
    result1 = gemini_batch_search(batch1, topic=f"Thị trường {ind_name} tại {mkt_name}")
    
    print("  🔎 Batch 2: Phân tích đối thủ & chi phí...")
    batch2 = [
        f"Top đối thủ cạnh tranh cho {target} trong ngành {ind_name} {mkt_name} 2025: so sánh pricing features strengths weaknesses",
        f"Đối thủ quốc tế trong ngành {ind_name}: {idea_keywords}, so sánh giá tính năng, điểm yếu tại {mkt_name}",
        f"Hành vi chi tiêu của {target} {mkt_name}, willingness to pay cho sản phẩm {ind_name}, channels preferred",
        f"Chi phí cloud hosting API AI 3D rendering cho startup {mkt_name} 2025, pricing tiers cho MVP",
    ]
    
    result2 = gemini_batch_search(batch2, topic=f"Đối thủ & Chi phí {ind_name}")
    
    _tracker.end_step(1)
    return f"## Market Research\n{result1}\n\n## Competitor & Cost Research\n{result2}"


def step_strategy_gtm(business_idea: str, industry: str, market: str,
                      ctx: dict, research_data: str) -> str:
    """Step 2: Strategy + GTM (1 batch + 1 analysis)."""
    _tracker.start_step(2)
    
    ind_name = INDUSTRIES.get(industry, industry)
    framework_names = INDUSTRY_FRAMEWORKS.get(industry, INDUSTRY_FRAMEWORKS["tech_startup"])
    frameworks_knowledge = load_all_frameworks(framework_names)
    ctx_notes = _context_to_prompt_notes(ctx)
    
    batch = [
        f"Go-to-market strategy SaaS startup bootstrapped {MARKETS.get(market)} 2025, PLG channels CAC",
        f"Content marketing SEO cho SaaS startup {MARKETS.get(market)}, freemium conversion benchmark",
        f"Blue ocean cơ hội thị trường ngách SaaS micro-SME {MARKETS.get(market)}, underserved",
        f"SaaS metrics benchmark 2025: gross margin, churn, freemium conversion, LTV/CAC",
    ]
    print("  🔎 Searching GTM benchmarks...")
    search_data = gemini_batch_search(batch, topic="Strategy & GTM benchmarks")
    
    analysis_prompt = f"""
Bạn là cựu Partner McKinsey + CMO 15 năm scale SaaS.

**Ý tưởng:** {business_idea}
**Ngành:** {ind_name}

## CONTEXT TỪ USER (BẮT BUỘC TUÂN THỦ):
{ctx_notes}

## MBA Frameworks:
{frameworks_knowledge[:4000]}

## Yêu cầu:

### A. STRATEGIC ANALYSIS
1. **Lean Canvas**: 9 blocks, 3-5 bullet mỗi block
2. **SWOT Matrix**: 6+ items/quadrant, TOWS strategies (2/quadrant)
3. **Porter's Five Forces**: Score 1-5, evidence
4. **PESTEL**: Top 3 factors, scoring Impact x Likelihood
5. **Blue Ocean ERRC Grid**: 3-5 mỗi cột

### B. GO-TO-MARKET (chi tiết theo tháng)
1. **GTM Phases** (week-by-week 3 tháng đầu)
2. **Acquisition by Channel**: CAC per channel
3. **Content & SEO**: 10 keywords, calendar
4. **Pricing**: Tier structure (DÙNG GIÁ TỪ CONTEXT NẾU CÓ)

### C. CUSTOMER PERSONAS (BẮT BUỘC 2 PERSONAS KHÁC NHAU)
- Persona 1 và Persona 2 cho 2 segments khác nhau
- Mỗi persona: Demographics, Pains (trích dẫn lời nói), Gains, Willingness to pay

## QUY TẮC:
- Viết tiếng Việt | Tables markdown | Thực tế cho bootstrap 1 người
"""
    
    print("  🧠 Analyzing with Gemini Pro...")
    report = gemini_analyze(analysis_prompt, context=f"## Research:\n{research_data[:4000]}\n\n## Search:\n{search_data}")
    _tracker.end_step(2)
    return report


def step_financials(business_idea: str, industry: str, market: str,
                    ctx: dict, research_data: str) -> str:
    """Step 3: Financial Analysis + Scoring."""
    _tracker.start_step(3)
    
    budget = ctx.get("budget_vnd", 50_000_000)
    budget_display = f"{budget / 1_000_000:.0f} triệu VND"
    ctx_notes = _context_to_prompt_notes(ctx)
    scoring = _get_scoring_prompt(ctx)
    
    batch = [
        f"Chi phí khởi nghiệp SaaS startup {MARKETS.get(market)} 2025: hosting, tools, marketing",
        f"SaaS revenue projection benchmark Year 1-3 monthly MRR growth early stage",
        f"Thuế doanh nghiệp {MARKETS.get(market)} 2025, ưu đãi startup công nghệ",
    ]
    print("  🔎 Searching financial benchmarks...")
    benchmark_data = gemini_batch_search(batch, topic="Financial benchmarks")
    fin_frameworks = load_all_frameworks(["financial_projections", "investment_analysis"])
    
    analysis_prompt = f"""
Bạn là CFA kiêm serial entrepreneur. Xây dựng MÔ HÌNH TÀI CHÍNH:

**Ý tưởng:** {business_idea}
**Vốn:** {budget_display}

## CONTEXT BẮT BUỘC:
{ctx_notes}

## Financial Frameworks:
{fin_frameworks[:3000]}

## Yêu cầu (TẤT CẢ BẢNG MARKDOWN):

### 1. Assumptions Table
### 2. Revenue Projections — **3 SCENARIOS bắt buộc**
- MONTHLY cho Year 1, ANNUAL Y2-Y3
- **Pessimistic / Base / Optimistic** (3 cột riêng, KHÔNG được bỏ)

### 3. P&L Statement (bảng)
### 4. Cash Flow (Monthly Year 1) — show runway
### 5. Unit Economics: CAC, LTV, LTV/CAC, Payback
  - NẾU CAC = 0 (organic), phải ghi rõ: "CAC = 0 (sweat equity, opportunity cost ~X triệu/tháng)"
### 6. Break-Even: tháng cụ thể, customers cụ thể
### 7. Investment Metrics: NPV, IRR, ROI, Payback (show formula)
### 8. Sensitivity ±20%
### 9. Chấm điểm:
{scoring}
### 10. Risk Assessment (Top 7)

## QUY TẮC:
- Conservative assumptions
- PRICING TỪ CONTEXT NẾU CÓ (không tự đặt giá khác)
- Currency = VND, show calculation
- Verdict decisive, dựa trên data
"""
    
    print("  🧠 Analyzing financials with Gemini Pro...")
    report = gemini_analyze(analysis_prompt, context=f"## Benchmarks:\n{benchmark_data}\n\n## Research:\n{research_data[:3000]}")
    _tracker.end_step(3)
    return report


def step_devils_advocate(business_idea: str, ctx: dict, all_analysis: str) -> str:
    """Step 4: Devil's Advocate — phản biện và tìm lỗi."""
    _tracker.start_step(4)
    
    prompt = f"""
Bạn là DEVIL'S ADVOCATE. Công việc duy nhất: TÌM LỖI và THÁCH THỨC.
Bạn KHÔNG được đồng ý hay khen. Bạn chỉ được PHÊ BÌNH.

**Ý tưởng đang phân tích:** {business_idea}

## Yêu cầu (PHẢI ĐỦ 6 PHẦN):

### 1. 🚩 Top 5 Assumptions Nguy Hiểm Nhất
- Liệt kê 5 giả định trong plan mà NẾU SAI sẽ LÀM SỤP toàn bộ mô hình
- Mỗi assumption: tại sao nguy hiểm + xác suất sai + hậu quả

### 2. 🔍 Cross-check 3 Số Liệu Đáng Ngờ
- Tìm 3 con số/claim trong plan có thể SAI hoặc MISLEADING
- Giải thích tại sao đáng ngờ và cần verify

### 3. ⚔️ Nếu BẠN Là Đối Thủ
- Bạn sẽ attack ở ĐÂU? Chiến lược gì để "giết" dự án này?
- 3 kịch bản đối thủ phản công cụ thể

### 4. 💀 Worst Case Scenario
- Kịch bản xấu nhất: timeline, khi nào hết tiền, hậu quả
- "Nếu KHÔNG có khách hàng nào sau 6 tháng thì sao?"

### 5. 👁️ Blind Spots (Điểm Mù)
- 3-5 rủi ro/vấn đề mà founder CHƯA NHẬN RA
- Psychological biases phổ biến của founder solo

### 6. 🏋️ Stress Test
- Nếu churn rate = 10% (gấp đôi giả định) → revenue Y1 = ?
- Nếu conversion rate = 1% (giảm nửa) → bao lâu hòa vốn?
- Nếu đối thủ lớn ra tính năng tương tự miễn phí → strategy?

## QUY TẮC:
- THẲNG THẮN, KHÔNG NỂ, KHÔNG LẠC QUAN
- Mỗi phê bình CÓ DỮ LIỆU hoặc LOGIC rõ ràng
- Kết luận: "Rủi ro lớn nhất theo tôi là..."
"""
    
    print("  🧠 Running Devil's Advocate analysis...")
    report = gemini_analyze(prompt, context=all_analysis[:8000])
    _tracker.end_step(4)
    return report


def step_final_synthesis(business_idea: str, industry: str, market: str,
                         ctx: dict, all_sections: dict) -> str:
    """Step 5: Final synthesis with cross-validation."""
    _tracker.start_step(5)
    
    ind_name = INDUSTRIES.get(industry, industry)
    mkt_name = MARKETS.get(market, market)
    budget = ctx.get("budget_vnd", 50_000_000)
    budget_display = f"{budget / 1_000_000:.0f} triệu VND"
    timestamp = datetime.now().strftime("%d/%m/%Y")
    ctx_notes = _context_to_prompt_notes(ctx)
    
    try:
        industry_knowledge = load_industry(industry)[:2000]
    except FileNotFoundError:
        industry_knowledge = ""
    
    project_name_note = ""
    if ctx.get("project_name"):
        project_name_note = f"# {ctx['project_name']} - Business Plan"
    else:
        project_name_note = "# [TÊN DỰ ÁN] - Business Plan"
    
    synthesis_prompt = f"""
Bạn là Senior Business Plan Writer. TỔNG HỢP thành business plan hoàn chỉnh.

**Ý tưởng:** {business_idea}
**Ngành:** {ind_name} | **Thị trường:** {mkt_name}
**Vốn:** {budget_display} | **Ngày:** {timestamp}

## CONTEXT BẮT BUỘC — TUÂN THỦ TUYỆT ĐỐI:
{ctx_notes}

## STRUCTURE (13 sections):

{project_name_note}

## Executive Summary (Key Metrics TABLE, compelling narrative)
## 1. Company Description (Vision, Mission, Problem, Solution)
## 2. Market Analysis (TAM/SAM/SOM TABLE, **2 Personas**, 7+ Trends)
## 3. Competitive Analysis (Competitor TABLE, Positioning, Advantages)
## 4. Business Model (Lean Canvas TABLE, Revenue, Pricing TABLE — DÙNG GIÁ TỪ CONTEXT)
## 5. Strategic Analysis (SWOT TABLE, TOWS, Porter TABLE, PESTEL, ERRC Grid TABLE)
## 6. Go-to-Market Strategy (Phases by month, Channels TABLE, Content plan)
## 7. Operations Plan (Tech Stack TABLE, Team timeline, Milestones TABLE)
## 8. Financial Projections
   - Assumptions TABLE
   - Revenue TABLE: **3 SCENARIOS (Pessimistic/Base/Optimistic) — MONTHLY Y1**
   - P&L TABLE
   - Cash Flow TABLE
   - Unit Economics TABLE
   - Break-Even
## 9. Quyết Định & Chấm Điểm (Decision Matrix TABLE, VERDICT bold)
## 10. 😈 Devil's Advocate — Phản Biện & Thách Thức
   - Giữ NGUYÊN NỘI DUNG phản biện, KHÔNG LÀM NHẸ ĐI
## 11. Implementation Roadmap TABLE
## 12. Risk Management TABLE (7+ risks)
## 13. Appendix (Legal checklist, Assumptions, Sources & References URLs)

## QUY TẮC:
1. GIỮ NGUYÊN [Source](URL) citations
2. GIỮ NGUYÊN data cụ thể
3. PRICING PHẢI NHẤT QUÁN across ALL sections (dùng từ context)
4. Tables markdown nhiều nhất
5. Tối thiểu 5000 words
6. Devil's Advocate section KHÔNG ĐƯỢC LÀM MỀM — giữ nguyên sự thẳng thắn
7. Sources section liệt kê TẤT CẢ URLs
"""
    
    combined = ""
    for name, content in all_sections.items():
        combined += f"\n{'='*30}\n## {name}\n{'='*30}\n{content}"
    
    print("  🧠 Synthesizing final business plan with Gemini Pro...")
    report = gemini_analyze(synthesis_prompt, context=combined)
    _tracker.end_step(5)
    _tracker.finish()
    return report


# ═══════════════════════════════════════════════
# MAIN PIPELINE
# ═══════════════════════════════════════════════

def run_pipeline(business_idea: str, industry: str = "tech_startup",
                 market: str = "vietnam", context_file: str = None,
                 interactive: bool = True) -> str:
    """
    Pipeline v4: 5 steps, ~9-10 API calls.
    With questionnaire, Devil's Advocate, cross-validation, caching.
    """
    ind_name = INDUSTRIES.get(industry, industry)
    mkt_name = MARKETS.get(market, market)
    
    # Build context
    if context_file:
        ctx = load_context_file(context_file)
        ctx.setdefault("business_idea", business_idea)
        ctx.setdefault("industry", industry)
        ctx.setdefault("market", market)
        ctx.setdefault("budget_vnd", 50_000_000)
        ctx.setdefault("is_bootstrap", ctx.get("budget_vnd", 50_000_000) < 100_000_000)
        ctx.setdefault("needs_fundraising", False)
    elif interactive:
        ctx = interactive_questionnaire(business_idea, industry, market)
    else:
        # Non-interactive fallback
        ctx = {
            "business_idea": business_idea,
            "industry": industry,
            "market": market,
            "project_name": "",
            "pricing": {},
            "budget_vnd": 50_000_000,
            "team_size": 1,
            "constraints": [],
            "target_customers": "",
            "needs_fundraising": False,
            "is_bootstrap": True,
        }
        # Auto-detect from idea text
        idea_lower = business_idea.lower()
        import re
        budget_match = re.search(r'(\d+)\s*(?:triệu|tr|trieu)', idea_lower)
        if budget_match:
            ctx["budget_vnd"] = int(budget_match.group(1)) * 1_000_000
        if ctx["budget_vnd"] < 100_000_000:
            ctx["is_bootstrap"] = True
    
    mode = "🏃 BOOTSTRAP" if ctx.get("is_bootstrap") else "💼 INVESTOR"
    
    # Reset tracker
    global _tracker
    _tracker = ProgressTracker()
    
    print(f"\n{'='*60}")
    print(f"🚀 BUSINESS DEEP RESEARCH AGENT v4")
    print(f"{'='*60}")
    print(f"📌 Ý tưởng:    {business_idea}")
    if ctx.get("project_name"):
        print(f"📛 Tên dự án:  {ctx['project_name']}")
    print(f"🏢 Ngành:      {ind_name}")
    print(f"🌍 Thị trường: {mkt_name}")
    print(f"💰 Vốn:        {ctx.get('budget_vnd', 50_000_000) / 1_000_000:.0f} triệu VND")
    if ctx.get("pricing"):
        print(f"💵 Pricing:    {ctx['pricing']}")
    print(f"🎯 Mode:       {mode}")
    print(f"🔍 Engine:     Gemini + Google Search (batched, cached, URL-resolved)")
    print(f"{'='*60}")
    print(f"⏱️  5 steps: Research → Strategy → Financial → Devil's Advocate → Synthesis")
    print(f"{'='*60}\n")
    
    # Step 1: Research
    research = step_research(business_idea, industry, market, ctx)
    
    # Step 2: Strategy + GTM
    strategy = step_strategy_gtm(business_idea, industry, market, ctx, research)
    
    # Step 3: Financial + Scoring
    financials = step_financials(business_idea, industry, market, ctx, research)
    
    # Step 4: Devil's Advocate
    all_analysis = f"{research[:3000]}\n{strategy[:3000]}\n{financials[:3000]}"
    devils = step_devils_advocate(business_idea, ctx, all_analysis)
    
    # Step 5: Final synthesis
    all_sections = {
        "Market Research & Competitors": research,
        "Strategic Analysis & Go-to-Market": strategy,
        "Financial Analysis & Decision": financials,
        "Devil's Advocate (Phản Biện)": devils,
    }
    
    final_plan = step_final_synthesis(business_idea, industry, market, ctx, all_sections)
    
    # Post-processing: validate output
    issues = validate_output(final_plan)
    if issues:
        print(f"\n{'='*60}")
        print("⚠️ OUTPUT VALIDATION REPORT:")
        for issue in issues:
            print(f"  {issue}")
        print("="*60)
    else:
        print("\n  ✅ Output validation passed — no issues found")
    
    return final_plan
