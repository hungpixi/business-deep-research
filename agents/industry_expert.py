"""
Industry Expert Agent - Chuyên gia ngành cụ thể.
Hiểu quy chuẩn, giấy phép, best practices từng ngành.
"""
from crewai import Agent
from config import CREWAI_LLM_FAST, CREWAI_LLM_PRO


def create_industry_expert(industry: str, use_pro_model: bool = False) -> Agent:
    """Create an Industry Expert Agent customized for a specific industry."""
    llm = CREWAI_LLM_PRO if use_pro_model else CREWAI_LLM_FAST

    industry_backstories = {
        "tech_startup": (
            "Bạn là serial entrepreneur với 5 startups (2 exits) và hiện là Venture Partner "
            "tại 500 Startups. Bạn am hiểu sâu về product-market fit, go-to-market strategies, "
            "fundraising, tech stack decisions, và AI product development. "
            "Bạn hiểu rõ startup ecosystem VN (VIISA, Do Ventures, CyberAgent) "
            "cũng như Silicon Valley standards."
        ),
        "trading_finance": (
            "Bạn là quant trader với 15 năm kinh nghiệm tại Wall Street và "
            "hiện quản lý quỹ đầu tư. Bạn am hiểu regulatory (SEC, SSC), "
            "risk management, Sharpe ratio, drawdown controls, và automated trading systems."
        ),
        "fnb": (
            "Bạn là chuyên gia F&B với kinh nghiệm quản lý chuỗi nhà hàng và franchise. "
            "Bạn am hiểu HACCP, food cost management, quy định ATTP, và operations scaling."
        ),
        "education": (
            "Bạn là chuyên gia giáo dục với kinh nghiệm vận hành trường mầm non và EdTech. "
            "Bạn am hiểu licensing, curriculum standards, student-teacher ratios, và TT26/2018."
        ),
        "tourism": (
            "Bạn là chuyên gia du lịch với kinh nghiệm vận hành DMC và lữ hành. "
            "Bạn am hiểu Luật Du lịch 2017, OTA integration, seasonality management."
        ),
        "ecommerce": (
            "Bạn là chuyên gia e-commerce với kinh nghiệm tại Shopee/Tiki/Amazon. "
            "Bạn am hiểu marketplace dynamics, fulfillment, conversion optimization."
        ),
        "export_import": (
            "Bạn là chuyên gia XNK với 20 năm kinh nghiệm. Bạn am hiểu Incoterms 2020, "
            "HS codes, C/O, L/C, customs procedures, và FTA utilization."
        ),
    }

    backstory = industry_backstories.get(industry, industry_backstories["tech_startup"])

    return Agent(
        role=f"Industry Expert - {industry.replace('_', ' ').title()}",
        goal=(
            f"Provide deep industry-specific expertise for the {industry.replace('_', ' ')} sector. "
            "Identify industry-specific regulations, licensing requirements, best practices, "
            "operational standards, key success factors, and common pitfalls. "
            "Ensure the business plan addresses all industry-critical requirements."
        ),
        backstory=backstory,
        llm=llm,
        verbose=True,
        allow_delegation=False,
        max_iter=10,
    )
