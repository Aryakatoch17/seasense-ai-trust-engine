FROM python:3.9-slim

WORKDIR /app

# Copy requirements first for better caching
COPY ai_trust_engine/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY ai_trust_engine/ .

# Expose port
EXPOSE 8005

# Health check
HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
  CMD curl -f http://localhost:8005/health || exit 1

# Run the application
CMD ["python", "-m", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8005"]
