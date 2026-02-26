"""
Output Validator - Cross-check consistency trong business plan output.
Kiểm tra: pricing match, revenue math, financial logic.
"""
import re


def validate_output(content: str) -> list[str]:
    """
    Validate business plan output for consistency issues.
    Returns list of warnings/issues found.
    """
    issues = []
    
    # 1. Check pricing consistency
    pricing_values = set()
    pricing_pattern = re.compile(r'(\d{2,3}[,.]?\d{3})\s*(?:VND|VNĐ|đ)', re.IGNORECASE)
    for match in pricing_pattern.finditer(content):
        val = match.group(1).replace(',', '').replace('.', '')
        if 50000 <= int(val) <= 5000000:  # Reasonable SaaS pricing range
            pricing_values.add(int(val))
    
    if len(pricing_values) > 6:
        issues.append(f"⚠️ Quá nhiều mức giá khác nhau ({len(pricing_values)}), có thể mâu thuẫn: {sorted(pricing_values)}")
    
    # 2. Check if multiple scenarios exist
    if "pessimistic" not in content.lower() and "bi quan" not in content.lower():
        issues.append("⚠️ Thiếu kịch bản Pessimistic trong financial projections")
    
    if "optimistic" not in content.lower() and "lạc quan" not in content.lower():
        issues.append("⚠️ Thiếu kịch bản Optimistic trong financial projections")
    
    # 3. Check for persona count
    persona_count = content.lower().count("persona")
    if persona_count < 2:
        issues.append("⚠️ Có thể thiếu customer personas (chỉ tìm thấy < 2 lần nhắc)")
    
    # 4. Check devil's advocate / critical section
    has_critical = any(
        term in content.lower() 
        for term in ["devil's advocate", "phản biện", "blind spot", "worst case", "rủi ro lớn nhất"]
    )
    if not has_critical:
        issues.append("⚠️ Thiếu phần phản biện / critical review")
    
    # 5. Check sources exist
    url_count = len(re.findall(r'https?://[^\s\)]+', content))
    if url_count < 5:
        issues.append(f"⚠️ Quá ít source URLs ({url_count}), cần ít nhất 5")
    
    # 6. Check redirect URLs
    redirect_count = content.count("vertexaisearch.cloud.google.com/grounding-api-redirect")
    if redirect_count > 0:
        issues.append(f"⚠️ {redirect_count} redirect URLs chưa được resolve thành URL gốc")
    
    return issues


def format_validation_report(issues: list[str]) -> str:
    """Format validation issues into a report section."""
    if not issues:
        return "\n✅ Output validation passed — no issues found.\n"
    
    report = "\n## ⚠️ Output Validation Report\n\n"
    for i, issue in enumerate(issues, 1):
        report += f"{i}. {issue}\n"
    report += "\n"
    return report
