"""
Search Cache - Lưu kết quả search vào file, TTL 24h.
Tránh tốn API khi chạy lại cùng query.
"""
import hashlib
import json
import time
from pathlib import Path

CACHE_DIR = Path(__file__).parent.parent / "cache"
DEFAULT_TTL = 86400  # 24 hours


def _get_cache_path(query: str) -> Path:
    key = hashlib.sha256(query.encode()).hexdigest()[:16]
    return CACHE_DIR / f"{key}.json"


def get_cached(query: str, ttl: int = DEFAULT_TTL) -> str | None:
    """Get cached search result if still valid."""
    CACHE_DIR.mkdir(exist_ok=True)
    path = _get_cache_path(query)
    
    if not path.exists():
        return None
    
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
        if time.time() - data["timestamp"] < ttl:
            print(f"  💾 Cache hit: {query[:50]}...")
            return data["result"]
    except (json.JSONDecodeError, KeyError):
        pass
    
    return None


def set_cached(query: str, result: str):
    """Save search result to cache."""
    CACHE_DIR.mkdir(exist_ok=True)
    path = _get_cache_path(query)
    
    data = {
        "query": query,
        "result": result,
        "timestamp": time.time(),
    }
    path.write_text(json.dumps(data, ensure_ascii=False), encoding="utf-8")


def clear_cache():
    """Clear all cached results."""
    if CACHE_DIR.exists():
        for f in CACHE_DIR.glob("*.json"):
            f.unlink()
        print("  🗑️ Cache cleared")
