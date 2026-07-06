# FraudScan AI — Fake Job Detector

[![Python](https://img.shields.io/badge/python-3.11-blue.svg)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.135.3-green.svg)](https://fastapi.tiangolo.com/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.55.0-red.svg)](https://streamlit.io/)
[![scikit-learn](https://img.shields.io/badge/scikit--learn-1.8.0-orange.svg)](https://scikit-learn.org/)
[![Deployed on Render](https://img.shields.io/badge/deployed%20on-Render-46E3B7.svg)](https://render.com/)

An AI-powered web application and REST API that helps job seekers identify potentially fraudulent job postings. The system combines a trained Random Forest classifier with rule-based red-flag detection to classify postings as real or fake and surface common scam patterns.

---

## Live Demo

**Try the application:** [https://fake-job-detector-app-qa6q.onrender.com/](https://fake-job-detector-app-qa6q.onrender.com/)

The live deployment runs on [Render](https://render.com/) as two Docker web services: a FastAPI backend for ML inference and a Streamlit frontend for the user interface.

---

## Features

- **ML-based classification** — Random Forest model trained on 17,880 job postings predicts whether a posting is real or fake.
- **REST API** — FastAPI backend exposes health checks, prediction, and history endpoints.
- **Interactive web UI** — Streamlit frontend with a polished, responsive layout for analyzing job descriptions.
- **Fraud risk metrics** — Displays fraud probability percentage, model confidence, and a visual risk meter.
- **Heuristic red-flag scanner** — 18 regex-based rules detect common scam signals (unrealistic pay, urgency tactics, bank-detail requests, suspicious contact methods, MLM language, and more).
- **Analytics dashboard** — Aggregates scan statistics, distribution charts, and a recent-predictions table when database logging is enabled.
- **Optional MySQL logging** — Persists predictions for historical analytics (disabled by default).
- **Docker support** — Single Dockerfile serves both API and frontend via configurable commands.
- **Render Blueprint** — One-click multi-service deployment via `render.yaml`.
- **Model training pipeline** — Reproducible training script with TF-IDF vectorization, SMOTE oversampling, and model export.

---

## Screenshots

| Page | Placeholder |
|-------|-------------|
| Detector — Input | <img width="1440" height="799" alt="image" src="https://github.com/user-attachments/assets/41783d12-8b47-45a5-b514-ebb1424b56f2" /> |
| Detector — Result | <img width="1440" height="799" alt="image" src="https://github.com/user-attachments/assets/d7fa92fd-7f96-4794-a9ae-f37def0ea824" /> |
| Analytics dashboard | <img width="1440" height="799" alt="image" src="https://github.com/user-attachments/assets/7698a488-f91c-44c5-858b-53789c64fb08" /> |
|-------|-------------|

---

## Tech Stack

| Layer | Technologies |
|-------|-------------|
| **Language** | Python 3.11 |
| **Frontend** | Streamlit 1.55.0, Requests, Pandas, custom CSS (Inter font) |
| **Backend** | FastAPI 0.135.3, Uvicorn 0.44.0, Pydantic 2.x |
| **Machine Learning** | scikit-learn 1.8.0, imbalanced-learn 0.14.2 (SMOTE), joblib 1.5.3 |
| **Database** | MySQL (optional), mysql-connector-python 9.6.0 |
| **Deployment** | Docker, Render Blueprint |

---

## Project Architecture

```
┌─────────────────────┐         HTTP (REST)         ┌─────────────────────┐
│  Streamlit Frontend │  ─────────────────────────► │   FastAPI Backend   │
│       (app.py)      │  POST /predict, GET /history│      (main.py)      │
└─────────────────────┘                             └──────────┬──────────┘
                                                                 │
                                    ┌────────────────────────────┼────────────────────────────┐
                                    │                            │                            │
                                    ▼                            ▼                            ▼
                          tfidf_vectorizer.pkl        random_forest_model.pkl          MySQL (optional)
                                                                                    predictions table
```

The frontend and backend are decoupled services. The Streamlit app calls the FastAPI API for predictions and history; the API loads serialized ML artifacts at startup and optionally writes results to MySQL.

---

## Folder Structure

```text
fake-job-detector/
├── .dockerignore              # Docker build exclusions (venv, .env, training CSV)
├── .env.example               # Environment variable template
├── .gitignore
├── Dockerfile                 # Shared image for API and Streamlit services
├── README.md
├── app.py                     # Streamlit web application (Detector + Analytics)
├── main.py                    # FastAPI backend (prediction + history API)
├── preprocess.py              # Dataset loading and text cleaning utilities
├── train.py                   # ML training pipeline
├── render.yaml                # Render Blueprint (API + frontend services)
├── requirements.txt           # Python dependencies
├── data/
│   ├── .gitkeep
│   └── fake_job_postings.csv  # Training dataset (~17,880 job postings)
└── model/
    ├── .gitkeep
    ├── fake_job_detector.pkl      # Legacy baseline model (not used at runtime)
    ├── random_forest_model.pkl    # Active Random Forest classifier
    └── tfidf_vectorizer.pkl       # Active TF-IDF vectorizer
```

---

## How It Works

### 1. User input

A user pastes a job description (title, company profile, requirements, benefits, etc.) into the Streamlit **Detector** page and clicks **Analyze Posting**.

### 2. API prediction

The frontend sends a `POST /predict` request with the raw text. The backend:

1. Cleans the text (lowercase, strip HTML, remove special characters and numbers, normalize whitespace).
2. Transforms the cleaned text with the pre-trained TF-IDF vectorizer.
3. Runs inference with the Random Forest classifier.
4. Returns the label (`Real` or `Fake`), confidence score, and fraud probability.
5. Optionally inserts the result into MySQL when database logging is enabled.

### 3. Red-flag heuristics

In parallel on the frontend, regex patterns scan the original text for known scam indicators (e.g., unrealistic salary claims, bank-detail requests, WhatsApp-only contact).

### 4. Analytics (optional)

When `ENABLE_DB_LOGGING=true` and MySQL is configured, predictions are stored in a `predictions` table. The **Analytics Dashboard** page fetches the last 50 records via `GET /history` and renders summary metrics and charts.

### Model training

Run `python train.py` to retrain from `data/fake_job_postings.csv`:

- Combines `title`, `company_profile`, `description`, `requirements`, and `benefits` into a single text field.
- Applies TF-IDF (`max_features=15000`, `ngram_range=(1, 3)`, English stop words, `sublinear_tf=True`).
- Balances the training set with SMOTE.
- Trains a Random Forest (`n_estimators=200`, `max_depth=20`, `class_weight='balanced'`).
- Saves `model/tfidf_vectorizer.pkl` and `model/random_forest_model.pkl`.

**Dataset:** 17,880 postings — 17,014 real (95.2%) and 866 fake (4.8%).

**Evaluation (80/20 stratified split):** 98.41% accuracy; fake-class precision 0.97, recall 0.69.

---

## Installation

### Prerequisites

- Python 3.11
- Git
- *(Optional)* MySQL 8+ if enabling database logging

### Steps

```bash
git clone https://github.com/Arya185/fake-job-detector.git
cd fake-job-detector

python3 -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate

pip install -r requirements.txt
```

Copy the environment template and adjust values as needed:

```bash
cp .env.example .env
```

Ensure the trained model artifacts exist in `model/` (`random_forest_model.pkl` and `tfidf_vectorizer.pkl`). They are included in the repository. To regenerate them, run:

```bash
python train.py
```

---

## Environment Variables

| Variable | Default | Required | Description |
|----------|---------|----------|-------------|
| `API_BASE_URL` | `http://127.0.0.1:8000` | Frontend | Base URL of the FastAPI backend (no trailing slash). |
| `MODEL_DIR` | `./model` | Backend | Directory containing `tfidf_vectorizer.pkl` and `random_forest_model.pkl`. |
| `ENABLE_DB_LOGGING` | `false` | Backend | Set to `true` to enable MySQL prediction logging and analytics history. |
| `MYSQL_HOST` | — | If logging enabled | MySQL server hostname. |
| `MYSQL_PORT` | `3306` | If logging enabled | MySQL server port. |
| `MYSQL_USER` | — | If logging enabled | MySQL username. |
| `MYSQL_PASSWORD` | `""` | If logging enabled | MySQL password. |
| `MYSQL_DATABASE` | — | If logging enabled | Database name (e.g., `fake_job_detector`). |

When database logging is enabled, create a `predictions` table:

```sql
CREATE TABLE predictions (
    id INT AUTO_INCREMENT PRIMARY KEY,
    input_text VARCHAR(500) NOT NULL,
    prediction VARCHAR(50) NOT NULL,
    fraud_probability FLOAT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

---

## Running Locally

Start the **backend** first:

```bash
python3 -m uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

Verify: [http://localhost:8000/health](http://localhost:8000/health)

In a second terminal, start the **frontend**:

```bash
python3 -m streamlit run app.py --server.port 8501 --server.address 0.0.0.0
```

Open [http://localhost:8501](http://localhost:8501) in your browser.

### Docker (local)

Build and run the API:

```bash
docker build -t fake-job-detector .
docker run -p 8000:8000 fake-job-detector
```

Run the Streamlit frontend (override the default command):

```bash
docker run -p 8501:8501 \
  -e API_BASE_URL=http://host.docker.internal:8000 \
  fake-job-detector \
  python -m streamlit run app.py --server.port 8501 --server.address 0.0.0.0 --server.headless true
```

---

## API Endpoints

Base URL (local): `http://localhost:8000`

Interactive docs: [http://localhost:8000/docs](http://localhost:8000/docs) (Swagger UI)

### `GET /`

Basic status check.

**Response:**

```json
{
  "message": "Fake Job Detector API is running ✅"
}
```

---

### `GET /health`

Health check with configuration details.

**Response:**

```json
{
  "status": "ok",
  "database_logging": false,
  "model_dir": "./model"
}
```

---

### `POST /predict`

Classify a job posting.

**Request body:**

```json
{
  "text": "Senior Software Engineer at Acme Corp. Requirements: 5+ years Python..."
}
```

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `text` | string | Yes | Full job posting text to analyze. |

**Response:**

```json
{
  "prediction": "Real ✅",
  "confidence": "94.12%",
  "fraud_probability": 5.88
}
```

| Field | Type | Description |
|-------|------|-------------|
| `prediction` | string | `"Real ✅"` or `"Fake 🚨"` |
| `confidence` | string | Model confidence as a percentage string |
| `fraud_probability` | float | Probability of fraud (0–100) |

---

### `GET /history`

Retrieve the 50 most recent logged predictions.

**Response (logging disabled):**

```json
{
  "history": [],
  "message": "Database logging disabled. Set ENABLE_DB_LOGGING=true and MySQL variables to enable analytics history."
}
```

**Response (logging enabled):**

```json
{
  "history": [
    {
      "prediction": "Fake 🚨",
      "fraud_probability": 87.5,
      "created_at": "2026-07-05T10:30:00"
    }
  ]
}
```

---

## Deployment

This project is deployed on **Render** using a Blueprint defined in `render.yaml`.

**Live application:** [https://fake-job-detector-app-qa6q.onrender.com/](https://fake-job-detector-app-qa6q.onrender.com/)

### Render services

| Service | Command | Health check |
|---------|---------|--------------|
| `fake-job-detector-api` | `uvicorn main:app --host 0.0.0.0 --port 10000` | `/health` |
| `fake-job-detector-app` | `streamlit run app.py --server.port 10000 ...` | `/` |

The frontend receives `API_BASE_URL` automatically from the API service's `RENDER_EXTERNAL_URL`.

### Deploy your own instance

1. Fork this repository.
2. Open the [Render Dashboard](https://dashboard.render.com/).
3. Click **New → Blueprint** and connect your fork.
4. Render provisions both services from `render.yaml`.
5. *(Optional)* Enable MySQL logging by setting `ENABLE_DB_LOGGING=true` and the MySQL environment variables on the API service.

---

## Future Improvements

- Improve fake-class recall with transformer-based models (e.g., BERT, DistilBERT).
- Add domain and email verification heuristics for recruiter contact information.
- Support job URL input with automatic scraping from LinkedIn, Indeed, and similar platforms.
- Collect user feedback on incorrect predictions to support continuous model retraining.
- Add automated tests and CI for API endpoints and preprocessing logic.
- Include OpenAPI-generated client SDKs and rate limiting for public API usage.

---

## Contributing

Contributions are welcome. To propose a change:

1. Fork the repository.
2. Create a feature branch: `git checkout -b feature/your-feature-name`
3. Commit your changes using [Conventional Commits](https://www.conventionalcommits.org/): `git commit -m 'feat: add your feature'`
4. Push to your fork: `git push origin feature/your-feature-name`
5. Open a pull request against `main`.

---

## License

This project is licensed under the terms of the [MIT license](https://github.com/Arya185/fake-job-detector?tab=MIT-1-ov-file).

---

## Author

**Arya Patel** — [GitHub @Arya185](https://github.com/Arya185)

---

## Note

Created readme.md using Cursor Agent
