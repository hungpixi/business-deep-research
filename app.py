"""
Business Deep Research — FastAPI Backend
ASGI server with async SSE streaming for pipeline execution.

Usage: python app.py
"""
import json
import os
import sys
import queue
import threading
import asyncio
import io
import re
from datetime import datetime
from pathlib import Path
from typing import Optional

from fastapi import FastAPI, HTTPException, Request
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, StreamingResponse, HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from dotenv import load_dotenv

load_dotenv()

# === Paths ===
BASE_DIR = Path(__file__).parent
WEB_DIR = BASE_DIR / "web" / "out"
KNOWLEDGE_DIR = BASE_DIR / "knowledge"
OUTPUT_DIR = BASE_DIR / "output"
SETTINGS_FILE = BASE_DIR / ".settings.json"

# === App ===
app = FastAPI(
    title="Business Deep Research",
    description="AI tạo sản phẩm. Con người vận hành dịch vụ.",
    version="4.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


# === Pydantic Models ===
class PipelineRequest(BaseModel):
    idea: str
    industry: str = "tech_startup"
    market: str = "vietnam"
    context: dict = {}

class SettingsUpdate(BaseModel):
    api_provider: Optional[str] = None
    gemini_api_key: Optional[str] = None
    antigravity_proxy_url: Optional[str] = None
    antigravity_api_key: Optional[str] = None
    model_fast: Optional[str] = None
    model_pro: Optional[str] = None
    tavily_api_key: Optional[str] = None

class KnowledgeContent(BaseModel):
    content: str = ""


# === Settings ===
def load_settings() -> dict:
    defaults = {
        "api_provider": "gemini_direct",
        "gemini_api_key": os.getenv("GEMINI_API_KEY", ""),
        "antigravity_proxy_url": "http://localhost:8045/v1",
        "antigravity_api_key": "",
        "model_fast": os.getenv("GEMINI_MODEL_FAST", "gemini-2.0-flash"),
        "model_pro": os.getenv("GEMINI_MODEL_PRO", "gemini-2.5-pro"),
        "tavily_api_key": os.getenv("TAVILY_API_KEY", ""),
    }
    if SETTINGS_FILE.exists():
        try:
            saved = json.loads(SETTINGS_FILE.read_text(encoding="utf-8"))
            defaults.update(saved)
        except Exception:
            pass
    return defaults

def save_settings(settings: dict):
    SETTINGS_FILE.write_text(json.dumps(settings, indent=2, ensure_ascii=False), encoding="utf-8")


# === Stream Capture (redirect print → queue) ===
class StreamCapture(io.TextIOBase):
    def __init__(self, q: queue.Queue, original):
        self.q = q
        self.original = original

    def write(self, text):
        if self.original:
            self.original.write(text)
        if text.strip():
            step_match = re.match(r'.*STEP (\d+)/(\d+):\s+(.*)', text.strip())
            if step_match:
                self.q.put({
                    "event": "step",
                    "step": int(step_match.group(1)),
                    "total": int(step_match.group(2)),
                    "name": step_match.group(3).strip()
                })
            else:
                self.q.put({"event": "log", "message": text.strip()})
        return len(text)

    def flush(self):
        if self.original:
            self.original.flush()


# ══════════════════════════════════════
# API: Config
# ══════════════════════════════════════

@app.get("/api/config")
async def get_config():
    try:
        from config import INDUSTRIES, MARKETS, INDUSTRY_FRAMEWORKS
        return {
            "industries": INDUSTRIES,
            "markets": MARKETS,
            "frameworks": INDUSTRY_FRAMEWORKS,
            "philosophy": "AI sẽ thay chúng ta tạo ra sản phẩm. AI sẽ không thay thế con người hoàn toàn khi vận hành dịch vụ được.",
        }
    except Exception as e:
        raise HTTPException(500, str(e))


# ══════════════════════════════════════
# API: Settings (Antigravity Tools)
# ══════════════════════════════════════

@app.get("/api/settings")
async def get_settings():
    settings = load_settings()
    masked = dict(settings)
    for key in ["gemini_api_key", "antigravity_api_key", "tavily_api_key"]:
        if masked.get(key) and len(masked[key]) > 12:
            masked[key] = masked[key][:8] + "..." + masked[key][-4:]
    return masked

@app.put("/api/settings")
async def update_settings_endpoint(data: SettingsUpdate):
    settings = load_settings()
    update = data.model_dump(exclude_none=True)
    settings.update(update)
    save_settings(settings)

    if data.gemini_api_key:
        os.environ["GEMINI_API_KEY"] = data.gemini_api_key
    if data.tavily_api_key:
        os.environ["TAVILY_API_KEY"] = data.tavily_api_key

    return {"status": "ok"}


# ══════════════════════════════════════
# API: Pipeline Runner (SSE)
# ══════════════════════════════════════

@app.post("/api/run")
async def run_pipeline_endpoint(req: PipelineRequest):
    if not req.idea.strip():
        raise HTTPException(400, "Cần nhập ý tưởng kinh doanh")

    q: queue.Queue = queue.Queue()

    def pipeline_thread():
        old_stdout = sys.stdout
        sys.stdout = StreamCapture(q, old_stdout)
        try:
            from pipeline import run_pipeline
            from config import INDUSTRY_FRAMEWORKS

            ctx_file = None
            if req.context:
                ctx_path = BASE_DIR / "_temp_context.json"
                ctx_path.write_text(json.dumps(req.context, ensure_ascii=False), encoding="utf-8")
                ctx_file = str(ctx_path)

            result = run_pipeline(
                business_idea=req.idea,
                industry=req.industry,
                market=req.market,
                context_file=ctx_file,
                interactive=False,
            )

            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"business_plan_{req.industry}_{timestamp}.md"
            OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
            filepath = OUTPUT_DIR / filename

            header = f"""---
title: Business Plan - {req.idea}
industry: {req.industry}
market: {req.market}
generated: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
engine: Gemini API + Google Search Grounding
frameworks: {", ".join(INDUSTRY_FRAMEWORKS.get(req.industry, []))}
philosophy: AI tạo sản phẩm, con người vận hành dịch vụ
---

"""
            filepath.write_text(header + result, encoding="utf-8")

            q.put({
                "event": "result",
                "content": result,
                "filename": filename,
            })

            temp = BASE_DIR / "_temp_context.json"
            if temp.exists():
                temp.unlink()

        except Exception as e:
            q.put({"event": "error", "message": str(e)})
        finally:
            sys.stdout = old_stdout
            q.put({"event": "done"})

    thread = threading.Thread(target=pipeline_thread, daemon=True)
    thread.start()

    async def event_generator():
        while True:
            try:
                msg = q.get(timeout=0.5)
                yield f"data: {json.dumps(msg, ensure_ascii=False)}\n\n"
                if msg.get("event") == "done":
                    break
            except queue.Empty:
                yield f"data: {json.dumps({'event': 'ping'})}\n\n"
                await asyncio.sleep(0.1)

    return StreamingResponse(
        event_generator(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "X-Accel-Buffering": "no",
        }
    )


# ══════════════════════════════════════
# API: Knowledge CRUD
# ══════════════════════════════════════

KNOWLEDGE_CATEGORIES = {
    "frameworks": KNOWLEDGE_DIR / "frameworks",
    "industries": KNOWLEDGE_DIR / "industries",
    "markets": KNOWLEDGE_DIR / "markets",
}

@app.get("/api/knowledge/{category}")
async def list_knowledge(category: str):
    if category not in KNOWLEDGE_CATEGORIES:
        raise HTTPException(404, f"Category '{category}' not found")

    dir_path = KNOWLEDGE_CATEGORIES[category]
    if not dir_path.exists():
        return {"files": [], "category": category}

    files = []
    for f in sorted(dir_path.glob("*.md")):
        stat = f.stat()
        files.append({
            "name": f.stem,
            "filename": f.name,
            "size": stat.st_size,
            "modified": datetime.fromtimestamp(stat.st_mtime).isoformat(),
        })

    return {"files": files, "category": category}

@app.get("/api/knowledge/{category}/{name}")
async def get_knowledge(category: str, name: str):
    if category not in KNOWLEDGE_CATEGORIES:
        raise HTTPException(404, "Category not found")

    filepath = KNOWLEDGE_CATEGORIES[category] / f"{name}.md"
    if not filepath.exists():
        raise HTTPException(404, "File not found")

    content = filepath.read_text(encoding="utf-8")
    stat = filepath.stat()
    return {
        "name": name,
        "category": category,
        "content": content,
        "size": stat.st_size,
        "modified": datetime.fromtimestamp(stat.st_mtime).isoformat(),
    }

@app.put("/api/knowledge/{category}/{name}")
async def update_knowledge(category: str, name: str, data: KnowledgeContent):
    if category not in KNOWLEDGE_CATEGORIES:
        raise HTTPException(404, "Category not found")

    dir_path = KNOWLEDGE_CATEGORIES[category]
    dir_path.mkdir(parents=True, exist_ok=True)
    filepath = dir_path / f"{name}.md"
    filepath.write_text(data.content, encoding="utf-8")
    return {"status": "ok", "name": name}

@app.post("/api/knowledge/{category}/{name}")
async def create_knowledge(category: str, name: str, data: KnowledgeContent):
    if category not in KNOWLEDGE_CATEGORIES:
        raise HTTPException(404, "Category not found")

    dir_path = KNOWLEDGE_CATEGORIES[category]
    dir_path.mkdir(parents=True, exist_ok=True)
    filepath = dir_path / f"{name}.md"

    if filepath.exists():
        raise HTTPException(409, "File already exists")

    content = data.content or f"# {name}\n\nNội dung framework mới.\n"
    filepath.write_text(content, encoding="utf-8")
    return {"status": "created", "name": name}

@app.delete("/api/knowledge/{category}/{name}")
async def delete_knowledge(category: str, name: str):
    if category not in KNOWLEDGE_CATEGORIES:
        raise HTTPException(404, "Category not found")

    filepath = KNOWLEDGE_CATEGORIES[category] / f"{name}.md"
    if not filepath.exists():
        raise HTTPException(404, "File not found")

    filepath.unlink()
    return {"status": "deleted", "name": name}


# ══════════════════════════════════════
# API: Reports
# ══════════════════════════════════════

@app.get("/api/reports")
async def list_reports():
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    reports = []
    for f in sorted(OUTPUT_DIR.glob("*.md"), key=lambda x: x.stat().st_mtime, reverse=True):
        content = f.read_text(encoding="utf-8")
        meta = {}
        if content.startswith("---"):
            parts = content.split("---", 2)
            if len(parts) >= 3:
                for line in parts[1].strip().split("\n"):
                    if ":" in line:
                        key, val = line.split(":", 1)
                        meta[key.strip()] = val.strip()

        stat = f.stat()
        reports.append({
            "filename": f.name,
            "size": stat.st_size,
            "modified": datetime.fromtimestamp(stat.st_mtime).isoformat(),
            "title": meta.get("title", f.stem),
            "industry": meta.get("industry", ""),
            "market": meta.get("market", ""),
        })

    return {"reports": reports}

@app.get("/api/reports/{filename}")
async def get_report(filename: str):
    filepath = OUTPUT_DIR / filename
    if not filepath.exists():
        raise HTTPException(404, "Report not found")

    content = filepath.read_text(encoding="utf-8")
    stat = filepath.stat()
    return {
        "filename": filename,
        "content": content,
        "size": stat.st_size,
        "modified": datetime.fromtimestamp(stat.st_mtime).isoformat(),
    }

@app.delete("/api/reports/{filename}")
async def delete_report(filename: str):
    filepath = OUTPUT_DIR / filename
    if not filepath.exists():
        raise HTTPException(404, "Report not found")

    filepath.unlink()
    return {"status": "deleted"}


# ══════════════════════════════════════
# Serve Frontend (Next.js static export)
# ══════════════════════════════════════

# Mount static assets (_next, images, etc.)
if WEB_DIR.exists():
    next_static = WEB_DIR / "_next"
    if next_static.exists():
        app.mount("/_next", StaticFiles(directory=str(next_static)), name="next_static")

@app.get("/")
async def serve_index():
    index = WEB_DIR / "index.html"
    if index.exists():
        return FileResponse(str(index))
    return HTMLResponse("""
    <html><head><title>Business Deep Research</title></head>
    <body style="font-family:Inter,sans-serif;background:#0a0a0a;color:#fff;
                  display:flex;align-items:center;justify-content:center;height:100vh;">
    <div style="text-align:center;">
        <h1>🚀 Business Deep Research</h1>
        <p>Frontend chưa build. Chạy: <code>cd web && npm run build</code></p>
        <p>API docs: <a href="/docs" style="color:#60a5fa;">/docs</a></p>
    </div></body></html>
    """)

@app.get("/editor")
async def serve_editor():
    f = WEB_DIR / "editor.html"
    return FileResponse(str(f)) if f.exists() else HTTPException(404)

@app.get("/reports")
async def serve_reports_page():
    f = WEB_DIR / "reports.html"
    return FileResponse(str(f)) if f.exists() else HTTPException(404)

@app.get("/settings")
async def serve_settings_page():
    f = WEB_DIR / "settings.html"
    return FileResponse(str(f)) if f.exists() else HTTPException(404)

# Catch-all for other static files
@app.get("/{path:path}")
async def serve_static(path: str):
    if WEB_DIR.exists():
        file_path = WEB_DIR / path
        if file_path.exists() and file_path.is_file():
            return FileResponse(str(file_path))
        html_path = WEB_DIR / f"{path}.html"
        if html_path.exists():
            return FileResponse(str(html_path))
    raise HTTPException(404)


# ══════════════════════════════════════
# Main
# ══════════════════════════════════════

if __name__ == "__main__":
    import uvicorn

    print("""
╔══════════════════════════════════════════════════════════════╗
║                                                              ║
║   🚀 BUSINESS DEEP RESEARCH — Web UI (FastAPI)              ║
║   AI tạo sản phẩm. Con người vận hành dịch vụ.              ║
║                                                              ║
║   🌐 http://localhost:5000                                   ║
║   📡 API Docs: http://localhost:5000/docs                    ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝
    """)

    uvicorn.run("app:app", host="0.0.0.0", port=5000, reload=True)
