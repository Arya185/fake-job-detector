import os
from pathlib import Path
import logging
import joblib

from fastapi import FastAPI

from models.schemas import (
    JobPosting,
    PredictionResponse,
    HistoryItem,
    HistoryResponse,
)

from services.database import (
    db_logging_enabled,
    get_db,
)

from services.predictor import predict_text

BASE_DIR = Path(__file__).resolve().parent
MODEL_DIR = Path(os.getenv("MODEL_DIR", BASE_DIR / "model"))

tfidf = joblib.load(MODEL_DIR / "tfidf_vectorizer.pkl")
clf = joblib.load(MODEL_DIR / "random_forest_model.pkl")

app = FastAPI(title="Fake Job Detector API")
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s"
)
logger = logging.getLogger(__name__)


@app.get("/")
def root():
    return {"message": "Fake Job Detector API is running ✅"}

@app.get("/health")
def health():
    return {
        "status": "ok",
        "database_logging": db_logging_enabled(),
        "model_dir": str(MODEL_DIR),
    }

@app.post("/predict", response_model=PredictionResponse)
def predict(job: JobPosting):
    return predict_text(
        job.text,
        tfidf,
        clf,
    )

@app.get("/history", response_model=HistoryResponse)

def history():
    if not db_logging_enabled():
        return {
            "history": [],
            "message": "Database logging disabled. Set ENABLE_DB_LOGGING=true and MySQL variables to enable analytics history.",
        }

    try:
        db = get_db()
        cursor = db.cursor(dictionary=True)
        cursor.execute(
            "SELECT prediction, fraud_probability, created_at FROM predictions ORDER BY created_at DESC LIMIT 50"
        )
        rows = cursor.fetchall()
        cursor.close()
        db.close()
        return {"history": rows}
    except Exception as e:
        return {"history": [], "error": str(e)}