# === Stage 1: Build Next.js frontend ===
FROM node:20-alpine AS frontend
WORKDIR /app/web
COPY web/package.json web/package-lock.json ./
RUN npm ci --silent
COPY web/ ./
RUN npm run build

# === Stage 2: Python backend ===
FROM python:3.11-slim
WORKDIR /app

# System deps
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl && rm -rf /var/lib/apt/lists/*

# Python deps
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy app code
COPY app.py pipeline.py config.py utils.py ./
COPY tools/ ./tools/
COPY knowledge/ ./knowledge/
COPY output/.gitkeep ./output/

# Copy built frontend from stage 1
COPY --from=frontend /app/web/out ./web/out

# Create non-root user
RUN useradd -m appuser && chown -R appuser:appuser /app
USER appuser

EXPOSE 5000

# Health check
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s \
    CMD curl -f http://localhost:5000/api/config || exit 1

CMD ["python", "app.py"]
