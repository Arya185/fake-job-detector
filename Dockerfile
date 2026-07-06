FROM python:3.11-slim

WORKDIR /app

# Python settings
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Default environment variables (can be overridden by Render)
ENV MODEL_DIR=/app/model
ENV API_BASE_URL=http://127.0.0.1:10000

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application files
COPY ..

# Default command (used for local Docker runs)
CMD ["python", "-m", "uvicorn", "main:app", "--host" ,"0.0.0.0", "--port","10000"]
