FROM python:3.11-slim

WORKDIR /app

# Python settings
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Default environment variables (can be overridden by Render)
ENV MODEL_DIR=/app/model
ENV API_BASE_URL=http://127.0.0.1:8000

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application files
COPY app.py main.py ./
COPY model ./model

# Expose common application ports (for local development only)
EXPOSE 8000
EXPOSE 8501

# Default command (used for local Docker runs)
CMD ["python", "-m", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
