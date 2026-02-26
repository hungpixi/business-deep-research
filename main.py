"""
Business Deep Research Agent v4 - Main Entry Point
Pipeline: Gemini API + Google Search + URL Resolver + Cache + Devil's Advocate

Usage:
    python main.py --idea "Mô tả ý tưởng" --industry tech_startup --market vietnam
    python main.py --idea "..." --context context.json
    python main.py --idea "..." --no-interactive
    python main.py --list-industries
    python main.py --idea "..." --dry-run
    python main.py --clear-cache
"""
import argparse
import os
import sys
from datetime import datetime
from pathlib import Path

from dotenv import load_dotenv
load_dotenv()

from config import (
    INDUSTRIES,
    MARKETS,
    INDUSTRY_FRAMEWORKS,
    OUTPUT_DIR,
    validate_config,
)
from utils import save_output


def parse_args():
    parser = argparse.ArgumentParser(
        description="🚀 Business Deep Research Agent v4",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python main.py --idea "AI chatbot CSKH cho SME Việt Nam" --industry tech_startup
  python main.py --idea "..." --context context.json
  python main.py --idea "..." --no-interactive
  python main.py --clear-cache
        """
    )
    
    parser.add_argument("--idea", "-i", type=str, help="Mô tả ý tưởng kinh doanh")
    parser.add_argument("--industry", "-n", type=str, default="tech_startup",
                       choices=list(INDUSTRIES.keys()))
    parser.add_argument("--market", "-m", type=str, default="vietnam",
                       choices=list(MARKETS.keys()))
    parser.add_argument("--output", "-o", type=str, default=None)
    parser.add_argument("--context", "-c", type=str, default=None,
                       help="Path to context.json file")
    parser.add_argument("--no-interactive", action="store_true",
                       help="Skip interactive questionnaire")
    parser.add_argument("--list-industries", action="store_true")
    parser.add_argument("--list-frameworks", action="store_true")
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--clear-cache", action="store_true",
                       help="Clear search cache")
    
    return parser.parse_args()


def print_banner():
    print("""
╔══════════════════════════════════════════════════════════════╗
║                                                              ║
║   🚀 BUSINESS DEEP RESEARCH AGENT v4                        ║
║   AI-Powered Business Plan Generator                         ║
║                                                              ║
║   ✨ Gemini API + Google Search Grounding                    ║
║   📚 12 MBA Frameworks | 😈 Devil's Advocate                ║
║   🔍 Web Search + URL Resolver + Cache                       ║
║   📋 Interactive Questionnaire                               ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝
    """)


def list_industries():
    print("\n📋 Ngành kinh doanh có sẵn:\n")
    for key, name in INDUSTRIES.items():
        frameworks = INDUSTRY_FRAMEWORKS.get(key, [])
        print(f"  • {key:<20} → {name}")
        print(f"    Frameworks: {', '.join(frameworks)}\n")


def run_dry(idea, industry, market):
    print("\n🔍 DRY RUN - Kiểm tra config:\n")
    print(f"  Ý tưởng:    {idea}")
    print(f"  Ngành:      {INDUSTRIES.get(industry)} ({industry})")
    print(f"  Thị trường: {MARKETS.get(market)} ({market})")
    print(f"  Frameworks: {', '.join(INDUSTRY_FRAMEWORKS.get(industry, []))}")
    
    try:
        validate_config()
        print(f"\n  ✅ Config hợp lệ!")
        print(f"  ✅ GEMINI_API_KEY: ...{os.getenv('GEMINI_API_KEY', '')[-8:]}")
        print(f"  ✅ Output dir: {OUTPUT_DIR}")
    except ValueError as e:
        print(f"\n  ❌ Config error: {e}")
        return False
    
    print(f"\n  🔍 Testing Gemini Search + URL Resolver...")
    try:
        from tools.gemini_search import gemini_search
        result = gemini_search("Market size SaaS Vietnam 2025", detailed=False)
        if result and not result.startswith("[Search Error]"):
            print(f"  ✅ Gemini Search working!")
            # Check URL quality
            if "vertexaisearch.cloud.google.com" in result:
                print(f"  ⚠️ Some redirect URLs still present")
            else:
                print(f"  ✅ URLs resolved to direct links!")
            print(f"  📝 Preview: {result[:200]}...")
        else:
            print(f"  ⚠️ Gemini Search returned: {result[:100]}")
    except Exception as e:
        print(f"  ❌ Gemini Search error: {e}")
    
    # Check cache
    from tools.search_cache import CACHE_DIR
    cache_files = list(CACHE_DIR.glob("*.json")) if CACHE_DIR.exists() else []
    print(f"\n  💾 Cache: {len(cache_files)} entries in {CACHE_DIR}")
    
    return True


def main():
    print_banner()
    args = parse_args()
    
    if args.clear_cache:
        from tools.search_cache import clear_cache
        clear_cache()
        print("✅ Search cache cleared")
        return
    
    if args.list_industries:
        list_industries()
        return
    
    if args.list_frameworks:
        print("\n📚 MBA Frameworks theo ngành:\n")
        for ind, fws in INDUSTRY_FRAMEWORKS.items():
            print(f"\n  🏢 {INDUSTRIES.get(ind, ind)} ({ind}):")
            for i, fw in enumerate(fws, 1):
                print(f"     {i}. {fw}")
        return
    
    if not args.idea:
        print("❌ Cần --idea 'mô tả ý tưởng'. Ví dụ:")
        print("   python main.py --idea 'AI chatbot cho SME Việt Nam'")
        print("   python main.py --idea '...' --context context.json")
        return
    
    if args.dry_run:
        run_dry(args.idea, args.industry, args.market)
        return
    
    # Validate config
    try:
        validate_config()
    except ValueError as e:
        print(f"❌ Config error: {e}")
        sys.exit(1)
    
    # Import and run pipeline
    from pipeline import run_pipeline
    
    final_plan = run_pipeline(
        business_idea=args.idea,
        industry=args.industry,
        market=args.market,
        context_file=args.context,
        interactive=not args.no_interactive,
    )
    
    # Save output
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = args.output or f"business_plan_{args.industry}_{timestamp}.md"
    
    header = f"""---
title: Business Plan - {args.idea}
industry: {args.industry}
market: {args.market}
generated: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
engine: Gemini API + Google Search Grounding (v4)
frameworks: {", ".join(INDUSTRY_FRAMEWORKS.get(args.industry, []))}
version: v4
---

"""
    full_output = header + final_plan
    filepath = save_output(full_output, filename, OUTPUT_DIR)
    
    print(f"\n{'='*60}")
    print(f"✅ Business plan đã được tạo thành công!")
    print(f"📄 File: {filepath}")
    print(f"📊 Size: {filepath.stat().st_size / 1024:.1f} KB")
    print(f"{'='*60}")


if __name__ == "__main__":
    main()
