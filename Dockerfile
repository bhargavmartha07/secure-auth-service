# ---------- Stage 1: Builder ----------
FROM python:3.11-slim AS builder

WORKDIR /app

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt


# ---------- Stage 2: Runtime ----------
FROM python:3.11-slim

ENV TZ=UTC
WORKDIR /app

# Install system dependencies (cron + timezone + procps)
RUN apt-get update && \
    apt-get install -y cron tzdata procps && \
    rm -rf /var/lib/apt/lists/*

# Copy Python environment from builder
COPY --from=builder /usr/local /usr/local

# Copy application code
COPY app app
COPY scripts scripts

# Copy cron configuration
COPY cron/2fa-cron /etc/cron.d/2fa-cron

# Copy keys (required by assignment)
COPY student_private.pem .
COPY student_public.pem .
COPY instructor_public.pem .

# Set correct permissions for cron
RUN chmod 0644 /etc/cron.d/2fa-cron && crontab /etc/cron.d/2fa-cron

# Create persistent directories with write permissions
RUN mkdir /data /cron && chmod 777 /data /cron

# Pre-create cron log file (important!)
RUN touch /cron/last_code.txt && chmod 666 /cron/last_code.txt

# Expose API port
EXPOSE 8080

# Start cron daemon + FastAPI server
CMD service cron start && uvicorn app.main:app --host 0.0.0.0 --port 8080
