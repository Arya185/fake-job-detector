import os
import re
from pathlib import Path
import logging
import joblib
import mysql.connector
from fastapi import FastAPI
from pydantic import BaseModel

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

def db_logging_enabled() -> bool:
    required = (
        os.getenv("MYSQL_HOST"),
        os.getenv("MYSQL_USER"),
        os.getenv("MYSQL_DATABASE"),
    )
    return os.getenv("ENABLE_DB_LOGGING", "false").lower() == "true" and all(required)


def get_db():
    if not db_logging_enabled():
        raise RuntimeError("Database logging disabled.")

    return mysql.connector.connect(
        host=os.getenv("MYSQL_HOST"),
        port=int(os.getenv("MYSQL_PORT", "3306")),
        user=os.getenv("MYSQL_USER"),
        password=os.getenv("MYSQL_PASSWORD", ""),
        database=os.getenv("MYSQL_DATABASE"),
        ssl_disabled=False,
    )

class JobPosting(BaseModel):
    text: str


def clean_text(text: str) -> str:
    if not isinstance(text, str):
        return ""
    text = text.lower()
    text = re.sub(r'<[^>]+>', ' ', text)
    text = re.sub(r'[^a-z\s]', ' ', text)
    text = re.sub(r'\s+', ' ', text).strip()
    return text

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


@app.post("/predict")
def predict(job: JobPosting):
    cleaned = clean_text(job.text)
    vec = tfidf.transform([cleaned])
    prediction = clf.predict(vec)[0]
    probability = clf.predict_proba(vec)[0]

    label = "Fake 🚨" if prediction == 1 else "Real ✅"
    confidence = round(float(max(probability)) * 100, 2)
    fraud_prob = round(float(probability[1]) * 100, 2)

    try:
        db = get_db()
        cursor = db.cursor()
        cursor.execute(
            "INSERT INTO predictions (input_text, prediction, fraud_probability) VALUES (%s, %s, %s)",
            (job.text[:500], label, fraud_prob)
        )
        db.commit()
        cursor.close()
        db.close()
    except Exception as e:
        logger.exception("Failed to log prediction to database")

    return {
        "prediction": label,
        "confidence": f"{confidence}%",
        "fraud_probability": fraud_prob
    }

@app.get("/history")
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
