# Fake Job Detector

Fake Job Detector identifies potentially fraudulent job postings with machine learning. Repository includes FastAPI inference API, Streamlit web interface, model training pipeline, Docker setup, and optional MySQL-backed prediction history.

## Features

- Detects fake vs real job postings from free-form text input
- Returns fraud probability and confidence score
- Highlights regex-based scam red flags in submitted text
- Shows analytics dashboard for recent prediction history
- Trains Random Forest model on combined job posting text fields
- Ships pretrained model artifacts for local inference
- Supports containerized deployment with FastAPI and Streamlit in one service
- Supports optional MySQL logging for prediction history

## Tech Stack

### Frontend

- Streamlit
- Custom HTML/CSS inside Streamlit

### Backend

- FastAPI
- Uvicorn
- Pydantic

### Database

- MySQL via `mysql-connector-python` for optional prediction logging

### AI/ML

- scikit-learn
- imbalanced-learn (SMOTE)
- pandas
- numpy
- joblib

### Deployment

- Docker
- Python 3.11 slim base image

## Project Structure

```text
fake-job-detector/
├── app.py
├── main.py
├── train.py
├── preprocess.py
├── requirements.txt
├── Dockerfile
├── .env.example
├── data/
│   └── fake_job_postings.csv
├── model/
│   ├── fake_job_detector.pkl
│   ├── random_forest_model.pkl
│   └── tfidf_vectorizer.pkl
└── README.md
```

## Installation

### Prerequisites

- Python 3.11 recommended
- `pip`
- Optional: MySQL server for prediction history
- Optional: Docker

### Local setup

1. Clone repository:

   ```bash
   git clone https://github.com/Arya185/fake-job-detector.git
   cd fake-job-detector
   ```

2. Create virtual environment:

   ```bash
   python -m venv .venv
   source .venv/bin/activate
   ```

3. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

4. Configure environment variables:

   ```bash
   cp .env.example .env
   ```

5. Update `.env` values if you want MySQL-backed history.

## Environment Variables

All runtime variables derived from code:

```env
API_BASE_URL=http://127.0.0.1:8000
MODEL_DIR=./model
ENABLE_DB_LOGGING=false
MYSQL_HOST=localhost
MYSQL_PORT=3306
MYSQL_USER=root
MYSQL_PASSWORD=your_mysql_password
MYSQL_DATABASE=fake_job_detector
```

### Variable notes

- `API_BASE_URL`: Base URL Streamlit uses for FastAPI requests
- `MODEL_DIR`: Directory containing `tfidf_vectorizer.pkl` and `random_forest_model.pkl`
- `ENABLE_DB_LOGGING`: Set `true` to persist predictions and enable analytics history
- `MYSQL_*`: Required only when `ENABLE_DB_LOGGING=true`

## Running Project

### Development

Run FastAPI:

```bash
uvicorn main:app --reload
```

Run Streamlit in another terminal:

```bash
streamlit run app.py
```

App URLs:

- Streamlit UI: `http://127.0.0.1:8501`
- FastAPI API: `http://127.0.0.1:8000`
- API health check: `http://127.0.0.1:8000/health`

### Production-style local run with Docker

```bash
docker build -t fake-job-detector .
docker run --rm -p 8000:8000 -p 8501:8501 --env-file .env fake-job-detector
```

## Build

### Python environment build

```bash
pip install -r requirements.txt
```

### Docker build

```bash
docker build -t fake-job-detector .
```

## Deployment

Repository supports Docker-first deployment best. Single container runs FastAPI on port `8000` and Streamlit on port `8501`.

### Suitable platforms

- Render
- Railway
- Any VM or container host that accepts Docker images

### Build command

```bash
docker build -t fake-job-detector .
```

### Start command

Container default command:

```bash
sh -c "uvicorn main:app --host 0.0.0.0 --port 8000 & streamlit run app.py --server.port 8501 --server.address 0.0.0.0 --server.headless true"
```

### Exposed ports

- `8000` for FastAPI
- `8501` for Streamlit

### Required production configuration

- Set `API_BASE_URL` to reachable FastAPI URL if frontend and API run separately
- Keep `MODEL_DIR` pointed at deployed `model/` directory
- Set `ENABLE_DB_LOGGING=true` only if MySQL database exists and contains required table

### MySQL requirement for analytics history

If history enabled, database must expose `predictions` table with columns used by code:

- `input_text`
- `prediction`
- `fraud_probability`
- `created_at`

### Domain configuration

- Point domain or platform URL to Streamlit service
- Expose FastAPI only if external API access needed

### Common deployment issues

- Streamlit cannot reach API because `API_BASE_URL` still points to localhost
- History page empty because DB logging disabled or MySQL variables missing
- Training script fails if `imbalanced-learn` not installed
- Container platform exposes only one port; in that case split API and frontend into separate services or front with reverse proxy

### Post-deployment verification

1. Open Streamlit home page.
2. Submit sample job text and confirm prediction returns.
3. Check `GET /health`.
4. If MySQL enabled, confirm `/history` returns rows after predictions.

## Usage

1. Start API and Streamlit services.
2. Open detector page in browser.
3. Paste full job description into text area.
4. Click **Analyze Posting**.
5. Review verdict, confidence, fraud risk, and detected red flags.
6. Open analytics dashboard to inspect recent history if DB logging enabled.

## Screenshots

Screenshots not present in repository yet.

- Placeholder: `docs/screenshots/detector-home.png`
- Placeholder: `docs/screenshots/detector-result.png`
- Placeholder: `docs/screenshots/analytics-dashboard.png`

## API Documentation

### `GET /`

- Purpose: basic API status message
- Authentication: none

Example response:

```json
{
  "message": "Fake Job Detector API is running ✅"
}
```

### `GET /health`

- Purpose: health check and config visibility
- Authentication: none

Example response:

```json
{
  "status": "ok",
  "database_logging": false,
  "model_dir": "/app/model"
}
```

### `POST /predict`

- Purpose: classify job posting text
- Authentication: none

Request body:

```json
{
  "text": "Remote data entry job. No experience required..."
}
```

Example response:

```json
{
  "prediction": "Fake 🚨",
  "confidence": "98.12%",
  "fraud_probability": 98.12
}
```

### `GET /history`

- Purpose: fetch recent predictions from MySQL
- Authentication: none
- Notes: returns empty history with message when DB logging disabled

Example response:

```json
{
  "history": [
    {
      "prediction": "Fake 🚨",
      "fraud_probability": 97.4,
      "created_at": "2026-07-04T00:00:00"
    }
  ]
}
```

## Architecture

1. `preprocess.py` loads CSV dataset, combines `title`, `company_profile`, `description`, `requirements`, and `benefits`, then cleans text.
2. `train.py` vectorizes text with TF-IDF, balances training data with SMOTE, trains Random Forest classifier, and saves model artifacts to `model/`.
3. `main.py` loads pretrained artifacts, exposes prediction and history endpoints, and optionally writes predictions to MySQL.
4. `app.py` provides Streamlit UI, sends text to FastAPI, displays verdict, and shows history analytics.

## Installation Process for MySQL History

MySQL setup not automated in repository. Code expects existing database named by `MYSQL_DATABASE` and table named `predictions`. Create schema before enabling `ENABLE_DB_LOGGING=true`.

## Future Improvements

- Add automated tests for API, preprocessing, and model loading
- Add migrations or SQL bootstrap script for MySQL schema
- Replace hardcoded Streamlit styling with reusable theme assets
- Add request validation and structured logging
- Serve frontend and API behind single reverse proxy for easier hosting
- Add CI for linting, tests, Docker build, and dependency checks

## License

No license file present in repository. Recommended license: MIT.

## Author

- GitHub: [Arya185](https://github.com/Arya185)
