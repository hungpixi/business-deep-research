"""
Gemini Search Tool v4 — Rate-limited, cached, with URL resolver.
- Inline citations via groundingSupports + groundingChunks
- Redirect URL → direct URL resolver
- Search cache (24h TTL)
- Rate limiter + exponential backoff for 429
"""
import time
import threading
import requests
from google import genai
from google.genai import types
from config import GEMINI_API_KEY, GEMINI_MODEL_FAST, GEMINI_MODEL_PRO
from tools.search_cache import get_cached, set_cached


# === Rate Limiter ===
class RateLimiter:
    def __init__(self, max_per_minute: int = 10):
        self.max_per_minute = max_per_minute
        self.tokens = max_per_minute
        self.last_refill = time.time()
        self.lock = threading.Lock()
    
    def wait(self):
        with self.lock:
            now = time.time()
            elapsed = now - self.last_refill
            self.tokens = min(
                self.max_per_minute,
                self.tokens + elapsed * (self.max_per_minute / 60.0)
            )
            self.last_refill = now
            if self.tokens < 1:
                wait_time = (1 - self.tokens) / (self.max_per_minute / 60.0)
                print(f"  ⏳ Rate limit: waiting {wait_time:.1f}s...")
                time.sleep(wait_time)
                self.tokens = 0
                self.last_refill = time.time()
            else:
                self.tokens -= 1


# Free tier: 2 RPM cho search grounding, 15 RPM cho generate
_rate_limiter = RateLimiter(max_per_minute=2)
_client = None
_url_cache = {}  # In-memory cache for resolved URLs


def get_client():
    global _client
    if _client is None:
        _client = genai.Client(api_key=GEMINI_API_KEY)
    return _client


def _retry_with_backoff(func, max_retries: int = 4, base_delay: float = 15.0):
    for attempt in range(max_retries + 1):
        try:
            return func()
        except Exception as e:
            error_str = str(e)
            if "429" in error_str or "RESOURCE_EXHAUSTED" in error_str:
                if attempt < max_retries:
                    delay = base_delay * (2 ** attempt)
                    print(f"  ⚠️ Rate limited (429). Retry {attempt+1}/{max_retries} in {delay:.0f}s...")
                    time.sleep(delay)
                    continue
            raise


# === URL Resolver ===
def resolve_url(redirect_url: str) -> str:
    """
    Resolve Google redirect URL → actual URL.
    Dùng HTTP HEAD request với allow_redirects=True.
    """
    if "vertexaisearch.cloud.google.com/grounding-api-redirect" not in redirect_url:
        return redirect_url  # Already a direct URL
    
    if redirect_url in _url_cache:
        return _url_cache[redirect_url]
    
    try:
        resp = requests.head(
            redirect_url, 
            allow_redirects=True, 
            timeout=5,
            headers={"User-Agent": "Mozilla/5.0"}
        )
        final_url = resp.url
        if final_url and final_url != redirect_url:
            _url_cache[redirect_url] = final_url
            return final_url
    except Exception:
        pass
    
    # Fallback: return original
    _url_cache[redirect_url] = redirect_url
    return redirect_url


def _resolve_all_urls_in_text(text: str) -> str:
    """Replace all redirect URLs in text with resolved URLs."""
    import re
    redirect_pattern = re.compile(
        r'https://vertexaisearch\.cloud\.google\.com/grounding-api-redirect/[^\s\)]+',
    )
    
    urls_to_resolve = set(redirect_pattern.findall(text))
    if not urls_to_resolve:
        return text
    
    print(f"  🔗 Resolving {len(urls_to_resolve)} redirect URLs...")
    for url in urls_to_resolve:
        resolved = resolve_url(url)
        if resolved != url:
            text = text.replace(url, resolved)
    
    return text


# === Citations ===
def add_citations(response) -> str:
    """Official pattern: inline [1](url) via groundingSupports + groundingChunks, with URL resolution."""
    text = response.text or ""
    
    candidate = response.candidates[0] if response.candidates else None
    if not candidate:
        return text
    
    grounding = getattr(candidate, 'grounding_metadata', None)
    if not grounding:
        return text
    
    supports = getattr(grounding, 'grounding_supports', None)
    chunks = getattr(grounding, 'grounding_chunks', None)
    
    # Resolve all chunk URLs first
    if chunks:
        for chunk in chunks:
            web = getattr(chunk, 'web', None)
            if web:
                uri = getattr(web, 'uri', '')
                if uri:
                    resolved = resolve_url(uri)
                    if hasattr(web, 'uri'):
                        try:
                            web.uri = resolved
                        except (AttributeError, TypeError):
                            pass
    
    if not supports or not chunks:
        source_list = []
        if chunks:
            for i, chunk in enumerate(chunks):
                web = getattr(chunk, 'web', None)
                if web:
                    uri = getattr(web, 'uri', '')
                    title = getattr(web, 'title', 'Source')
                    if uri:
                        source_list.append(f"{i+1}. [{title}]({uri})")
            if source_list:
                text += "\n\n**Nguồn tham khảo:**\n" + "\n".join(source_list)
        return text
    
    sorted_supports = sorted(
        supports,
        key=lambda s: getattr(getattr(s, 'segment', None), 'end_index', 0),
        reverse=True
    )
    
    for support in sorted_supports:
        segment = getattr(support, 'segment', None)
        if not segment:
            continue
        end_index = getattr(segment, 'end_index', None)
        chunk_indices = getattr(support, 'grounding_chunk_indices', [])
        if end_index is None or not chunk_indices:
            continue
        
        citation_links = []
        for idx in chunk_indices:
            if idx < len(chunks):
                web = getattr(chunks[idx], 'web', None)
                if web:
                    uri = getattr(web, 'uri', '')
                    if uri:
                        citation_links.append(f"[{idx + 1}]({uri})")
        
        if citation_links:
            citation_string = " " + ", ".join(citation_links)
            text = text[:end_index] + citation_string + text[end_index:]
    
    # Append full reference list with resolved URLs
    source_list = []
    seen_uris = set()
    for i, chunk in enumerate(chunks):
        web = getattr(chunk, 'web', None)
        if web:
            uri = getattr(web, 'uri', '')
            title = getattr(web, 'title', 'Source')
            if uri and uri not in seen_uris:
                seen_uris.add(uri)
                source_list.append(f"[{i+1}] [{title}]({uri})")
    
    if source_list:
        text += "\n\n---\n**📚 Nguồn tham khảo:**\n" + "\n".join(source_list) + "\n"
    
    # Final pass: resolve any remaining redirect URLs in text
    text = _resolve_all_urls_in_text(text)
    
    return text


# === Search Functions ===
def gemini_search(query: str, detailed: bool = True) -> str:
    """Search with caching + rate limiting + retry + URL resolution."""
    # Check cache first
    cached = get_cached(query)
    if cached:
        return cached
    
    client = get_client()
    
    system_instruction = (
        "Bạn là chuyên gia nghiên cứu thị trường và phân tích kinh doanh.\n"
        "Khi trả lời:\n"
        "1. LUÔN cung cấp số liệu CỤ THỂ (con số, %, $, VND)\n"
        "2. Ưu tiên dữ liệu từ: báo cáo chính thức, bài báo uy tín, nghiên cứu học thuật\n"
        "3. Nếu data không chính xác 100%, ghi rõ 'Ước tính'\n"
        "4. Trả lời bằng tiếng Việt, thuật ngữ chuyên môn giữ tiếng Anh\n"
        "5. Phân tích chi tiết, đưa ra nhiều số liệu nhất có thể"
    )
    
    search_query = f"Phân tích chi tiết với số liệu cụ thể: {query}" if detailed else query
    
    def _call():
        _rate_limiter.wait()
        return client.models.generate_content(
            model=GEMINI_MODEL_FAST,
            contents=search_query,
            config=types.GenerateContentConfig(
                system_instruction=system_instruction,
                tools=[types.Tool(google_search=types.GoogleSearch())],
                temperature=0.3,
            ),
        )
    
    try:
        response = _retry_with_backoff(_call)
        result = add_citations(response)
        set_cached(query, result)  # Save to cache
        return result
    except Exception as e:
        return f"[Search Error] {str(e)}"


def gemini_batch_search(queries: list[str], topic: str = "") -> str:
    """Batch queries into ONE API call. Cached."""
    cache_key = f"BATCH:{topic}:{';'.join(queries)}"
    cached = get_cached(cache_key)
    if cached:
        return cached
    
    client = get_client()
    
    combined_query = f"Nghiên cứu chi tiết về: {topic}\n\n"
    combined_query += "Hãy trả lời TẤT CẢ các câu hỏi sau với số liệu cụ thể:\n\n"
    for i, q in enumerate(queries, 1):
        combined_query += f"{i}. {q}\n"
    combined_query += "\nTrả lời từng câu hỏi chi tiết, có số liệu và dẫn chứng."
    
    system_instruction = (
        "Bạn là Senior Market Research Analyst. Trả lời từng câu hỏi chi tiết.\n"
        "Mỗi câu trả lời phải có: số liệu cụ thể, nguồn dữ liệu, phân tích.\n"
        "Viết tiếng Việt, thuật ngữ chuyên môn giữ tiếng Anh."
    )
    
    def _call():
        _rate_limiter.wait()
        return client.models.generate_content(
            model=GEMINI_MODEL_FAST,
            contents=combined_query,
            config=types.GenerateContentConfig(
                system_instruction=system_instruction,
                tools=[types.Tool(google_search=types.GoogleSearch())],
                temperature=0.3,
            ),
        )
    
    try:
        print(f"  🔍 Batch search ({len(queries)} queries in 1 call): {topic[:60]}...")
        response = _retry_with_backoff(_call)
        result = add_citations(response)
        set_cached(cache_key, result)
        return result
    except Exception as e:
        return f"[Batch Search Error] {str(e)}"


def gemini_deep_research(topic: str, sub_queries: list[str]) -> str:
    """Deep research v4: batched + cached."""
    BATCH_SIZE = 4
    all_results = []
    
    for batch_start in range(0, len(sub_queries), BATCH_SIZE):
        batch = sub_queries[batch_start:batch_start + BATCH_SIZE]
        batch_num = batch_start // BATCH_SIZE + 1
        total_batches = (len(sub_queries) + BATCH_SIZE - 1) // BATCH_SIZE
        
        print(f"  📦 Batch [{batch_num}/{total_batches}] ({len(batch)} queries):")
        for q in batch:
            print(f"     • {q[:70]}...")
        
        result = gemini_batch_search(batch, topic=topic)
        all_results.append(result)
    
    combined = f"# Deep Research: {topic}\n\n"
    combined += "\n\n---\n\n".join(all_results)
    return combined


def gemini_analyze(prompt: str, context: str = "") -> str:
    """Gemini Pro analysis with retry."""
    client = get_client()
    full_prompt = prompt
    if context:
        full_prompt = f"## Context (Research Data):\n{context}\n\n## Task:\n{prompt}"
    
    def _call_pro():
        _rate_limiter.wait()
        return client.models.generate_content(
            model=GEMINI_MODEL_PRO,
            contents=full_prompt,
            config=types.GenerateContentConfig(
                temperature=0.2,
                max_output_tokens=16000,
            ),
        )
    
    def _call_flash():
        _rate_limiter.wait()
        return client.models.generate_content(
            model=GEMINI_MODEL_FAST,
            contents=full_prompt,
            config=types.GenerateContentConfig(
                temperature=0.2,
                max_output_tokens=16000,
            ),
        )
    
    try:
        response = _retry_with_backoff(_call_pro)
        return response.text if response.text else "[No response]"
    except Exception as e:
        print(f"  ⚠️ Pro failed, fallback to Flash: {str(e)[:60]}")
        try:
            response = _retry_with_backoff(_call_flash)
            return response.text if response.text else "[No response]"
        except Exception as e2:
            return f"[Analysis Error] {str(e2)}"
