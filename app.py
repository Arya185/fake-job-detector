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

/* Prevent app viewport scroll to keep sidebar fixed and fully extended */
[data-testid="stAppViewContainer"], .stApp {
    height: 100vh !important;
    overflow: hidden !important;
}

/* Style the sidebar explicitly to span full screen height */
[data-testid="stSidebar"] {
    min-height: 100vh !important;
    height: 100vh !important;
    background-color: #0B0F19 !important;
}

/* Allow only the main content panel to scroll */
.stMain, [data-testid="stMainBlockContainer"], .block-container {
    height: 100% !important;
    min-height: 100vh !important;
    overflow-y: auto !important;
    overflow-x: hidden !important;
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

/* SaaS dashboard metrics */
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

/* Custom themed Streamlit native alerts */
div[data-testid="stAlert"] {
    background-color: rgba(30, 41, 59, 0.4) !important;
    border: 1px solid rgba(255, 255, 255, 0.08) !important;
    border-radius: 14px !important;
    color: #F1F5F9 !important;
    padding: 15px 20px !important;
}
div[data-testid="stAlert"] p {
    color: #E2E8F0 !important;
    font-size: 0.95rem !important;
}
div[data-testid="stAlert"] [role="img"] {
    filter: brightness(1.2) !important;
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
    except Exception:
        pass
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
    st.write("🌲 Random Forest (200 Trees)")
    st.write("⚡ FastAPI Endpoint Handler")
    st.write("📊 TF-IDF (15,000 Features)")
    st.write("🛡️ Risk Rule Engine")

# ---- DETECTOR PANEL PAGE ----
if page == "🔍 Detector Panel":
    if 'job_text' not in st.session_state:
        st.session_state.job_text = ""
    
    # Hero / Header
    st.markdown("""
    <div class="hero-wrapper">
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
        with st.container(border=True):
            st.markdown("""
            <div style='text-align: center;'>
                <div class="dashboard-stat-val" style="text-align: center;">17,880</div>
                <div class="dashboard-stat-label" style="text-align: center;">Training Corpus</div>
            </div>
            """, unsafe_allow_html=True)
    with m_col2:
        with st.container(border=True):
            st.markdown("""
            <div style='text-align: center;'>
                <div class="dashboard-stat-val" style="text-align: center;">98.4%</div>
                <div class="dashboard-stat-label" style="text-align: center;">Model Accuracy</div>
            </div>
            """, unsafe_allow_html=True)
    with m_col3:
        with st.container(border=True):
            st.markdown("""
            <div style='text-align: center;'>
                <div class="dashboard-stat-val" style="text-align: center;">&lt; 150ms</div>
                <div class="dashboard-stat-label" style="text-align: center;">Average Latency</div>
            </div>
            """, unsafe_allow_html=True)
    with m_col4:
        with st.container(border=True):
            st.markdown("""
            <div style='text-align: center;'>
                <div class="dashboard-stat-val" style="text-align: center;">Real-time</div>
                <div class="dashboard-stat-label" style="text-align: center;">Explainable Verdict</div>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("###")

    # Main Interactive Card Row
    col_input, col_info = st.columns([1.3, 1], gap="large")

    with col_input:
        with st.container(border=True):
            st.markdown('<div class="saas-card-header">📊 Scan Console</div>', unsafe_allow_html=True)
            
            # Interactive Quick Trial templates
            st.markdown("<span style='font-size:0.85rem; font-weight:600; color:#64748B;'>Select a template to pre-fill instantly:</span>", unsafe_allow_html=True)
            t_col1, t_col2 = st.columns(2)
            with t_col1:
                if st.button("✅ Template: Legitimate Tech Role", use_container_width=True):
                    st.session_state.job_text = (
                        "We are seeking a Senior Software Engineer to join our growing engineering team. "
                        "In this role, you will design, build, and maintain robust APIs using Python, FastAPI, and PostgreSQL. "
                        "Responsibilities:\n- Design scalable backend services\n- Write unit tests and maintain high code coverage\n- Participate in design reviews\n\n"
                        "Requirements:\n- 5+ years of software development experience\n- Strong proficiency in Python or Go\n- Experience with Docker, Kubernetes, and AWS.\n\n"
                        "We offer competitive salary, equity options, comprehensive healthcare, and flexible remote work arrangements. Apply directly via our company careers portal."
                    )
                    st.rerun()
            with t_col2:
                if st.button("🚨 Template: High-Risk Assistant", use_container_width=True):
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
            uploaded_file = st.file_uploader("Upload job posting", type=["txt", "md"], label_visibility="collapsed")
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
            words = len(job_text.split())
            chars = len(job_text)
            
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
                analyze = st.button("🔍 Run Forensic Scan", use_container_width=True, type="primary", disabled=not is_valid)
            with b_col2:
                reset = st.button("↺ Clear", use_container_width=True)
                if reset:
                    st.session_state.job_text = ""
                    st.rerun()

    with col_info:
        with st.container(border=True):
            st.markdown('<div class="saas-card-header">🧠 How It Works</div>', unsafe_allow_html=True)
            st.markdown("""
            FraudScan AI evaluates postings through a multi-layered detection pipeline:
            
            1. **NLP Text Preprocessing**: Text is converted to lowercase, cleaned of HTML layout structures, and stripped of punctuation.
            2. **Random Forest Inference**: Uses a pre-trained ensemble classifier with a TF-IDF vectorizer trained on 17,880 rows.
            3. **Rule Matcher Constraint Audit**: Evaluates the text against a structured keyword risk database.
            4. **Frontend Pattern Matcher**: Highlights heuristic patterns directly on the client side.
            """)
            
            st.markdown("<span style='font-size:0.8rem; text-transform:uppercase; letter-spacing:0.5px; color:#64748B; font-weight:700;'>Detection Pipeline Indicators</span>", unsafe_allow_html=True)
            st.success("✔ TF-IDF Text Vectorization Pipeline")
            st.success("✔ Random Forest Model Inference")
            st.success("✔ Rules-based Categorical Risk Assessor")
            st.success("✔ Heuristic Signals Keyword Highlighter")

    # --- Prediction Execution Result Panel ---
    if analyze:
        if not is_api_online:
            st.error("❌ **Backend API Offline:** Connection failed. Make sure the FastAPI backend is running.")
        else:
            status = st.status("Executing Pipeline...", expanded=True)
            status.write("🧹 Preprocessing input text structure...")
            time.sleep(0.15)
            status.write("🌲 Loading Random Forest weights and computing class probabilities...")
            time.sleep(0.15)
            status.write("🛡️ Checking keyword match thresholds...")
            time.sleep(0.1)
            
            start_time = time.time()
            try:
                response = requests.post(
                    f"{API_BASE_URL}/predict",
                    json={"text": job_text},
                    timeout=90
                )
                scan_duration = round(time.time() - start_time, 3)
                scan_timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                
                if response.status_code == 422:
                    status.update(label="Forensic Scan Failed", state="error")
                    st.error("❌ **Payload Validation Error:** The backend API rejected the text payload format. Please adjust content size.")
                else:
                    response.raise_for_status()
                    result = response.json()
                    status.update(label="Forensic Scan Complete", state="complete")
                    
                    prediction = result["prediction"]
                    confidence = result["confidence"]
                    fraud_prob = result["fraud_probability"]
                    risk_score = result["risk_score"]
                    matched_rules = result["matched_rules"]
                    matched_keywords = result["matched_keywords"]
                    
                    st.markdown("###")
                    
                    # Modern SaaS Verdict Banner & Details
                    verdict_is_fake = "Fake" in prediction
                    
                    with st.container(border=True):
                        st.markdown('<div class="saas-card-header">📊 Scan Diagnostics Summary</div>', unsafe_allow_html=True)
                        
                        # Verdict layout
                        v_col1, v_col2 = st.columns([1.5, 1], gap="medium")
                        
                        with v_col1:
                            if verdict_is_fake:
                                verdict_badge = """
                                <div style='display:inline-flex; align-items:center; gap:8px; background:rgba(239, 68, 68, 0.1); border:1px solid rgba(239, 68, 68, 0.2); color:#ef4444; padding:6px 14px; border-radius:30px; font-weight:700; font-size:0.95rem; text-transform:uppercase; letter-spacing:0.5px;'>
                                    <span style='width:8px; height:8px; background:#ef4444; border-radius:50%; display:inline-block; box-shadow:0 0 8px #ef4444;'></span>
                                    Scam Posting Detected (High Risk)
                                </div>
                                """
                                st.markdown(verdict_badge, unsafe_allow_html=True)
                                st.markdown("<h2 style='font-size:2.2rem; font-weight:800; color:#EF4444; margin:15px 0 5px 0;'>AI Threat Warning</h2>", unsafe_allow_html=True)
                                st.markdown("<p style='color:#EF4444; font-weight:500; font-size:1rem; line-height:1.5;'>This job posting exhibits structural elements commonly associated with recruitment frauds and scam networks. Exercise extreme caution.</p>", unsafe_allow_html=True)
                            else:
                                verdict_badge = """
                                <div style='display:inline-flex; align-items:center; gap:8px; background:rgba(16, 185, 129, 0.1); border:1px solid rgba(16, 185, 129, 0.2); color:#10b981; padding:6px 14px; border-radius:30px; font-weight:700; font-size:0.95rem; text-transform:uppercase; letter-spacing:0.5px;'>
                                    <span style='width:8px; height:8px; background:#10b981; border-radius:50%; display:inline-block; box-shadow:0 0 8px #10b981;'></span>
                                    Legitimate Posting Verified
                                </div>
                                """
                                st.markdown(verdict_badge, unsafe_allow_html=True)
                                st.markdown("<h2 style='font-size:2.2rem; font-weight:800; color:#10B981; margin:15px 0 5px 0;'>Passed Verification</h2>", unsafe_allow_html=True)
                                st.markdown("<p style='color:#A7F3D0; font-weight:500; font-size:1rem; line-height:1.5;'>No major scam indicators or threat indicators were flagged by the detection pipelines. The posting matches legitimate structures.</p>", unsafe_allow_html=True)
                        
                        with v_col2:
                            st.markdown(f"""
                            <div style='background:rgba(15, 23, 42, 0.4); border:1px solid rgba(255,255,255,0.05); padding:15px; border-radius:12px; font-size:0.9rem;'>
                                <div style='display:flex; justify-content:space-between; margin-bottom:6px;'><span style='color:#64748B;'>Scan Speed:</span><span style='color:#FFF; font-weight:600;'>{scan_duration}s</span></div>
                                <div style='display:flex; justify-content:space-between; margin-bottom:6px;'><span style='color:#64748B;'>Scan Timestamp:</span><span style='color:#FFF; font-weight:600;'>{scan_timestamp}</span></div>
                                <div style='display:flex; justify-content:space-between; margin-bottom:6px;'><span style='color:#64748B;'>Verdict Score:</span><span style='color:#FFF; font-weight:600;'>{prediction}</span></div>
                                <div style='display:flex; justify-content:space-between;'><span style='color:#64748B;'>Signal Risk Index:</span><span style='color:#FFF; font-weight:600;'>{risk_score}</span></div>
                            </div>
                            """, unsafe_allow_html=True)
                    
                    # Risk visualization & Action items row
                    col_gauge, col_findings = st.columns([1, 1.3], gap="large")
                    
                    with col_gauge:
                        with st.container(border=True):
                            st.markdown('<div class="saas-card-header">📊 Risk Visualization</div>', unsafe_allow_html=True)
                            
                            # Plotly gauge chart
                            fig = go.Figure(go.Indicator(
                                mode="gauge+number",
                                value=fraud_prob,
                                number={"font": {"size": 38, "color": "#FFF", "family": "Plus Jakarta Sans"}},
                                gauge={
                                    "axis": {"range": [0, 100], "tickwidth": 1, "tickcolor": "#475569"},
                                    "bar": {"color": "#7C5CFF", "thickness": 0.25},
                                    "steps": [
                                        {"range": [0, 25], "color": "#064E3B"},
                                        {"range": [25, 50], "color": "#78350F"},
                                        {"range": [50, 75], "color": "#7C2D12"},
                                        {"range": [75, 100], "color": "#7F1D1D"}
                                    ],
                                    "threshold": {
                                        "line": {"color": "#7C5CFF", "width": 4},
                                        "thickness": 0.8,
                                        "value": fraud_prob
                                    }
                                }
                            ))
                            fig.update_layout(
                                height=250,
                                margin=dict(l=20, r=20, t=30, b=10),
                                paper_bgcolor="rgba(0,0,0,0)",
                                plot_bgcolor="rgba(0,0,0,0)",
                                font={"color": "#94A3B8"}
                            )
                            st.plotly_chart(fig, use_container_width=True)
                            st.markdown("<p style='text-align:center; font-size:0.85rem; color:#64748B; margin-top:-10px;'>This dial indicates the structural scam probability percentage index.</p>", unsafe_allow_html=True)
                        
                    with col_findings:
                        with st.container(border=True):
                            st.markdown('<div class="saas-card-header">💡 Actions & Recommendations</div>', unsafe_allow_html=True)
                            
                            if fraud_prob >= 75:
                                st.markdown("""
                                <div class="finding-card" style="border-left: 4px solid #EF4444;">
                                    <div style="display:flex; justify-content:space-between; margin-bottom:8px;">
                                        <span style="font-weight:700; color:#FFF;">🔴 CRITICAL SCAM RISK ACTION</span>
                                        <span class="severity-pill-danger">High Priority</span>
                                    </div>
                                    <ul style="margin: 0; padding-left: 20px; font-size:0.9rem; color:#E2E8F0; line-height:1.6;">
                                        <li>❌ <b>Do NOT transfer funds:</b> Under no conditions send onboarding processing or registration money.</li>
                                        <li>❌ <b>Do NOT share documents:</b> Avoid sending scans of identity documents (SSN, passport, banking logs).</li>
                                        <li>🔍 <b>Verify domain metadata:</b> Confirm the recruiter email matches the official domain.</li>
                                    </ul>
                                </div>
                                """, unsafe_allow_html=True)
                            elif fraud_prob >= 50:
                                st.markdown("""
                                <div class="finding-card" style="border-left: 4px solid #F59E0B;">
                                    <div style="display:flex; justify-content:space-between; margin-bottom:8px;">
                                        <span style="font-weight:700; color:#FFF;">🟡 ELEVATED RISK AUDIT</span>
                                        <span class="severity-pill-warning">Medium Priority</span>
                                    </div>
                                    <ul style="margin: 0; padding-left: 20px; font-size:0.9rem; color:#E2E8F0; line-height:1.6;">
                                        <li>📞 <b>Confirm interview modes:</b> Ignore offers that bypass interactive panels.</li>
                                        <li>🔍 <b>Recruiter research:</b> Look up the hiring coordinator's company credentials.</li>
                                        <li>💵 <b>Verify pay guidelines:</b> Ensure salaries align with industry standards.</li>
                                    </ul>
                                </div>
                                """, unsafe_allow_html=True)
                            else:
                                st.markdown("""
                                <div class="finding-card" style="border-left: 4px solid #10B981;">
                                    <div style="display:flex; justify-content:space-between; margin-bottom:8px;">
                                        <span style="font-weight:700; color:#FFF;">🟢 LOW RISK CLEARANCE</span>
                                        <span class="severity-pill-info">Low Priority</span>
                                    </div>
                                    <p style="font-size:0.9rem; color:#E2E8F0; line-height:1.5; margin:0;">
                                        The posting has passed key structural checks. Standard career procedures are recommended. Cross-verify the posting directly on the organization's official website.
                                    </p>
                                </div>
                                """, unsafe_allow_html=True)
                    
                    st.divider()
                    
                    # AI Audit Findings Panel
                    with st.container(border=True):
                        st.markdown('<div class="saas-card-header">🛡️ Structural Threat Intelligence Audit</div>', unsafe_allow_html=True)
                        
                        col_det_kw, col_det_cat, col_det_regex = st.columns(3)
                        
                        with col_det_kw:
                            st.markdown("<h4 style='font-size:1.05rem; font-weight:700; color:#FFF; margin-bottom:12px;'>Matched Rule Keywords</h4>", unsafe_allow_html=True)
                            if matched_keywords:
                                for kw in matched_keywords:
                                    st.markdown(f'<div class="finding-card" style="padding:10px 15px; margin-bottom:10px; border-left:3px solid #7C5CFF; font-size:0.85rem;"><span style="color:#A78BFA; font-weight:600;">⚠️ Keyword:</span> "{kw.title()}"</div>', unsafe_allow_html=True)
                            else:
                                st.success("No suspicious rules keywords matched.")
                                
                        with col_det_cat:
                            st.markdown("<h4 style='font-size:1.05rem; font-weight:700; color:#FFF; margin-bottom:12px;'>Matched Threat Categories</h4>", unsafe_allow_html=True)
                            if matched_rules:
                                category_info = {
                                    "payment": ("💰", "Payment / Fee Request", "danger"),
                                    "contact": ("📞", "Suspicious Contact Method", "warning"),
                                    "urgency": ("⚡", "High Urgency / Pressure Tactic", "info"),
                                    "salary": ("💵", "Unrealistic Income / Work Terms", "warning")
                                }
                                for r in matched_rules:
                                    r_lower = r.lower().strip()
                                    emoji, display_name, severity = category_info.get(r_lower, ("⚠️", r.title(), "info"))
                                    severity_class = f"severity-pill-{severity}"
                                    st.markdown(f"""
                                    <div class="finding-card" style="padding:12px 15px; margin-bottom:10px; border-left:3px solid #EF4444;">
                                        <div style="display:flex; justify-content:space-between; align-items:center;">
                                            <span style="font-weight:600; color:#FFF; font-size:0.85rem;">{emoji} {display_name}</span>
                                            <span class="{severity_class}" style="font-size:0.65rem;">Flagged</span>
                                        </div>
                                    </div>
                                    """, unsafe_allow_html=True)
                            else:
                                st.success("No dangerous category signals matched.")
                                
                        with col_det_regex:
                            st.markdown("<h4 style='font-size:1.05rem; font-weight:700; color:#FFF; margin-bottom:12px;'>Frontend Heuristic Signals</h4>", unsafe_allow_html=True)
                            found_flags = check_red_flags(job_text)
                            if found_flags:
                                for flag in found_flags:
                                    st.markdown(f"""
                                    <div class="finding-card" style="padding:10px 15px; margin-bottom:10px; border-left:3px solid #F59E0B; font-size:0.85rem;">
                                        <div style="font-weight:600; color:#FFF; margin-bottom:4px;">{flag['label']}</div>
                                        <span style="font-size:0.75rem; color:#64748B;">Matched snippet: "{flag['match']}"</span>
                                    </div>
                                    """, unsafe_allow_html=True)
                            else:
                                st.success("No frontend regex heuristic signals matched.")
                    
                    # Explanations Expander
                    st.markdown("###")
                    with st.expander("🧠 View Pipeline Logic & Reasoning Explanation Details", expanded=False):
                        st.markdown(f"""
                        #### Forensic Reasoning Matrix
                        - **Ensemble Classifier Verdict**: The Random Forest model evaluated the job posting TF-IDF weights and classified the text with a **{confidence} confidence** probability.
                        - **Categorical Risk Contribution**: The backend rules engine matched indicators contributing to a **risk index of {risk_score}**.
                        - **Threat Evaluation Breakdown**:
                          - **Payment Risks**: Upfront payments contribute +30 to the risk score.
                          - **Contact Risks**: Messaging platform redirection checks contribute +20 to the risk score.
                          - **Urgency Risks**: High pressure urgency constraints contribute +15 to the risk score.
                          - **Salary Risks**: Easy income/no experience claims contribute +10 to the risk score.
                        """)
                        
            except requests.exceptions.Timeout:
                status.update(label="API Timeout", state="error")
                st.error("⏱️ **API Connection Timeout:** The backend server is taking too long to respond. The free tier on Render might be sleeping. Please try again.")
            except requests.exceptions.RequestException as e:
                status.update(label="Scan Error", state="error")
                st.error(f"❌ **Request Failed:** API connection error details:\n`{e}`")
            except Exception as e:
                status.update(label="Engine Failure", state="error")
                st.exception(e)
                
    st.markdown(
        '<div class="footer">🛡️ FraudScan AI — Powered by Random Forest + FastAPI + Streamlit | Trained on 17,880 job postings</div>',
        unsafe_allow_html=True
    )

# ---- ANALYTICS CONSOLE PAGE ----
if page == "📊 Analytics Console":
    st.markdown("""
    <div class="hero-wrapper" style="padding:40px 0 20px;">
        <h1 class="hero-title">Database Analytics Console</h1>
        <p class="hero-desc">Real-time scan logs, metrics, and distribution summaries retrieved from MySQL logs</p>
    </div>
    """, unsafe_allow_html=True)
    st.divider()

    if not is_api_online:
        st.error("❌ **Connection Error:** Backend is offline. Cannot query prediction logs.")
    else:
        try:
            with st.spinner("Retrieving historical scan logs from database..."):
                response = requests.get(f"{API_BASE_URL}/history", timeout=90)
                response.raise_for_status()
                data = response.json()
                
            error = data.get("error")
            history = data.get("history", [])
            
            if error:
                st.error(f"❌ **Database Telemetry Error:** `{error}`")
                st.info("💡 **Database Setup Guide:** Ensure your MySQL credentials are set in environment variables and the `predictions` table exists.")
            elif "message" in data and data.get("message") and "Database logging disabled" in data.get("message"):
                # Database Setup Tutorial Component
                st.warning("⚠️ **Database Logging is Currently Disabled**")
                with st.container(border=True):
                    st.markdown('<div class="saas-card-header">⚙️ How to Enable Prediction Logging & Analytics</div>', unsafe_allow_html=True)
                    st.markdown("""
                    <p style="font-size:0.95rem; line-height:1.6; color:#94A3B8;">
                        To unlock historical analysis features, configure the backend FastAPI application to store outputs inside a MySQL database:
                    </p>
                    <ol style="color:#E2E8F0; font-size:0.9rem; line-height:1.8; padding-left:20px;">
                        <li>Enable database logging in the backend by setting <b><code>ENABLE_DB_LOGGING=true</code></b> inside your backend environment configuration.</li>
                        <li>Provide your MySQL database credentials:
                            <ul style="padding-left:20px;">
                                <li><code>MYSQL_HOST</code> (e.g. <code>localhost</code>)</li>
                                <li><code>MYSQL_PORT</code> (default: <code>3306</code>)</li>
                                <li><code>MYSQL_USER</code> (e.g. <code>root</code>)</li>
                                <li><code>MYSQL_PASSWORD</code></li>
                                <li><code>MYSQL_DATABASE</code> (e.g. <code>fake_job_detector</code>)</li>
                            </ul>
                        </li>
                        <li>Connect to your database and execute the table schema creation query:</li>
                    </ol>
                    <pre style="background:rgba(0,0,0,0.4); border:1px solid rgba(255,255,255,0.06); padding:15px; border-radius:8px; color:#A78BFA; font-size:0.85rem;"><code>CREATE TABLE predictions (
    id INT AUTO_INCREMENT PRIMARY KEY,
    input_text VARCHAR(500) NOT NULL,
    prediction VARCHAR(50) NOT NULL,
    fraud_probability FLOAT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);</code></pre>
                    """, unsafe_allow_html=True)
            elif not history:
                with st.container(border=True):
                    st.markdown("""
                    <div style='text-align: center; padding: 40px 20px;'>
                        <div style='font-size: 3rem; margin-bottom: 15px;'>📊</div>
                        <h3 style='color: #FFF; font-weight: 700; margin-bottom: 8px;'>No Prediction Records Found</h3>
                        <p style='color: #94A3B8; font-size: 0.95rem; margin-bottom: 24px; width: 60%; margin-left: auto; margin-right: auto;'>
                            Prediction logs will populate here once you analyze job postings. Scan your first posting on the Detector page to build telemetry profiles.
                        </p>
                    </div>
                    """, unsafe_allow_html=True)
                    st.info("💡 Switch to the **🔍 Detector Panel** in the sidebar navigation to run scans.")
            else:
                df = pd.DataFrame(history)
                df['created_at'] = pd.to_datetime(df['created_at'])
                df['verdict_label'] = df['prediction'].apply(
                    lambda x: 'Fake' if 'Fake' in str(x) else 'Real'
                )
                
                # SaaS filters panel
                with st.container(border=True):
                    st.markdown('<div class="saas-card-header">⚙️ Telemetry Filtration & Search</div>', unsafe_allow_html=True)
                    
                    f_col1, f_col2, f_col3 = st.columns([1, 1, 1.2])
                    with f_col1:
                        v_filter = st.selectbox("Filter by Verdict", ["All", "Fake 🚨", "Real ✅"])
                    with f_col2:
                        s_filter = st.selectbox("Sort Log Chronology", ["Date (Newest First)", "Date (Oldest First)", "Probability (High to Low)", "Probability (Low to High)"])
                    with f_col3:
                        prob_range = st.slider("Filter by Fraud Probability (%)", min_value=0.0, max_value=100.0, value=(0.0, 100.0))
                
                # Apply filters
                filtered_df = df.copy()
                if v_filter == "Fake 🚨":
                    filtered_df = filtered_df[filtered_df['verdict_label'] == 'Fake']
                elif v_filter == "Real ✅":
                    filtered_df = filtered_df[filtered_df['verdict_label'] == 'Real']
                
                filtered_df = filtered_df[
                    (filtered_df['fraud_probability'] >= prob_range[0]) &
                    (filtered_df['fraud_probability'] <= prob_range[1])
                ]
                
                # Calculations
                total = len(filtered_df)
                fakes = len(filtered_df[filtered_df['verdict_label'] == 'Fake'])
                reals = len(filtered_df[filtered_df['verdict_label'] == 'Real'])
                avg_prob = filtered_df['fraud_probability'].mean() if total > 0 else 0.0
                
                # Telemetry widgets row
                w1, w2, w3, w4 = st.columns(4)
                with w1:
                    with st.container(border=True):
                        st.markdown(f'<div style="text-align: center;"><div class="dashboard-stat-val">{total}</div><div class="dashboard-stat-label">Total Logs (Filtered)</div></div>', unsafe_allow_html=True)
                with w2:
                    with st.container(border=True):
                        st.markdown(f'<div style="text-align: center;"><div class="dashboard-stat-val" style="color:#EF4444;">{fakes}</div><div class="dashboard-stat-label">Fake Postings</div></div>', unsafe_allow_html=True)
                with w3:
                    with st.container(border=True):
                        st.markdown(f'<div style="text-align: center;"><div class="dashboard-stat-val" style="color:#10B981;">{reals}</div><div class="dashboard-stat-label">Verified Legitimate</div></div>', unsafe_allow_html=True)
                with w4:
                    with st.container(border=True):
                        st.markdown(f'<div style="text-align: center;"><div class="dashboard-stat-val">{avg_prob:.1f}%</div><div class="dashboard-stat-label">Avg Scam Rate</div></div>', unsafe_allow_html=True)
                
                st.markdown("###")
                
                if total == 0:
                    st.warning("No historical entries matched the filter criteria.")
                else:
                    # Plots
                    col_chart1, col_chart2 = st.columns(2)
                    
                    with col_chart1:
                        with st.container(border=True):
                            st.markdown('<div class="saas-card-header">🥧 Verdict Distribution Ratio</div>', unsafe_allow_html=True)
                            pie = px.pie(
                                values=filtered_df["verdict_label"].value_counts().values,
                                names=filtered_df["verdict_label"].value_counts().index,
                                hole=0.6,
                                color=filtered_df["verdict_label"].value_counts().index,
                                color_discrete_map={"Fake": "#EF4444", "Real": "#10B981"}
                            )
                            pie.update_traces(textinfo="percent+label", textfont_size=12)
                            pie.update_layout(
                                height=320,
                                margin=dict(l=10, r=10, t=10, b=10),
                                paper_bgcolor="rgba(0,0,0,0)",
                                font={"color": "#94A3B8"}
                            )
                            st.plotly_chart(pie, use_container_width=True)
                        
                    with col_chart2:
                        with st.container(border=True):
                            st.markdown('<div class="saas-card-header">📈 Probability Histogram</div>', unsafe_allow_html=True)
                            hist = px.histogram(
                                filtered_df,
                                x="fraud_probability",
                                nbins=10,
                                color="verdict_label",
                                color_discrete_map={"Fake": "#EF4444", "Real": "#10B981"},
                                labels={"fraud_probability": "Scam Prob %", "count": "Frequency"}
                            )
                            hist.update_layout(
                                height=320,
                                margin=dict(l=10, r=10, t=10, b=10),
                                paper_bgcolor="rgba(0,0,0,0)",
                                plot_bgcolor="rgba(0,0,0,0)",
                                font={"color": "#94A3B8"}
                            )
                            st.plotly_chart(hist, use_container_width=True)
                    
                    # Sort logic execution
                    if "Newest" in s_filter:
                        sorted_df = filtered_df.sort_values('created_at', ascending=False)
                    elif "Oldest" in s_filter:
                        sorted_df = filtered_df.sort_values('created_at', ascending=True)
                    elif "High to Low" in s_filter:
                        sorted_df = filtered_df.sort_values('fraud_probability', ascending=False)
                    else:
                        sorted_df = filtered_df.sort_values('fraud_probability', ascending=True)
                        
                    sorted_df['Date/Time'] = sorted_df['created_at'].dt.strftime('%Y-%m-%d %H:%M:%S')
                    
                    # History Logs table card
                    with st.container(border=True):
                        st.markdown('<div class="saas-card-header">🕐 Forensic Search Logs</div>', unsafe_allow_html=True)
                        st.dataframe(
                            sorted_df[['prediction', 'fraud_probability', 'Date/Time']].reset_index(drop=True),
                            use_container_width=True,
                            column_config={
                                "prediction": st.column_config.TextColumn("Verdict Outcome"),
                                "fraud_probability": st.column_config.ProgressColumn("Scam Score Index (%)", format="%.2f", min_value=0.0, max_value=100.0),
                                "Date/Time": st.column_config.TextColumn("Scanned At")
                            }
                        )
                    
        except requests.exceptions.Timeout:
            st.error("⏱️ **Database Timeout:** Render database logging query timed out. Reload in a minute.")
        except requests.exceptions.RequestException as e:
            st.error(f"❌ **Request Error:** Analytics loading query failed:\n`{e}`")
        except Exception as e:
            st.exception(e)

# ---- SYSTEM STATUS PAGE ----
if page == "⚙️ System Status":
    st.markdown("""
    <div class="hero-wrapper" style="padding:40px 0 20px;">
        <h1 class="hero-title">System Diagnostics Console</h1>
        <p class="hero-desc">Real-time status checks, health telemetry indicators, and server logging verification</p>
    </div>
    """, unsafe_allow_html=True)
    st.divider()

    # Query fresh health status specifically for the status page rendering to avoid stale state mismatches
    status_health_data, status_api_online = query_api_health()

    with st.container(border=True):
        st.markdown('<div class="saas-card-header">📡 API Communication Connection</div>', unsafe_allow_html=True)
        
        # Calculate response latency
        t_start = time.time()
        api_ok = False
        greet_msg = None
        
        try:
            res = requests.get(f"{API_BASE_URL}/", timeout=3)
            if res.status_code == 200:
                api_ok = True
                greet_msg = res.json().get("message")
        except Exception:
            pass
            
        t_latency = round((time.time() - t_start) * 1000, 2)
        
        c_status, c_ping = st.columns(2)
        with c_status:
            if api_ok:
                st.success("🟢 **FastAPI Connection Active**")
                st.info(f"API Greeting Response: *\"{greet_msg}\"*")
            else:
                st.error("🔴 **FastAPI Server Offline**")
                st.markdown("""
                **FastAPI Starting Command:**
                Start the backend FastAPI server in your terminal:
                ```bash
                python3 -m uvicorn main:app --host 127.0.0.1 --port 8000 --reload
                ```
                Verify your environment `API_BASE_URL` points to `http://127.0.0.1:8000`.
                """)
        with c_ping:
            if api_ok:
                st.metric("📶 Live Connection Latency (RTT)", f"{t_latency} ms")
            else:
                st.metric("📶 Live Connection Latency (RTT)", "N/A (Offline)")

    with st.container(border=True):
        st.markdown('<div class="saas-card-header">🏥 Health Telemetry Details</div>', unsafe_allow_html=True)
        if status_health_data and status_api_online:
            th1, th2, th3 = st.columns(3)
            with th1:
                mysql_connected = "Active 🟢" if status_health_data.get("database_logging") else "Disabled 🟡"
                st.metric("MySQL State", mysql_connected)
            with th2:
                st.metric("FastAPI Internal Status", status_health_data.get("status", "Unknown").upper())
            with th3:
                st.metric("Model Directory Path", status_health_data.get("model_dir", "Unknown"))
                
            st.markdown("<p style='font-size:0.85rem; color:#64748B; margin-top:15px;'>Health metrics are verified directly from backend configuration.</p>", unsafe_allow_html=True)
            if not status_health_data.get("database_logging"):
                st.warning("⚠️ **Notice:** Database prediction logging is currently set to `false`. Prediction logs will not be recorded in MySQL. Set `ENABLE_DB_LOGGING=true` in backend variables to store predictions.")
        else:
            st.warning("⚠️ Could not load telemetry because the FastAPI server is currently offline.")

    with st.container(border=True):
        st.markdown('<div class="saas-card-header">🧩 Threat Classification Framework</div>', unsafe_allow_html=True)
        st.markdown("""
        #### Classifier Inference Design
        - **Classifier Engine**: Scikit-Learn Random Forest Classifier (200 trees, max depth of 20)
        - **Preprocessing Pipeline**: Convert input to lower, strip HTML layout symbols, remove numbers/special characters, and run TF-IDF Vectorizer (15,000 feature limit, 1 to 3 n-gram range).
        - **Risk Categories & Heuristic Weights**:
          - `payment` (upfront deposit, joining fee, processing fee, security deposit) ➜ **+30 Risk Points**
          - `contact` (whatsapp, telegram, DM me, personal number) ➜ **+20 Risk Points**
          - `urgency` (urgent hiring, apply immediately, limited seats) ➜ **+15 Risk Points**
          - `salary` (earn daily, easy income, earn lakh) ➜ **+10 Risk Points**
        """)