I have worked on it take a look at it but there is some errors:
File "/app/app.py", line 553
              st.markdown("""
                          ^
SyntaxError: unterminated triple-quoted string literal (detected at line 557)


import streamlit as st
import requests
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import re
import os
import time
from datetime import datetime

API_BASE_URL = os.getenv("API_BASE_URL", "http://127.0.0.1:8000").rstrip("/")

st.set_page_config(
    page_title="FraudScan AI — Advanced Job Risk Analytics",
    page_icon="🛡️",
    layout="wide"
)

# Premium Custom Styling Overrides (Stripe, Linear, and Vercel theme integration)
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&display=swap');

* {
    font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, sans-serif;
}

/* Background & main card layouts */
.stApp {
    background-color: #080B11 !important;
    color: #F8FAFC !important;
}

/* Glassmorphic layered card containers styling Streamlit native container borders */
div[data-testid="stVerticalBlockBorder"] {
    background: rgba(17, 24, 39, 0.7) !important;
    backdrop-filter: blur(16px) !important;
    border: 1px solid rgba(255, 255, 255, 0.08) !important;
    border-radius: 20px !important;
    padding: 24px 30px !important;
    box-shadow: 0 12px 40px rgba(0, 0, 0, 0.4), inset 0 1px 0 rgba(255, 255, 255, 0.05) !important;
    margin-bottom: 25px !important;
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
}

div[data-testid="stVerticalBlockBorder"]:hover {
    border-color: rgba(124, 92, 255, 0.3) !important;
    box-shadow: 0 12px 40px rgba(124, 92, 255, 0.08) !important;
}

.saas-card-header {
    font-size: 1.15rem;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 1px;
    color: #94A3B8;
    margin-top: 5px;
    margin-bottom: 20px;
    border-bottom: 1px solid rgba(255, 255, 255, 0.06);
    padding-bottom: 12px;
}

/* Scrollbars overrides */
::-webkit-scrollbar {
    width: 8px;
    height: 8px;
}
::-webkit-scrollbar-track {
    background: #080B11;
}
::-webkit-scrollbar-thumb {
    background: #1E293B;
    border-radius: 4px;
}
::-webkit-scrollbar-thumb:hover {
    background: #334155;
}

/* Base dividers override */
hr {
    border-color: rgba(255, 255, 255, 0.06) !important;
    margin: 22px 0 !important;
}

/* Widget UI enhancements */
div[data-baseweb="select"] > div {
    background-color: rgba(15, 23, 42, 0.8) !important;
    border: 1px solid rgba(255, 255, 255, 0.1) !important;
    border-radius: 12px !important;
    color: #F8FAFC !important;
}

div[data-baseweb="slider"] {
    padding-bottom: 12px !important;
}

div[role="slider"] {
    background-color: #7C5CFF !important;
}

/* Custom styled buttons targeting Streamlit primary and secondary states */
div.stButton > button[kind="primary"] {
    background: linear-gradient(135deg, #7C5CFF 0%, #A855F7 100%) !important;
    color: white !important;
    border: none !important;
    border-radius: 12px !important;
    padding: 10px 24px !important;
    font-weight: 700 !important;
    font-size: 0.95rem !important;
    box-shadow: 0 4px 15px rgba(124, 92, 255, 0.25) !important;
    transition: all 0.25s !important;
    height: 45px !important;
}

div.stButton > button[kind="primary"]:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 8px 25px rgba(124, 92, 255, 0.4) !important;
}

div.stButton > button[kind="secondary"] {
    background-color: rgba(255, 255, 255, 0.04) !important;
    color: #E2E8F0 !important;
    border: 1px solid rgba(255, 255, 255, 0.08) !important;
    border-radius: 12px !important;
    padding: 10px 24px !important;
    font-weight: 600 !important;
    transition: all 0.25s !important;
    height: 45px !important;
}

div.stButton > button[kind="secondary"]:hover {
    background-color: rgba(255, 255, 255, 0.08) !important;
    border-color: rgba(255, 255, 255, 0.15) !important;
}

/* SaaS dashboard metrics */
.dashboard-stat-card {
    background: linear-gradient(135deg, rgba(30, 41, 59, 0.6) 0%, rgba(15, 23, 42, 0.8) 100%);
    border: 1px solid rgba(255, 255, 255, 0.06);
    border-radius: 16px;
    padding: 24px;
    text-align: left;
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    box-shadow: 0 4px 20px rgba(0, 0, 0, 0.2);
}

.dashboard-stat-card:hover {
    transform: translateY(-4px);
    border-color: rgba(124, 92, 255, 0.4);
    box-shadow: 0 12px 30px rgba(124, 92, 255, 0.15);
}

.dashboard-stat-val {
    font-size: 2.3rem;
    font-weight: 800;
    color: #FFFFFF;
    line-height: 1;
    margin-bottom: 4px;
    background: linear-gradient(90deg, #FFFFFF 0%, #E2E8F0 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}

.dashboard-stat-label {
    font-size: 0.85rem;
    font-weight: 600;
    color: #94A3B8;
    text-transform: uppercase;
    letter-spacing: 0.5px;
}

/* Hero Section */
.hero-wrapper {
    text-align: center;
    padding: 60px 0 35px;
}

.hero-title {
    font-size: 58px;
    font-weight: 800;
    letter-spacing: -1.5px;
    line-height: 1.1;
    margin-bottom: 12px;
    background: linear-gradient(135deg, #FFF 30%, #7C5CFF 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}

.hero-subtitle {
    font-size: 1.25rem;
    font-weight: 500;
    color: #E2E8F0;
    line-height: 1.4;
    margin-bottom: 16px;
}

.hero-desc {
    width: 65%;
    margin: auto;
    font-size: 1rem;
    color: #94A3B8;
    line-height: 1.7;
}

/* Findings and Signals Cards */
.finding-card {
    background: rgba(15, 23, 42, 0.5);
    border: 1px solid rgba(255, 255, 255, 0.05);
    border-radius: 14px;
    padding: 20px;
    margin-bottom: 16px;
    transition: border-color 0.25s;
}

.finding-card:hover {
    border-color: rgba(255, 255, 255, 0.12);
}

.severity-pill-danger {
    background: rgba(239, 68, 68, 0.1);
    color: #F87171;
    border: 1px solid rgba(239, 68, 68, 0.2);
    font-size: 0.75rem;
    font-weight: 700;
    padding: 2px 10px;
    border-radius: 20px;
    text-transform: uppercase;
}

.severity-pill-warning {
    background: rgba(245, 158, 11, 0.1);
    color: #FBBF24;
    border: 1px solid rgba(245, 158, 11, 0.2);
    font-size: 0.75rem;
    font-weight: 700;
    padding: 2px 10px;
    border-radius: 20px;
    text-transform: uppercase;
}

.severity-pill-info {
    background: rgba(59, 130, 246, 0.1);
    color: #60A5FA;
    border: 1px solid rgba(59, 130, 246, 0.2);
    font-size: 0.75rem;
    font-weight: 700;
    padding: 2px 10px;
    border-radius: 20px;
    text-transform: uppercase;
}

/* Expanders override */
.streamlit-expanderHeader {
    background: rgba(30, 41, 59, 0.4) !important;
    border-radius: 12px !important;
    border: 1px solid rgba(255, 255, 255, 0.06) !important;
    color: #F1F5F9 !important;
    font-weight: 600 !important;
    padding: 12px 18px !important;
}

/* Layout inputs styling overrides */
.stTextArea textarea {
    background-color: rgba(15, 23, 42, 0.8) !important;
    border: 1px solid rgba(255, 255, 255, 0.1) !important;
    color: #F8FAFC !important;
    border-radius: 14px !important;
    font-size: 0.95rem !important;
    line-height: 1.6 !important;
    padding: 18px !important;
    transition: all 0.2s;
}

.stTextArea textarea:focus {
    border-color: #7C5CFF !important;
    box-shadow: 0 0 0 3px rgba(124, 92, 255, 0.2) !important;
}

/* File Upload drag area overrides */
.stFileUploader section {
    background-color: rgba(15, 23, 42, 0.4) !important;
    border: 1px dashed rgba(255, 255, 255, 0.15) !important;
    border-radius: 14px !important;
    padding: 20px !important;
}

.footer {
    text-align: center;
    color: #475569;
    font-size: 0.85rem;
    margin-top: 50px;
    padding-top: 25px;
    border-top: 1px solid rgba(255, 255, 255, 0.05);
}
</style>
""", unsafe_allow_html=True)

# Regex-based red flag patterns (Frontend Heuristics)
RED_FLAG_PATTERNS = [
    (r"earn(ing)?\s*\$[\d,]+", "💸 Earning promise with specific dollar amount"),
    (r"\$[\d,]+\s*(per|a|/)?\s*(week|day|hour|month)", "💸 Unrealistic salary claim"),
    (r"no\s+experience\s+(needed|required|necessary)", "🚫 No experience required"),
    (r"work\s*(from)?\s*home", "🏠 Work from home offer"),
    (r"guaranteed\s+(income|salary|pay|money)", "⚠️ Guaranteed income promise"),
    (r"(send|provide|submit).{0,30}(bank|account|routing)\s*(details|info|number)", "🏦 Bank details requested"),
    (r"(wire\s*transfer|western\s*union|moneygram)", "🏦 Suspicious payment method"),
    (r"no\s+interview(s)?", "🚫 No interview required"),
    (r"(urgent(ly)?|immediate(ly)?)\s+hiring", "🚨 Urgency hiring tactic"),
    (r"make\s+money\s+fast", "💸 Make money fast claim"),
    (r"unlimited\s+(income|earning|money)", "💸 Unlimited income promise"),
    (r"be\s+your\s+own\s+boss", "👔 Be your own boss"),
    (r"(whatsapp|telegram|signal)\s*(me|us|only)", "📱 Suspicious contact method"),
    (r"(100%|hundred\s+percent)\s+(legit|legitimate|real|genuine)", "⚠️ Overemphatic legitimacy claim"),
    (r"paid?\s+(daily|weekly)\s+(cash|direct)", "💸 Suspicious payment terms"),
    (r"(multi.?level|mlm|network)\s*marketing", "🚨 MLM/Network marketing"),
    (r"investment\s*(of|required|needed).{0,20}\$[\d,]+", "💰 Upfront investment required"),
    (r"(part[\s-]?time|flexible\s+hours).{0,30}\$[\d,]+", "💸 Suspicious part-time income"),
]

def check_red_flags(text):
    found = []
    for pattern, label in RED_FLAG_PATTERNS:
        matches = re.findall(pattern, text.lower())
        if matches:
            match_text = matches[0] if isinstance(matches[0], str) else matches[0][0]
            found.append({"label": label, "match": match_text})
    return found

# ---- SIDEBAR STATUS CHECK ----
def query_api_health():
    try:
        response = requests.get(f"{API_BASE_URL}/health", timeout=3)
        if response.status_code == 200:
            return response.json(), True
        else:
            return None, False
    except Exception:
        return None, False

api_health, is_api_online = query_api_health()

# ---- SIDEBAR ----
with st.sidebar:
    st.markdown("<div style='padding: 10px 0;'><h2 style='font-size:1.6rem; font-weight:800; background:linear-gradient(90deg, #FFF 0%, #7C5CFF 100%); -webkit-background-clip:text; -webkit-text-fill-color:transparent; margin:0;'>🛡️ FraudScan AI</h2></div>", unsafe_allow_html=True)
    st.caption("AI-Powered Job Risk Intelligence")
    st.divider()
    
    page = st.selectbox(
        "Navigation",
        ["🔍 Detector Panel", "📊 Analytics Console", "⚙️ System Status"],
        label_visibility="collapsed"
    )
    
    st.divider()
    
    st.markdown("<span style='font-size:0.75rem; text-transform:uppercase; letter-spacing:0.5px; color:#64748B; font-weight:700;'>Telemetry Monitor</span>", unsafe_allow_html=True)
    if is_api_online:
        st.markdown("● **API Status:** :green[Active 🟢]")
        if api_health and api_health.get("database_logging"):
            st.markdown("● **History Logger:** :green[Connected 🟢]")
        else:
            st.markdown("● **History Logger:** :orange[Disabled 🟡]")
    else:
        st.markdown("● **API Status:** :red[Unreachable 🔴]")
        st.caption("Start FastAPI backend (uvicorn main:app) to connect.")
    
    st.divider()
    st.markdown("<span style='font-size:0.75rem; text-transform:uppercase; letter-spacing:0.5px; color:#64748B; font-weight:700;'>Core Engine Specs</span>", unsafe_allow_html=True)
    st.write("🌲 Random Forest Classifier")
    st.write("⚡ FastAPI Endpoint Handler")
    st.write("📊 TF-IDF 15k-feature Model")
    st.write("🛡️ Risk Rule Engine")

# ---- DETECTOR PANEL PAGE ----
if page == "🔍 Detector Panel":
    DEFAULTS = {
        "job_text": "",
        "scan_result": None,
        "history": []
    }

    for k, v in DEFAULTS.items():
        st.session_state.setdefault(k, v)
    
    # Hero / Header
    st.markdown("""
    <div class="hero-wrapper" role="banner">
        <div style="display:inline-flex; align-items:center; gap:8px; background:rgba(124, 92, 255, 0.1); border:1px solid rgba(124, 92, 255, 0.25); color:#C084FC; padding:4px 12px; border-radius:20px; font-size:0.8rem; font-weight:700; text-transform:uppercase; letter-spacing:1px; margin-bottom:15px;">
            ✨ Intelligence Engine Active
        </div>
        <h1 class="hero-title">Automated Job Scam Detection</h1>
        <h2 class="hero-subtitle">Verify job postings instantly using Random Forest ML + Rule Heuristics</h2>
        <p class="hero-desc">Protect your candidates and clean your job boards. Paste any job posting description or drag in a text log file to perform a structural risk audit instantly.</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("###")

    # Statistics row styled like a dashboard
    m_col1, m_col2, m_col3, m_col4 = st.columns(4)
    with m_col1:
        st.markdown("""
        <div class="dashboard-stat-card" role="region" aria-label="Training corpus statistic">
            <div class="dashboard-stat-val">17,880</div>
            <div class="dashboard-stat-label">Training Corpus</div>
        </div>
        """, unsafe_allow_html=True)
    with m_col2:
        st.markdown("""
        <div class="dashboard-stat-card" role="region" aria-label="Model accuracy statistic">
            <div class="dashboard-stat-val">98.41%</div>
            <div class="dashboard-stat-label">Model Accuracy</div>
        </div>
        """, unsafe_allow_html=True)
    with m_col3:
        st.markdown("""
        <div class="dashboard-stat-card" role="region" aria-label="Response latency statistic">
            <div class="dashboard-stat-val">&lt; 150ms</div>
            <div class="dashboard-stat-label">Average Latency</div>
        </div>
        """, unsafe_allow_html=True)
    with m_col4:
        st.markdown("""
        <div class="dashboard-stat-card" role="region" aria-label="Audit explainability statistic">
            <div class="dashboard-stat-val">Real-time</div>
            <div class="dashboard-stat-label">Explainable Verdict</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("###")

    # Main Interactive Card Row
    col_input, col_info = st.columns([1.3, 1], gap="large")

    with col_input:
        with st.container(border=True):
            st.markdown('<div class="saas-card-header" role="heading" aria-level="3">📊 Scan Console</div>', unsafe_allow_html=True)
            
            # Interactive Quick Trial templates
            st.markdown("<span style='font-size:0.85rem; font-weight:600; color:#64748B;'>Select a template to pre-fill instantly:</span>", unsafe_allow_html=True)
            t_col1, t_col2 = st.columns(2)
            with t_col1:
                if st.button("✅ Template: Legitimate Tech Role", use_container_width=True, key="template_real"):
                    st.session_state.job_text = (
                        "We are seeking a Senior Software Engineer to join our growing engineering team. "
                        "In this role, you will design, build, and maintain robust APIs using Python, FastAPI, and PostgreSQL. "
                        "Responsibilities:\n- Design scalable backend services\n- Write unit tests and maintain high code coverage\n- Participate in design reviews\n\n"
                        "Requirements:\n- 5+ years of software development experience\n- Strong proficiency in Python or Go\n- Experience with Docker, Kubernetes, and AWS.\n\n"
                        "We offer competitive salary, equity options, comprehensive healthcare, and flexible remote work arrangements. Apply directly via our company careers portal."
                    )
                    st.rerun()
            with t_col2:
                if st.button("🚨 Template: High-Risk Assistant", use_container_width=True, key="template_fake"):
                    st.session_state.job_text = (
                        "URGENTLY HIRING! Easy work from home opportunity for part-time online assistants. "
                        "No experience is required, we provide full onboarding training! "
                        "Earn up to $1,500 per week guaranteed. Flexible hours, choose your own shift. "
                        "You will handle simple documents, email correspondence, and routing details. "
                        "Requirements: must have a laptop and active internet connection.\n\n"
                        "Note: A minor onboarding processing fee of $50 is required to secure the slot and pay for training materials, fully refundable after your first week. "
                        "WhatsApp us directly at +1 (987) 654-3210 immediately to apply! Only limited seats remaining, join today!"
                    )
                    st.rerun()
            
            st.markdown("<div style='margin: 15px 0 10px 0; border-top:1px solid rgba(255,255,255,0.06); padding-top:15px;'></div>", unsafe_allow_html=True)
            
            # File uploader
            st.markdown("<span style='font-size:0.85rem; font-weight:600; color:#64748B;'>Or upload a job advertisement file (.txt):</span>", unsafe_allow_html=True)
            uploaded_file = st.file_uploader("Upload job posting", type=["txt", "md"], label_visibility="collapsed", key="file_loader")
            if uploaded_file is not None:
                try:
                    uploaded_text = uploaded_file.read().decode("utf-8")
                    if uploaded_text:
                        st.session_state.job_text = uploaded_text
                except Exception as e:
                    st.error(f"Error loading file: {e}")
            
            st.markdown("<div style='margin-bottom:12px;'></div>", unsafe_allow_html=True)
            
            # Job description text area
            job_text = st.text_area(
                "Job Advertisement Text",
                value=st.session_state.job_text,
                placeholder="Paste the job advertisement text here...",
                height=300,
                label_visibility="collapsed",
                key="job_text_input"
            )
            st.session_state.job_text = job_text
            
            # Statistics
            job_text = job_text or ""
            chars = len(job_text)
            words = len(job_text.split())
            
            c_p1, c_p2 = st.columns([2, 1])
            with c_p1:
                if chars == 0:
                    st.info("💡 Paste text or click a template to start.")
                    is_valid = False
                elif chars < 20:
                    st.error(f"⚠️ Minimum required length is 20 characters (current: {chars}).")
                    is_valid = False
                elif chars > 10000:
                    st.error(f"🚨 Maximum character limit is 10,000 (current: {chars}).")
                    is_valid = False
                else:
                    is_valid = True
                    if chars < 150:
                        st.warning("ℹ️ Text is short; results are more reliable with complete details.")
                    elif chars < 600:
                        st.info("✅ Moderate text length. Ready for processing.")
                    else:
                        st.success("🌟 Highly detailed posting. Ideal for AI analysis.")
            with c_p2:
                st.markdown(f"<div style='text-align:right; font-size:0.85rem; color:#64748B; margin-top:5px;'><b>{chars:,} / 10,000</b> characters<br><b>{words:,}</b> words</div>", unsafe_allow_html=True)
                
            progress_val = min(1.0, chars / 10000)
            st.progress(progress_val)
            
            # Control buttons
            b_col1, b_col2 = st.columns([3, 1])
            with b_col1:
                analyze = st.button("🔍 Run Forensic Scan", use_container_width=True, type="primary", disabled=not is_valid, key="analyze_button")
            with b_col2:
                reset = st.button("↺ Clear", use_container_width=True, key="reset_button")
                if reset:
                    st.session_state.job_text = ""
                    st.rerun()

    with col_info:
        with st.container(border=True):
            st.markdown('<div class="saas-card-header" role="heading" aria-level="3">🧠 How It Works</div>', unsafe_allow_html=True)
            st.markdown("""
            FraudScan AI evaluates postings through a multi-layered detection pipeline:
            
            1. **NLP Text Preprocessing**: Text is converted to lowercase, cleaned of HTML layout structures, and stripped of punctuation.
            2. **Random Forest Inference**: Uses a pre-trained ensemble classifier with a TF-IDF vectorizer trained on 17,880 rows.
            3. **Rule Matcher Constraint Audit**: Evaluates the text against a structured keyword risk database.
            4. **Frontend Pattern Matcher**: Highlight heuristic patterns directly on the client side.
            """)
            
            st.markdown("<span style='font-size:0.8rem; text-transform:uppercase; letter-spacing:0.5px; color:#64748B; font-weight:700;'>Detection Pipeline Indicators</span>", unsafe_allow_html=True)
            st.success("✔ TF-IDF Text Vectorization Pipeline (15,000 Max Features)")
            st.success("✔ Random Forest Model Inference (200 Trees)")
            st.success("✔ Rules-based Categorical Risk Assessor")
            st.success("✔ Heuristic Signals Keyword Highlighter")

    # --- Connection Offline Alert Portal ---
    if not is_api_online:
        st.markdown("###")
        with st.container(border=True):
            st.markdown("<div class='saas-card-header' style='border-color:rgba(239,68,68,0.25); color:#EF4444;'>🔴 Connection Paused — API Offline</div>", unsafe_allow_html=True)
            st.warning("⚠️ **Diagnostics Notice:** The visual frontend cannot verify text or execute live scans because the FastAPI engine is unreachable.")
            st.markdown("""
            ### How to Start the Engine:
            Run the following command in your terminal workspace to restore live connection telemetry:
            ```bash
            python3 -m uvicorn main:app --host 127.0.0.1 --port 8000 --reload
            ```
            """, unsafe_allow_html=True) # <--- ADD THIS LINE
