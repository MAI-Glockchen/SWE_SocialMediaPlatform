# --- Base image with Python 3.13 (or 3.12+) ---
FROM python:3.13-slim AS base

# uv: ultra-fast package installer
RUN pip install --no-cache-dir uv

# Create app dir
WORKDIR /app

# Copy only dependency files first (cache layer)
COPY pyproject.toml uv.lock ./

# Install dependencies (production only)
RUN uv sync --frozen --no-dev

# Copy backend code
COPY backend ./backend

COPY post_generator ./post_generator

# Expose FastAPI port
EXPOSE 8000

# Run API
CMD ["uv", "run", "uvicorn", "backend.main:app", "--host", "0.0.0.0", "--port", "8000"]
