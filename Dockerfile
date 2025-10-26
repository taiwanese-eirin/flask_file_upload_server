# Dockerfile for flask_file_upload_server

# ---- Builder Stage ----
FROM python:3.11-slim as builder

# Prevent Python from writing .pyc files and buffer stdout/stderr
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Install build dependencies
RUN apt-get update \
    && apt-get install -y --no-install-recommends build-essential gcc \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /install

# Install Python dependencies
COPY requirements.txt .
RUN pip install --upgrade pip \
    && pip install --no-cache-dir --prefix="/install" -r requirements.txt

# ---- Final Stage ----
FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# Install runtime dependencies (gosu for dropping privileges, curl for healthcheck)
RUN apt-get update \
    && apt-get install -y --no-install-recommends gosu curl \
    && rm -rf /var/lib/apt/lists/*

# Copy installed packages from builder stage
COPY --from=builder /install /usr/local

# Copy app source
COPY . /app

# Create non-root user and group (fixed uid/gid for easier host bind mount ownership)
RUN groupadd -r -g 1000 appgroup && useradd --no-log-init -r -u 1000 -g appgroup appuser

# Add entrypoint
COPY entrypoint.sh /usr/local/bin/entrypoint.sh
RUN chmod +x /usr/local/bin/entrypoint.sh

# Default envs (can be overridden)
ENV GUNICORN_WORKERS=3
ENV UPLOAD_FOLDER=/data/uploads
ENV MAX_CONTENT_LENGTH=104857600

# Expose port used by gunicorn
EXPOSE 8000

ENTRYPOINT ["/usr/local/bin/entrypoint.sh"]
# Default command; adjust "app:app" to match your wsgi entry if needed
CMD gunicorn --bind 0.0.0.0:8000 app:app --workers "${GUNICORN_WORKERS}"