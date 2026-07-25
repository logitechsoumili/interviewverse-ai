# Stage 1: Build the React (Next.js) frontend
FROM node:20-alpine AS frontend-builder
WORKDIR /app/frontend

COPY frontend/package*.json ./
RUN npm ci

COPY frontend/ ./
ARG NEXT_PUBLIC_API_URL=/api/v1
ENV NEXT_PUBLIC_API_URL=$NEXT_PUBLIC_API_URL
ENV NODE_ENV=production
ENV NEXT_TELEMETRY_DISABLED=1

RUN npm run build

# Stage 2: Install Python dependencies
FROM python:3.11-slim AS backend-builder
WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

COPY backend/requirements.txt ./
RUN pip install --no-cache-dir --user -r requirements.txt

# Stage 3: Runtime image
FROM python:3.11-slim AS runner
WORKDIR /app

# Copy installed python dependencies from builder
COPY --from=backend-builder /root/.local /root/.local
ENV PATH=/root/.local/bin:$PATH

# Copy backend application files
COPY backend /app/backend

# Copy built frontend static files
COPY --from=frontend-builder /app/frontend/out /app/frontend/out

# Set environment variables
ENV PYTHONPATH=/app/backend:/app
ENV PYTHONUNBUFFERED=1

# Expose default port
EXPOSE 8000

# Create non-root user
RUN addgroup --system --gid 1001 appgroup && \
    adduser --system --uid 1001 --gid 1001 appuser && \
    chown -R appuser:appgroup /app

USER appuser

# Run FastAPI app with Uvicorn, binding to the PORT env variable provided by Render.
# Using exec ensures that uvicorn runs as PID 1 and receives OS shutdown signals correctly.
CMD ["sh", "-c", "exec uvicorn app.main:app --host 0.0.0.0 --port ${PORT:-8000}"]
