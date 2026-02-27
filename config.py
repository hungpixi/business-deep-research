"""
Configuration module for Business Deep Research Agent.
Loads environment variables and defines project-wide settings.
"""
import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# === API Keys ===
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")

# === Proxy API (Antigravity Tools) ===
PROXY_API_KEY = os.getenv("PROXY_API_KEY")
PROXY_BASE_URL = os.getenv("PROXY_BASE_URL", "http://localhost:8045/v1")
PROXY_MODEL = os.getenv("PROXY_MODEL", "gemini-2.5-pro")

# === Model Configuration ===
GEMINI_MODEL_FAST = os.getenv("GEMINI_MODEL_FAST", "gemini-2.0-flash")
GEMINI_MODEL_PRO = os.getenv("GEMINI_MODEL_PRO", "gemini-2.5-pro")

# CrewAI uses LiteLLM format for Gemini
CREWAI_LLM_FAST = f"gemini/{GEMINI_MODEL_FAST}"
CREWAI_LLM_PRO = f"gemini/{GEMINI_MODEL_PRO}"

# === Paths ===
BASE_DIR = Path(__file__).parent
KNOWLEDGE_DIR = BASE_DIR / "knowledge"
FRAMEWORKS_DIR = KNOWLEDGE_DIR / "frameworks"
INDUSTRIES_DIR = KNOWLEDGE_DIR / "industries"
MARKETS_DIR = KNOWLEDGE_DIR / "markets"
TEMPLATES_DIR = BASE_DIR / "templates"
OUTPUT_DIR = Path(os.getenv("OUTPUT_DIR", "./output"))

# === Supported Industries ===
INDUSTRIES = {
    "tech_startup": "Startup Công Nghệ",
    "trading_finance": "Trading & Tài Chính",
    "fnb": "F&B (Nhà Hàng / Quán Cà Phê)",
    "education": "Giáo Dục (Mầm Non)",
    "tourism": "Du Lịch & Lữ Hành",
    "ecommerce": "Thương Mại Điện Tử",
    "export_import": "Xuất Nhập Khẩu",
}

# === Supported Markets ===
MARKETS = {
    "vietnam": "Thị Trường Việt Nam",
    "international": "Thị Trường Quốc Tế",
    "sea": "Đông Nam Á",
}

# === MBA Frameworks mapping by industry ===
# Defines which frameworks are most relevant for each industry
INDUSTRY_FRAMEWORKS = {
    "tech_startup": [
        "lean_canvas",
        "business_model_canvas",
        "tam_sam_som",
        "swot_tows",
        "competitive_analysis",
        "porters_five_forces",
        "blue_ocean",
        "financial_projections",
        "investment_analysis",  # ROI, NPV, IRR, Payback
    ],
    "trading_finance": [
        "swot_tows",
        "porters_five_forces",
        "financial_projections",
        "investment_analysis",
        "pestel",
        "competitive_analysis",
    ],
    "fnb": [
        "business_model_canvas",
        "swot_tows",
        "porters_five_forces",
        "pestel",
        "value_chain",
        "financial_projections",
        "investment_analysis",
    ],
    "education": [
        "business_model_canvas",
        "swot_tows",
        "pestel",
        "tam_sam_som",
        "financial_projections",
        "investment_analysis",
    ],
    "tourism": [
        "business_model_canvas",
        "swot_tows",
        "pestel",
        "porters_five_forces",
        "value_chain",
        "ansoff_matrix",
        "financial_projections",
        "investment_analysis",
    ],
    "ecommerce": [
        "lean_canvas",
        "business_model_canvas",
        "tam_sam_som",
        "swot_tows",
        "competitive_analysis",
        "financial_projections",
        "investment_analysis",
    ],
    "export_import": [
        "business_model_canvas",
        "swot_tows",
        "pestel",
        "porters_five_forces",
        "value_chain",
        "financial_projections",
        "investment_analysis",
    ],
}

# === Investment Analysis Thresholds ===
INVESTMENT_THRESHOLDS = {
    "min_roi_percent": 20,         # ROI tối thiểu 20%/năm
    "max_payback_years": 3,        # Payback period tối đa 3 năm
    "min_npv_positive": True,      # NPV phải dương
    "min_irr_percent": 15,         # IRR tối thiểu 15%
    "max_burn_rate_months": 18,    # Runway tối thiểu 18 tháng
}

def validate_config():
    """Validate required configuration."""
    if not GEMINI_API_KEY:
        raise ValueError("GEMINI_API_KEY is required. Set it in .env file.")
    
    # Create output directory if not exists
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    
    return True
