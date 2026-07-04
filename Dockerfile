FROM python:3.11-slim

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV MODEL_DIR=/app/model
ENV API_BASE_URL=http://127.0.0.1:8000

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app.py main.py ./
COPY model ./model

EXPOSE 8000
EXPOSE 8501

CMD ["sh", "-c", "uvicorn main:app --host 0.0.0.0 --port ${PORT:-8000} & streamlit run app.py --server.port ${STREAMLIT_PORT:-8501} --server.address 0.0.0.0 --server.headless true"]
