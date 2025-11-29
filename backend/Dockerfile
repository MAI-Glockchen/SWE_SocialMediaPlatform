# Backend Dockerfile
FROM python:3.12-slim

ENV PYTHONUNBUFFERED=1
WORKDIR /app

# Install runtime deps
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Install minimal runtime dependencies needed by the app
RUN pip install --upgrade pip && \
    pip install --no-cache-dir fastapi uvicorn sqlmodel httpx

# Copy app
COPY backend/ ./backend/
COPY sqlite/ ./sqlite/

EXPOSE 8000

CMD ["uvicorn", "backend.main:app", "--host", "0.0.0.0", "--port", "8000"]
