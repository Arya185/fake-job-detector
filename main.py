import os
import re
from pathlib import Path

import joblib
import mysql.connector
from fastapi import FastAPI
from pydantic import BaseModel

# Import database setup
import setup_db

BASE_DIR = Path(__file__).resolve().parent
MODEL_DIR = Path(os.getenv("MODEL_DIR", BASE_DIR / "model"))

# Load models
tfidf = joblib.load(MODEL_DIR / "tfidf_vectorizer.pkl")
clf = joblib.load(MODEL_DIR / "random_forest_model.pkl")

app = FastAPI(title="Fake Job Detector API")


# Database initialization on startup
@app.on_event("startup")
def startup_event():
    """Initialize database on application startup."""
    if db_logging_enabled():
        print("🔄 Setting up database...")
        success = setup_db.setup_database()
        if success:
            print("✅ Database ready for logging")
        else:
            print("⚠️ Database setup failed. Predictions will still work but won't be logged.")
    else:
        print("ℹ️ Database logging is disabled")


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

    # Log to database if enabled
    if db_logging_enabled():
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
            print(f"✅ Prediction logged: {label} (fraud: {fraud_prob}%)")
        except Exception as e:
            print(f"⚠️ Failed to log prediction: {e}")

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


# Optional: Add a stats endpoint for analytics
@app.get("/stats")
def stats():
    """Get statistics about predictions."""
    if not db_logging_enabled():
        return {
            "error": "Database logging disabled. Enable to view stats."
        }
    
    try:
        db = get_db()
        cursor = db.cursor(dictionary=True)
        
        # Get total count
        cursor.execute("SELECT COUNT(*) as total FROM predictions")
        total = cursor.fetchone()['total']
        
        # Get fake vs real counts
        cursor.execute("""
            SELECT 
                prediction,
                COUNT(*) as count,
                AVG(fraud_probability) as avg_fraud_prob
            FROM predictions 
            GROUP BY prediction
        """)
        distribution = cursor.fetchall()
        
        # Get recent activity (last 7 days)
        cursor.execute("""
            SELECT 
                DATE(created_at) as date,
                COUNT(*) as count
            FROM predictions 
            WHERE created_at >= DATE_SUB(NOW(), INTERVAL 7 DAY)
            GROUP BY DATE(created_at)
            ORDER BY date DESC
        """)
        recent_activity = cursor.fetchall()
        
        cursor.close()
        db.close()
        
        return {
            "total_predictions": total,
            "distribution": distribution,
            "recent_activity": recent_activity
        }
    except Exception as e:
        return {"error": str(e)}
