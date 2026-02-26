"""
Utility functions: load knowledge files, search tools, output formatting.
"""
import os
from pathlib import Path
from typing import Optional
from config import FRAMEWORKS_DIR, INDUSTRIES_DIR, MARKETS_DIR


def load_framework(name: str) -> str:
    """Load MBA framework knowledge file."""
    path = FRAMEWORKS_DIR / f"{name}.md"
    if path.exists():
        return path.read_text(encoding="utf-8")
    raise FileNotFoundError(f"Framework not found: {name}")


def load_industry(name: str) -> str:
    """Load industry template file."""
    path = INDUSTRIES_DIR / f"{name}.md"
    if path.exists():
        return path.read_text(encoding="utf-8")
    raise FileNotFoundError(f"Industry template not found: {name}")


def load_market(name: str) -> str:
    """Load market context file."""
    path = MARKETS_DIR / f"{name}.md"
    if path.exists():
        return path.read_text(encoding="utf-8")
    raise FileNotFoundError(f"Market context not found: {name}")


def load_all_frameworks(framework_list: list[str]) -> str:
    """Load and concatenate multiple framework files."""
    contents = []
    for name in framework_list:
        try:
            content = load_framework(name)
            contents.append(f"\n{'='*60}\n## FRAMEWORK: {name.upper()}\n{'='*60}\n{content}")
        except FileNotFoundError:
            contents.append(f"\n[WARNING] Framework '{name}' not found, skipping.")
    return "\n".join(contents)


def save_output(content: str, filename: str, output_dir: Path) -> Path:
    """Save generated content to file."""
    output_dir.mkdir(parents=True, exist_ok=True)
    filepath = output_dir / filename
    filepath.write_text(content, encoding="utf-8")
    return filepath


def format_investment_verdict(score: float) -> str:
    """Format investment decision based on score."""
    if score >= 7.0:
        return "✅ **INVEST** - Cơ hội hấp dẫn, đáng đầu tư"
    elif score >= 5.0:
        return "⚠️ **CONDITIONAL** - Cần cải thiện một số yếu tố trước khi đầu tư"
    else:
        return "❌ **PASS** - Rủi ro cao hoặc không đủ hấp dẫn"
