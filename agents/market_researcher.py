"""
Market Research Agent - Nghiên cứu thị trường, đối thủ, xu hướng.
Sử dụng Tavily search + Gemini để thu thập và phân tích data thị trường.
"""
from crewai import Agent
from crewai_tools import SerperDevTool
from config import CREWAI_LLM_FAST, CREWAI_LLM_PRO, TAVILY_API_KEY

try:
    from tavily import TavilyClient
    HAS_TAVILY = True
except ImportError:
    HAS_TAVILY = False


def create_tavily_search_tool():
    """Create Tavily search wrapper as a CrewAI tool."""
    from crewai.tools import BaseTool
    from pydantic import Field

    class TavilySearchTool(BaseTool):
        name: str = "tavily_search"
        description: str = (
            "Search the internet for current information about markets, competitors, "
            "industry trends, and business data. Use this to find real-time data about "
            "market size, competitor analysis, and industry reports."
        )
        api_key: str = Field(default="")

        def _run(self, query: str) -> str:
            client = TavilyClient(api_key=self.api_key)
            response = client.search(
                query=query,
                search_depth="advanced",
                max_results=10,
                include_answer=True,
            )
            results = []
            if response.get("answer"):
                results.append(f"**Summary:** {response['answer']}\n")
            for r in response.get("results", []):
                results.append(f"- [{r['title']}]({r['url']}): {r['content'][:300]}...")
            return "\n".join(results) if results else "No results found."

    return TavilySearchTool(api_key=TAVILY_API_KEY)


def create_market_researcher(use_pro_model: bool = False) -> Agent:
    """Create a Market Research Agent."""
    llm = CREWAI_LLM_PRO if use_pro_model else CREWAI_LLM_FAST
    
    tools = []
    if HAS_TAVILY and TAVILY_API_KEY:
        tools.append(create_tavily_search_tool())

    return Agent(
        role="Senior Market Research Analyst",
        goal=(
            "Conduct comprehensive market research to understand the target market, "
            "identify competitors, analyze market trends, and estimate market size (TAM/SAM/SOM). "
            "Focus on finding real data and actionable insights."
        ),
        backstory=(
            "Bạn là chuyên gia nghiên cứu thị trường với 15 năm kinh nghiệm tại McKinsey "
            "và Harvard Business School. Bạn thành thạo phương pháp nghiên cứu top-down "
            "và bottom-up, có khả năng tổng hợp data từ nhiều nguồn thành insights sâu sắc. "
            "Bạn luôn cung cấp số liệu cụ thể, có nguồn trích dẫn."
        ),
        llm=llm,
        tools=tools,
        verbose=True,
        allow_delegation=False,
        max_iter=15,
    )
