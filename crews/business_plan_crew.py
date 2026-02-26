"""
Business Plan Crew - Main pipeline orchestrating all agents.
Sequential workflow: Market Research → Strategy → Financials → Industry Check → Final Plan
"""
from crewai import Crew, Task, Process
from agents.market_researcher import create_market_researcher
from agents.strategy_analyst import create_strategy_analyst
from agents.financial_modeler import create_financial_modeler
from agents.industry_expert import create_industry_expert
from agents.plan_writer import create_plan_writer
from utils import load_all_frameworks, load_industry, load_market
from config import INDUSTRY_FRAMEWORKS, INDUSTRIES, MARKETS


def build_business_plan_crew(
    business_idea: str,
    industry: str = "tech_startup",
    market: str = "vietnam",
    use_pro_model: bool = False,
) -> Crew:
    """
    Build a CrewAI crew for generating a comprehensive business plan.
    
    Args:
        business_idea: Mô tả ý tưởng kinh doanh
        industry: Ngành (tech_startup, trading_finance, fnb, etc.)
        market: Thị trường (vietnam, international, sea)
        use_pro_model: Dùng Gemini Pro (chậm hơn nhưng chất lượng cao hơn)
    """
    # --- Load Knowledge ---
    framework_names = INDUSTRY_FRAMEWORKS.get(industry, INDUSTRY_FRAMEWORKS["tech_startup"])
    frameworks_knowledge = load_all_frameworks(framework_names)
    
    try:
        industry_knowledge = load_industry(industry)
    except FileNotFoundError:
        industry_knowledge = "No specific industry template available."
    
    try:
        market_knowledge = load_market(market)
    except FileNotFoundError:
        market_knowledge = "No specific market context available."
    
    industry_name = INDUSTRIES.get(industry, industry)
    market_name = MARKETS.get(market, market)
    
    # --- Create Agents ---
    market_researcher = create_market_researcher(use_pro_model)
    strategy_analyst = create_strategy_analyst(use_pro_model)
    financial_modeler = create_financial_modeler(use_pro_model)
    industry_expert = create_industry_expert(industry, use_pro_model)
    plan_writer = create_plan_writer(use_pro_model=True)  # Always use Pro for final writing
    
    # --- Define Tasks ---
    
    # Task 1: Market Research
    task_market_research = Task(
        description=f"""
        Nghiên cứu thị trường cho ý tưởng kinh doanh sau:
        
        **Ý tưởng:** {business_idea}
        **Ngành:** {industry_name}
        **Thị trường:** {market_name}
        
        **Context thị trường:**
        {market_knowledge}
        
        **Yêu cầu phân tích:**
        1. **Market Overview:** Tổng quan thị trường, kích thước, tốc độ tăng trưởng (CAGR)
        2. **TAM/SAM/SOM:** Ước tính cụ thể với số liệu (cả top-down và bottom-up)
        3. **Target Customers:** Customer persona chi tiết (demographics, psychographics, pain points)
        4. **Competitor Analysis:** Top 5-10 đối thủ cạnh tranh trực tiếp và gián tiếp
           - Tên, mô tả, pricing, strengths/weaknesses
           - Market share estimation
        5. **Market Trends:** 5-7 xu hướng chính ảnh hưởng đến ngành
        6. **Customer Insights:** Hành vi mua hàng, willingness to pay, channels ưa thích
        
        **QUAN TRỌNG:** Cung cấp số liệu cụ thể, có nguồn trích dẫn. Không đoán mò.
        Nếu không tìm được data chính xác, ghi rõ là estimate và methodology.
        """,
        expected_output=(
            "Báo cáo nghiên cứu thị trường chi tiết bao gồm: Market Overview, TAM/SAM/SOM "
            "với số liệu cụ thể, Customer Persona, Competitor Analysis (bảng so sánh), "
            "Market Trends, và Customer Insights. Tất cả có dẫn nguồn."
        ),
        agent=market_researcher,
    )
    
    # Task 2: Strategic Analysis
    task_strategic_analysis = Task(
        description=f"""
        Sử dụng các MBA frameworks sau để phân tích chiến lược cho ý tưởng:
        
        **Ý tưởng:** {business_idea}
        **Ngành:** {industry_name}
        **Thị trường:** {market_name}
        
        **MBA Frameworks cần áp dụng:**
        {frameworks_knowledge}
        
        **Yêu cầu:**
        1. **Business Model Canvas** (hoặc Lean Canvas nếu là startup): Điền đủ 9 blocks
        2. **SWOT Analysis + TOWS Matrix:** 
           - Mỗi quadrant ít nhất 5 items
           - TOWS: 2 strategies cho mỗi quadrant (SO, WO, ST, WT)
        3. **Porter's Five Forces:** Rate 1-5 mỗi force, tính tổng, kết luận
        4. **PESTEL Analysis:** Focus vào factors relevant nhất cho thị trường {market_name}
        5. **Blue Ocean Strategy (ERRC Grid):** Eliminate / Reduce / Raise / Create
        6. **Competitive Positioning Map:** Xác định white space
        
        **Sử dụng data từ Market Research để phân tích có cơ sở.**
        """,
        expected_output=(
            "Phân tích chiến lược toàn diện với: Business Model Canvas (9 blocks), "
            "SWOT Matrix (5+ items/quadrant) + TOWS strategies, Porter's 5 Forces (scored 1-5), "
            "PESTEL Analysis, Blue Ocean ERRC Grid, và Competitive Positioning. "
            "Mỗi framework có actionable insights."
        ),
        agent=strategy_analyst,
        context=[task_market_research],
    )
    
    # Task 3: Financial Analysis & Investment Decision
    task_financial_analysis = Task(
        description=f"""
        Xây dựng mô hình tài chính và phân tích đầu tư cho:
        
        **Ý tưởng:** {business_idea}
        **Ngành:** {industry_name}  
        **Thị trường:** {market_name}
        
        **Framework phân tích đầu tư:**
        {load_all_frameworks(["financial_projections", "investment_analysis"])}
        
        **Yêu cầu:**
        1. **Revenue Projections (3 năm):**
           - 3 scenarios: Pessimistic (25%), Base (50%), Optimistic (25%)
           - Revenue model rõ ràng với assumptions
        
        2. **Cost Structure:**
           - Fixed costs, variable costs, one-time costs
           - Burn rate hàng tháng
        
        3. **P&L Statement (3 năm):** 
           Revenue → Gross Profit → EBITDA → Net Income
        
        4. **Cash Flow Projections:**
           - Monthly cho Year 1, quarterly cho Year 2-3
           - Runway calculation
        
        5. **Unit Economics:**
           - CAC, LTV, LTV/CAC ratio
           - Gross margin by product/service
        
        6. **Investment Metrics:**
           - NPV (discount rate 15-20%)
           - IRR
           - ROI per year
           - Payback Period
           - Profitability Index
        
        7. **Break-Even Analysis:**
           - BEP in units and revenue
           - Months to break-even
        
        8. **Sensitivity Analysis:**
           - Key variables impact on NPV
           - Tornado diagram format
        
        9. **Investment Decision Matrix:**
           - Score 10 criteria (1-10 each, weighted)
           - Total weighted score
           - **VERDICT: INVEST / CONDITIONAL / PASS** với lý do chi tiết
        
        10. **Risk Assessment:**
            - Top 5 risks with probability và impact
            - Mitigation strategies
            - Sharpe-like risk/reward ratio
        
        **QUAN TRỌNG:** 
        - Dùng assumptions conservative (đừng quá lạc quan)
        - Tất cả số liệu phải có logic, trình bày bằng bảng
        - Kết luận đầu tư PHẢI rõ ràng và decisive
        - Áp dụng tư duy VC/PE khi đánh giá
        """,
        expected_output=(
            "Mô hình tài chính hoàn chỉnh bao gồm: Revenue Projections 3 năm (3 scenarios), "
            "P&L Statement, Cash Flow, Unit Economics, Investment Metrics (NPV, IRR, ROI, Payback), "
            "Break-Even Analysis, Sensitivity Analysis, Investment Decision Matrix với scoring, "
            "và VERDICT rõ ràng (INVEST/CONDITIONAL/PASS). Tất cả trình bày bằng bảng Markdown."
        ),
        agent=financial_modeler,
        context=[task_market_research, task_strategic_analysis],
    )
    
    # Task 4: Industry Expert Review
    task_industry_review = Task(
        description=f"""
        Review toàn bộ business plan dưới góc nhìn chuyên gia ngành {industry_name}:
        
        **Ý tưởng:** {business_idea}
        **Thị trường:** {market_name}
        
        **Industry Knowledge:**
        {industry_knowledge}
        
        **Yêu cầu review:**
        1. **Regulatory Compliance:** Giấy phép, quy định cần có
        2. **Industry Standards:** Chuẩn ngành (KPIs, SLAs, certifications)
        3. **Operational Requirements:** Yêu cầu vận hành đặc thù
        4. **Risk Factors:** Rủi ro đặc thù ngành
        5. **Success Factors:** Yếu tố thành công quan trọng nhất
        6. **Common Pitfalls:** Sai lầm phổ biến của người mới vào ngành
        7. **Timeline:** Realistic timeline để launch và đạt milestones
        8. **Resource Requirements:** Team size, skillsets cần thiết
        
        **Chỉ ra cụ thể những gì THIẾU hoặc CẦN ĐIỀU CHỈNH trong business plan.**
        """,
        expected_output=(
            "Industry expert review bao gồm: Regulatory checklist, Industry standards/metrics, "
            "Operational requirements, Industry-specific risks, Key success factors, "
            "Common pitfalls to avoid, Realistic timeline, và Resource requirements. "
            "Nêu rõ điều chỉnh cần thiết cho business plan."
        ),
        agent=industry_expert,
        context=[task_market_research, task_strategic_analysis, task_financial_analysis],
    )
    
    # Task 5: Final Business Plan Document
    task_write_plan = Task(
        description=f"""
        Tổng hợp TẤT CẢ phân tích trước đó thành MỘT business plan hoàn chỉnh, chuyên nghiệp.
        
        **Ý tưởng:** {business_idea}
        **Ngành:** {industry_name}
        **Thị trường:** {market_name}
        
        **Format yêu cầu:** Markdown document với cấu trúc sau:
        
        # [TÊN DỰ ÁN] - Business Plan
        
        ## Executive Summary
        - Tóm tắt 1-2 trang: ý tưởng, thị trường, mô hình, tài chính, verdict đầu tư
        - Investment Highlights (bullet points)
        - Key Metrics bảng tóm tắt
        
        ## 1. Company Description
        - Vision, Mission
        - Problem Statement
        - Solution Description
        - Founding Team (nếu có info)
        
        ## 2. Market Analysis
        - Market Overview & TAM/SAM/SOM
        - Customer Persona
        - Market Trends
        
        ## 3. Competitive Analysis
        - Competitor Comparison Matrix (bảng)
        - Competitive Positioning Map
        - Our Competitive Advantage
        
        ## 4. Business Model
        - Business Model Canvas (9 blocks, format bảng)
        - Revenue Model chi tiết
        - Pricing Strategy
        
        ## 5. Strategic Analysis
        - SWOT Matrix (format bảng 2x2)
        - TOWS Strategies
        - Porter's Five Forces (scored)
        - PESTEL Summary
        - Blue Ocean ERRC Grid
        
        ## 6. Marketing & Sales Strategy
        - Go-to-Market Plan
        - Customer Acquisition Strategy
        - Sales Channels
        - Marketing Budget Allocation
        
        ## 7. Operations Plan
        - Technology Stack / Infrastructure
        - Team Structure & Hiring Plan
        - Key Partnerships
        - Milestones & Timeline (Gantt-like)
        - Industry-Specific Requirements (licenses, compliance)
        
        ## 8. Financial Projections
        - Revenue Projections (3 scenarios, 3 years, bảng)
        - P&L Statement (bảng)
        - Cash Flow Projections  
        - Unit Economics (CAC, LTV, margins)
        - Break-Even Analysis
        - Funding Requirements
        
        ## 9. Investment Analysis & Decision
        - NPV, IRR, ROI Summary (bảng)
        - Investment Decision Matrix (10 criteria, scored, weighted)
        - Sensitivity Analysis
        - Risk Assessment Matrix
        - **INVESTMENT VERDICT: [INVEST / CONDITIONAL / PASS]**
        - Lý do chi tiết cho verdict
        
        ## 10. Implementation Roadmap
        - Phase 1: MVP (Month 1-3)
        - Phase 2: Launch & Validation (Month 4-6)
        - Phase 3: Growth (Month 7-12)
        - Phase 4: Scale (Year 2-3)
        
        ## 11. Risk Management
        - Top 10 Risks (probability x impact matrix)
        - Mitigation Strategies
        - Contingency Plans
        
        ## 12. Appendix
        - Legal Requirements Checklist
        - Glossary
        - Assumptions List
        - Data Sources
        
        ---
        
        **QUY TẮC VIẾT:**
        - Viết bằng tiếng Việt, thuật ngữ chuyên môn giữ tiếng Anh
        - Mọi claim phải có data/evidence
        - Dùng tables và bullet points nhiều hơn paragraphs
        - Tổng tối thiểu 3000 words
        - Mỗi section phải có actionable insights
        - Investment Verdict phải ĐÚNG DATA, không thiên vị
        """,
        expected_output=(
            "Business plan hoàn chỉnh format Markdown, 12 sections đầy đủ, "
            "bao gồm Executive Summary, Market Analysis, Business Model Canvas, "
            "Strategic Analysis (SWOT/Porter/PESTEL), Financial Projections 3 năm, "
            "Investment Decision Matrix với VERDICT rõ ràng, Implementation Roadmap, "
            "và Risk Management. Tối thiểu 3000 words, professional quality."
        ),
        agent=plan_writer,
        context=[
            task_market_research,
            task_strategic_analysis,
            task_financial_analysis,
            task_industry_review,
        ],
    )
    
    # --- Build Crew ---
    crew = Crew(
        agents=[
            market_researcher,
            strategy_analyst,
            financial_modeler,
            industry_expert,
            plan_writer,
        ],
        tasks=[
            task_market_research,
            task_strategic_analysis,
            task_financial_analysis,
            task_industry_review,
            task_write_plan,
        ],
        process=Process.sequential,
        verbose=True,
        full_output=True,
    )
    
    return crew
