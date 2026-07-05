FROM python:3.11-slim

WORKDIR /app

# Python settings
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Default environment variables (can be overridden by Render)
ENV MODEL_DIR=/app/model
ENV API_BASE_URL=http://127.0.0.1:8000
ENV ENABLE_DB_LOGGING=false

# Install system dependencies for MySQL
RUN apt-get update && apt-get install -y \
    gcc \
    default-libmysqlclient-dev \
    pkg-config \
    && rm -rf /var/lib/apt/lists/*

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application files
COPY app.py main.py setup_db.py ./
COPY model ./model
COPY data ./data  # Optional: if you need data files

# Run database setup during build (will create tables if credentials are available)
# This will fail silently if database credentials are not provided during build
RUN python -c "import setup_db; setup_db.setup_database()" || echo "Database setup skipped (credentials not available)"

# Expose common application ports
EXPOSE 8000
EXPOSE 8501
EXPOSE 10000

# Default command (used for local Docker runs)
# Override this in docker-compose or render.yaml
CMD ["python", "-m", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
