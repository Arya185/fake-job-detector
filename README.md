# 🛡️ FraudScan AI — Fake Job Detector

[![Python Version](https://img.shields.io/badge/python-3.11-blue.svg)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.135.3-green.svg)](https://fastapi.tiangolo.com/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.55.0-red.svg)](https://streamlit.io/)
[![Scikit-Learn](https://img.shields.io/badge/scikit--learn-1.8.0-orange.svg)](https://scikit-learn.org/)
[![License](https://img.shields.io/badge/license-MIT-brightgreen.svg)](#license)

An AI-powered web application and REST API designed to detect fraudulent job postings using machine learning. It protects job seekers from employment scams by identifying red flags and estimating the likelihood of fraud in job descriptions.

🔗 **Live Application URL:** [https://fake-job-detector-app-qa6q.onrender.com/](https://fake-job-detector-app-qa6q.onrender.com/)

---

## 📌 Overview

Employment scams are on the rise, targeting vulnerable job seekers. This project solves that problem by providing an automated tool to scan and evaluate job descriptions. 

*   **What it does:** Classifies job postings into "Real" or "Fake" based on text content.
*   **How it works:** Uses natural language processing (NLP) to vectorize job details and runs a machine learning classifier to calculate fraud risk.
*   **Why it is useful:** Instantly flags potential scams, highlights known fraud-like text patterns, and provides an analytics dashboard for tracking scans.

---

## 🚀 Live Demo

Access the active frontend deployed on Render:
👉 **[FraudScan AI Web App](https://fake-job-detector-app-qa6q.onrender.com/)**

---

## ⚡ Features

*   **Fake Job Detection:** Paste any job title, requirements, or descriptions to check for fraud risk.
*   **AI/ML Prediction:** Powered by a Random Forest Classifier trained on combined text fields (title, company profile, description, requirements, benefits).
*   **Confidence & Risk Meter:** Displays the raw probability percentage of fraud alongside a confidence rating.
*   **Heuristic Red Flags:** Scans the text using regex rules to extract common scam patterns (e.g., unrealistic salary claims, urgency tactics, requests for bank details, WhatsApp-only contact).
*   **Interactive Analytics Dashboard:** Visualizes real-time distribution charts, average fraud risk, and recent prediction histories.
*   **Dual-Service API Integration:** Built as decoupled frontend (Streamlit) and backend (FastAPI) applications that communicate over REST.
*   **Optional Persistent Database Logging:** Saves predictions to an external MySQL database for analytics tracking when logging is enabled.

---

## 🛠️ Tech Stack

### Languages & Core Runtimes
*   **Python 3.11** - Main programming language.
*   **HTML5 / CSS3** - Custom styling embedded in Streamlit.

### Frontend
*   **Streamlit (v1.55.0)** - Interactive UI for the detector and analytics dashboard.
*   **Requests (v2.33.0)** - Handles HTTP calls to the FastAPI backend.
*   **Pandas & NumPy** - Data handling and visualization for the dashboard.

### Backend (REST API)
*   **FastAPI (v0.135.3)** - High-performance backend API framework.
*   **Uvicorn (v0.44.0)** - ASGI server process to run FastAPI.
*   **Pydantic (v2.9.2)** - Data validation and request payload enforcement.

### Machine Learning
*   **scikit-learn (v1.8.0)** - TF-IDF feature extraction and Random Forest model training.
*   **imbalanced-learn (v0.14.2)** - Handles class imbalance using SMOTE (Synthetic Minority Over-sampling Technique).
*   **joblib (v1.5.3)** - Serializes and loads pre-trained model files.

### Database
*   **MySQL** - Stores predictions (optional history log).
*   **mysql-connector-python (v9.6.0)** - Python driver for MySQL connections.

### Deployment & DevOps
*   **Docker** - Standardized multi-stage containers based on `python:3.11-slim`.
*   **Render** - Deployed as decoupled Docker services (API + Web Frontend).

---

## 📂 Project Structure

```text
fake-job-detector/
├── .dockerignore         # Excludes virtual environments and training datasets from builds
├── .env.example          # Template configuration file for environment variables
├── .gitignore            # Git ignore file
├── Dockerfile            # Multi-service production Docker configuration
├── README.md             # Project documentation (this file)
├── app.py                # Streamlit web application code
├── main.py               # FastAPI backend router and prediction service
├── preprocess.py         # Text preprocessing helper functions
├── render.yaml           # Render Blueprint specification for multi-service deployment
├── requirements.txt      # Python dependencies manifest
├── train.py              # Machine learning training pipeline
├── data/
│   └── fake_job_postings.csv  # ~50MB raw training dataset
└── model/
    ├── fake_job_detector.pkl  # Retained baseline model (unused)
    ├── random_forest_model.pkl # Active trained Random Forest classifier
    └── tfidf_vectorizer.pkl   # Active TF-IDF Vectorizer
```

---

## ⚙️ Installation & Local Setup

### Prerequisites
*   Python 3.11 installed.
*   *Optional:* A MySQL instance (only required if database logging is enabled).

### 1. Clone the Repository
```bash
git clone https://github.com/Arya185/fake-job-detector.git
cd fake-job-detector
```

### 2. Configure Environment Variables
Create your environment configuration file from the template:
```bash
cp .env.example .env
```
*(By default, database logging is disabled, so you do not need to configure MySQL credentials to run locally.)*

### 3. Create a Virtual Environment & Install Dependencies
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### 4. Run the Backend API
Start the FastAPI server on port 8000:
```bash
python3 -m uvicorn main:app --host 0.0.0.0 --port 8000
```
Verify the API is active by visiting `http://localhost:8000/health` in your browser.

### 5. Run the Streamlit Frontend
In a new terminal window (with the virtual environment activated), start the UI:
```bash
python3 -m streamlit run app.py --server.port 8501 --server.address 0.0.0.0
```
Open `http://localhost:8501` to use the application.

---

## 🔒 Environment Variables

| Variable | Default Value | Description |
| :--- | :--- | :--- |
| `API_BASE_URL` | `http://127.0.0.1:8000` | The backend API URL that the Streamlit frontend calls. |
| `MODEL_DIR` | `./model` | Directory where the `.pkl` model and vectorizer files are located. |
| `ENABLE_DB_LOGGING` | `false` | Set to `true` to log predictions and load historical charts in MySQL. |
| `MYSQL_HOST` | `localhost` | Host address of the MySQL database. |
| `MYSQL_PORT` | `3306` | Port of the MySQL database. |
| `MYSQL_USER` | `root` | Username of the MySQL database. |
| `MYSQL_PASSWORD` | `""` | Password of the MySQL database (leave empty for blank passwords). |
| `MYSQL_DATABASE` | `fake_job_detector` | Name of the database to log data to. |

---

## 💡 Usage

1.  **Start the Apps:** Ensure the FastAPI backend is running before launching the Streamlit app.
2.  **Paste Description:** Open the Streamlit UI, choose the **🔍 Detector** page, and paste a job posting (including title, description, benefits, and requirements) into the text box.
3.  **Analyze Posting:** Click **🔎 Analyze Posting**.
4.  **Interpret the AI Verdict:**
    *   **Real Verdict (Green Card):** Indicates that the job contains standard phrasing and low fraud traits.
    *   **Fake Verdict (Red Card):** Indicates that the job has high risk patterns or text features matching previous scams.
    *   **Risk & Confidence:** Look at the *Fraud Risk Meter* and *Confidence Score* to assess the certainty.
    *   **Heuristic Red Flags:** Check the bottom section for flagged regex patterns matching urgency words or suspicious payment terms.
5.  **Analytics:** Navigate to the **📊 Analytics Dashboard** on the sidebar to view aggregate stats on all historical predictions (requires `ENABLE_DB_LOGGING=true`).

---

## 🔌 API Documentation

The FastAPI backend exposes the following REST endpoints:

| Method | Endpoint | Request Body | Response Format | Description |
| :--- | :--- | :--- | :--- | :--- |
| **GET** | `/` | None | `{"message": "..."}` | Basic API status check. |
| **GET** | `/health` | None | `{"status": "...", "database_logging": bool, ...}` | Returns health status and directory variables. |
| **POST** | `/predict` | `{"text": "string"}` | `{"prediction": "Real/Fake", "confidence": "X%", "fraud_probability": Y}` | Evaluates a job description and returns classification metrics. |
| **GET** | `/history` | None | `{"history": [...]}` | Retrieves the last 50 logged predictions (returns empty list if database logging is disabled). |

---

## 📷 Screenshots

### 🔍 Detector Page
*Placeholder: `docs/screenshots/detector-home.png`*
*Placeholder: `docs/screenshots/detector-result.png`*

### 📊 Analytics Dashboard
*Placeholder: `docs/screenshots/analytics-dashboard.png`*

---

## 📊 Model Information

### Dataset
*   **Source:** Real-world dataset containing **17,880 rows** of job postings.
*   **Imbalance:** Extremely imbalanced with **17,014 real** postings (95.16%) and **866 fake** postings (4.84%).

### Preprocessing
1.  **Feature Combination:** Combines the text fields `title`, `company_profile`, `description`, `requirements`, and `benefits` into a single text block.
2.  **Cleaning:** Converts to lowercase, strips HTML tags, removes special characters/numbers, and normalizes whitespaces.
3.  **Vectorization:** Vectorizes the clean text using a TF-IDF Vectorizer with `ngram_range=(1, 3)`, `max_features=15000`, and `sublinear_tf=True`.
4.  **Sampling (SMOTE):** Applies SMOTE to balance the training set, generating synthetic fake postings to equal the real postings (balancing train size to 27,222 samples).

### Model Architecture
*   **Algorithm:** Random Forest Classifier
*   **Parameters:** `n_estimators=200`, `max_depth=20`, `class_weight='balanced'`, `n_jobs=-1`.

### Performance Metrics
Trained locally on a stratified 80/20 split:

*   **Overall Accuracy:** **98.41%**
*   **Classification Report:**

| Class | Precision | Recall | F1-Score | Support |
| :--- | :---: | :---: | :---: | :---: |
| **Real** | 0.98 | 1.00 | 0.99 | 3,403 |
| **Fake** | 0.97 | 0.69 | 0.81 | 173 |

### Model Limitations
*   **High Precision, Moderate Recall:** The model has high precision for fake jobs (0.97), meaning if it flags a job as fake, it is almost certainly a scam. However, its recall is 0.69, meaning it misses roughly 31% of scams. Users should still exercise caution even if a job is labeled as "Real".
*   **Text Dependency:** It does not review company domains, links, or contact emails (unless embedded in the description text).

---

## ☁️ Deployment

The project is deployed on **Render** under a Blueprint multi-service arrangement.

*   **Live App URL:** [https://fake-job-detector-app-qa6q.onrender.com/](https://fake-job-detector-app-qa6q.onrender.com/)

### Deplaying to Render Yourself
1.  Fork this repository.
2.  Go to the [Render Dashboard](https://dashboard.render.com/).
3.  Click **New > Blueprint**.
4.  Connect your GitHub fork and choose the repository.
5.  Render will parse the [render.yaml](file:///Users/aryapatel/arya/Programming/code/fake-job-detector/render.yaml) specification file and automatically provision:
    *   `fake-job-detector-api` (API backend running FastAPI).
    *   `fake-job-detector-app` (Web Frontend running Streamlit).
6.  Once built, your web app will be live.

---

## 🔮 Future Improvements

*   **Improve Recall for Fake Class:** Experiment with deep learning (e.g. BERT or DistilBERT) to capture finer contextual nuances.
*   **Domain & Email Verification:** Add heuristics that check if the recruiter's email domain exists or is associated with high-risk free email hosts.
*   **Dynamic Scraping:** Add a feature allowing users to paste a URL from LinkedIn or Indeed, scraping the job details on the fly.
*   **User Feedback Loop:** Allow users to flag incorrect predictions, collecting feedback to retrain and update models.

---

## 🤝 Contributing

Contributions are welcome! Please follow these steps:

1.  Fork the Project.
2.  Create your Feature Branch (`git checkout -b feature/AmazingFeature`).
3.  Commit your Changes (`git commit -m 'feat: add some amazing feature'`).
4.  Push to the Branch (`git push origin feature/AmazingFeature`).
5.  Open a Pull Request.

---

## 📄 License

No license is currently checked into this repository. It is recommended that this project use the **MIT License**.

---

## 👤 Author

*   **Github:** [@Arya185](https://github.com/Arya185)
