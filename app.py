import streamlit as st
import requests
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import re
import os

API_BASE_URL = os.getenv("API_BASE_URL", "http://127.0.0.1:8000").rstrip("/")

st.set_page_config(
    page_title="FraudScan AI",
    page_icon="🛡️",
    layout="wide"
)

# Premium CSS
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700&display=swap');

* { font-family: 'Inter', sans-serif; }

.hero{
    text-align:center;
    padding:60px 0 30px;
}

.hero h1{
    font-size:58px;
    font-weight:800;
    margin-bottom:10px;
    background:linear-gradient(
        90deg,
        #7C5CFF,
        #A855F7
    );
    -webkit-background-clip:text;
    -webkit-text-fill-color:transparent;
}

.hero h2{
    font-size:34px;
    font-weight:700;
    color:white;
    line-height:1.3;
    margin-bottom:20px;
}

.hero p{
    width:70%;
    margin:auto;
    font-size:18px;
    color:#94A3B8;
    line-height:1.8;
}

.result-fake {
    background: linear-gradient(135deg, #ff416c, #ff4b2b);
    color: white;
    padding: 1.5rem 2rem;
    border-radius: 16px;
    text-align: center;
    font-size: 1.8rem;
    font-weight: 700;
    margin: 1rem 0;
    box-shadow: 0 8px 32px rgba(255, 65, 108, 0.3);
}
.result-real {
    background: linear-gradient(135deg, #11998e, #38ef7d);
    color: white;
    padding: 1.5rem 2rem;
    border-radius: 16px;
    text-align: center;
    font-size: 1.8rem;
    font-weight: 700;
    margin: 1rem 0;
    box-shadow: 0 8px 32px rgba(17, 153, 142, 0.3);
}
.metric-card{
    background:#1E293B;
    border:1px solid #334155;
    border-radius:18px;
    padding:28px;
    text-align:center;
    transition:0.25s;
}
.metric-card:hover{
    transform:translateY(-6px);
    border-color:#7C5CFF;
}
.metric-value{
    font-size:34px;
    font-weight:800;
    color:white;
}
.metric-label{
    color:#94A3B8;
    margin-top:8px;
}
.flag-item {
    background: rgba(255, 65, 108, 0.1);
    border-left: 3px solid #ff416c;
    padding: 0.5rem 1rem;
    border-radius: 0 8px 8px 0;
    margin: 0.3rem 0;
    color: #ff8fa3;
    font-size: 0.9rem;
}
.safe-item {
    background: rgba(17, 153, 142, 0.1);
    border-left: 3px solid #11998e;
    padding: 0.8rem 1rem;
    border-radius: 0 8px 8px 0;
    color: #38ef7d;
}
.input-card {
    background: #1E293B;
    border: 1px solid #334155;
    border-radius: 18px;
    padding: 25px;
    margin-bottom: 20px;
}
.trust-badge {
    background: #0F172A;
    border: 1px solid #334155;
    border-radius: 12px;
    padding: 12px 8px;
    text-align: center;
    font-size: 0.9rem;
    font-weight: 500;
    color: #E2E8F0;
    transition: 0.2s;
}
.trust-badge:hover {
    border-color: #7C5CFF;
    transform: translateY(-2px);
}
/* Hide the text area label completely */
.stTextArea label {
    display: none !important;
}
.footer {
    text-align: center;
    color: #444;
    font-size: 0.8rem;
    padding: 2rem 0 1rem 0;
}
</style>
""", unsafe_allow_html=True)

# Regex-based red flag patterns
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

# ---- SIDEBAR ----
with st.sidebar:
    st.markdown("# 🛡 FraudScan AI")
    st.caption("AI Fraud Detection Platform")
    st.divider()
    
    page = st.selectbox(
        "Navigate",
        ["🔍 Detector", "📊 Analytics Dashboard"]
    )
    
    st.divider()
    
    st.markdown("### System")
    st.write("🌲 Random Forest")
    st.write("⚡ FastAPI")
    st.write("📊 TF-IDF")
    st.write("🛡 Rule Engine")
    
    st.divider()
    st.caption("Version 1.0")

# ---- DETECTOR PAGE ----
if page == "🔍 Detector":
    # Initialize session state for job text
    if 'job_text' not in st.session_state:
        st.session_state.job_text = ""
    
    st.markdown("""
    <div class="hero">

    <h1>🛡 FraudScan AI</h1>

    <h2>
    Analyze Job Postings using<br>
    Machine Learning + Rule Engine
    </h2>

    <p>
    Detect fraudulent job advertisements in seconds using an AI model,
    keyword-based fraud detection, and explainable risk analysis.
    </p>

    </div>
    """, unsafe_allow_html=True)

    st.markdown("###")

    c1, c2, c3, c4 = st.columns(4)

    with c1:
        st.markdown("""
        <div class="metric-card">
            <div class="metric-value">17K+</div>
            <div class="metric-label">
            Training Samples
            </div>
        </div>
        """, unsafe_allow_html=True)

    with c2:
        st.markdown("""
        <div class="metric-card">
            <div class="metric-value">98%</div>
            <div class="metric-label">
            Accuracy
            </div>
        </div>
        """, unsafe_allow_html=True)

    with c3:
        st.markdown("""
        <div class="metric-card">
            <div class="metric-value">&lt;1s</div>
            <div class="metric-label">
            Avg Response
            </div>
        </div>
        """, unsafe_allow_html=True)

    with c4:
        st.markdown("""
        <div class="metric-card">
            <div class="metric-value">24/7</div>
            <div class="metric-label">
            AI Detection
            </div>
        </div>
        """, unsafe_allow_html=True)

    # Trust Badges
    
    st.markdown("###")

    c1,c2,c3,c4,c5 = st.columns(5)

    for col, text in zip(
        [c1,c2,c3,c4,c5],
        [
            "🌲 Random Forest",
            "🧠 Explainable AI",
            "🛡 Rule Engine",
            "⚡ FastAPI",
            "📊 17K Dataset"
        ]
    ):
        with col:
            st.markdown(
                f"""
                <div class="trust-badge">
                    {text}
                </div>
                """,
                unsafe_allow_html=True
            )

    st.divider()

    col_left, col_right = st.columns([1.2, 1], gap="large")

    with col_left:
        # Wrap input section in card
        st.markdown('<div class="input-card">', unsafe_allow_html=True)
        
        # Use HTML for the header with better styling
        st.markdown("""
        <div style="display: flex; align-items: center; gap: 8px; margin-bottom: 12px;">
            <span style="font-size: 18px; font-weight: 600; color: #E2E8F0;">📋 Paste Job Description</span>
        </div>
        """, unsafe_allow_html=True)
        
        # Use session state for the text area - label hidden with CSS
        job_text = st.text_area(
            "Job Description",
            value=st.session_state.job_text,
            placeholder="Paste the complete job advertisement here.\n\nExample:\n\n• Job Title\n• Salary\n• Company Description\n• Requirements\n• Benefits\n• Contact Details",
            height=360,
            label_visibility="collapsed",
            key="job_text_input"
        )
        
        # Update session state when text changes
        st.session_state.job_text = job_text
        
        # Live Input Statistics
        words = len(job_text.split())
        chars = len(job_text)
        lines = len(job_text.splitlines())
        
        s1, s2, s3 = st.columns(3)
        
        with s1:
            st.metric("📝 Words", words)
        with s2:
            st.metric("🔤 Characters", chars)
        with s3:
            st.metric("📄 Lines", lines)
        
        # Input Quality Indicator
        if chars == 0:
            st.info("📝 Paste a job description to begin.")
        elif chars < 150:
            st.warning("⚠️ Input is quite short. Results may be less reliable.")
        elif chars < 500:
            st.info("✅ Good amount of information provided.")
        else:
            st.success("🌟 Excellent input quality for analysis.")

        col1, col2 = st.columns([3, 1])
        with col1:
            analyze = st.button("🚀 Start AI Analysis", use_container_width=True, type="primary")
        with col2:
            reset = st.button("↺ Reset", use_container_width=True)

        # Reset logic - clears the text area using session state
        if reset:
            st.session_state.job_text = ""
            st.rerun()
            
        st.markdown('</div>', unsafe_allow_html=True)

    with col_right:
        st.markdown("## 🤖 AI Engine")
        
        st.info("""
### Detection Pipeline

📥 Input Job Posting ➜ 🧹 Text Cleaning ➜ 🌲 Random Forest Classifier ➜ 🛡 Rule Engine ➜ 📈 Fraud Probability ➜ 💡 AI Recommendation

""")
        
        st.markdown("### Technologies")
        
        st.success("✔ Random Forest")
        st.success("✔ TF-IDF Vectorizer")
        st.success("✔ Rule-Based Detection")
        st.success("✔ Explainable AI")

    if analyze:
        if not job_text.strip():
            st.warning("⚠️ Please paste a job description first.")
        else:
            status = st.status("Running AI Analysis...", expanded=True)

            status.write("🧹 Cleaning text")
            status.write("🌲 Running Random Forest")
            status.write("🛡 Applying Rule Engine")
            status.write("📈 Calculating fraud probability")
            status.write("💡 Generating recommendation")

            status.update(
                label="Analysis Complete",
                state="complete"
            )
            try:
                response = requests.post(
                    f"{API_BASE_URL}/predict",
                    json={"text": job_text},
                    timeout=90
                )
                response.raise_for_status()
                result = response.json()
                prediction = result["prediction"]
                confidence = result["confidence"]
                fraud_prob = result["fraud_probability"]

                st.divider()

                if "Fake" in prediction:
                    st.markdown('<div class="result-fake">🚨 FRAUDULENT JOB POSTING DETECTED</div>', unsafe_allow_html=True)
                else:
                    st.markdown('<div class="result-real">✅ THIS JOB APPEARS LEGITIMATE</div>', unsafe_allow_html=True)

                st.markdown("###")
                m1, m2, m3, m4 = st.columns(4)
                with m1:
                    verdict_icon = "⚠️ Fake" if "Fake" in prediction else "✅ Real"
                    st.markdown(f'<div class="metric-card"><div class="metric-label">Verdict</div><div class="metric-value">{verdict_icon}</div></div>', unsafe_allow_html=True)
                with m2:
                    st.markdown(f'<div class="metric-card"><div class="metric-label">Fraud Risk</div><div class="metric-value">{fraud_prob}%</div></div>', unsafe_allow_html=True)
                with m3:
                    st.markdown(f'<div class="metric-card"><div class="metric-label">Confidence</div><div class="metric-value">{confidence}</div></div>', unsafe_allow_html=True)
                with m4:
                    st.markdown(f'<div class="metric-card"><div class="metric-label">Rule Score</div><div class="metric-value">{result["risk_score"]}</div></div>', unsafe_allow_html=True)

                st.markdown("###")
                st.markdown("### 📊 Risk Assessment")

                # Create gauge chart
                fig = go.Figure(go.Indicator(
                    mode="gauge+number",
                    value=fraud_prob,
                    title={"text": "Fraud Risk", "font": {"size": 24}},
                    number={"font": {"size": 40}},
                    gauge={
                        "axis": {"range": [0, 100], "tickwidth": 1, "tickcolor": "#94A3B8"},
                        "bar": {"color": "#7C5CFF"},
                        "steps": [
                            {"range": [0, 25], "color": "#22c55e"},
                            {"range": [25, 50], "color": "#eab308"},
                            {"range": [50, 75], "color": "#f97316"},
                            {"range": [75, 100], "color": "#ef4444"}
                        ],
                        "threshold": {
                            "line": {"color": "red", "width": 4},
                            "thickness": 0.75,
                            "value": fraud_prob
                        }
                    }
                ))

                fig.update_layout(
                    height=250,
                    margin=dict(l=20, r=20, t=50, b=20),
                    paper_bgcolor="rgba(0,0,0,0)",
                    plot_bgcolor="rgba(0,0,0,0)",
                    font={"color": "#E2E8F0"}
                )

                st.plotly_chart(fig, use_container_width=True)

                found_flags = check_red_flags(job_text)
                
                st.markdown("###")
                st.markdown("### 🤖 AI Analysis")
                col1, col2 = st.columns([1, 1])
                
                with col1:
                    st.markdown("#### 🚩 Rule-Based Findings")
                    if result["matched_keywords"]:
                        for keyword in result["matched_keywords"]:
                            st.markdown(
                                f"""
                                <div class="flag-item">
                                    ⚠️ <b>{keyword.title()}</b>
                                </div>
                                """,
                                unsafe_allow_html=True
                            )
                    else:
                        st.success("No suspicious keywords detected.")

                with col2:
                    st.markdown("#### 📂 Risk Categories")
                    if result["matched_rules"]:
                        for rule in result["matched_rules"]:
                            emoji = {
                                "Payment Fee": "💰",
                                "WhatsApp": "📞",
                                "Urgent Hiring": "⚡",
                                "Earn 2 Lakh": "💵"
                            }.get(rule, "⚠️")
                            st.info(f"{emoji} {rule.title()}")
                    else:
                        st.success("No risky categories found.")

                # AI Recommendation section
                st.markdown("###")
                st.markdown("### 🤖 AI Recommendation")
                
                if fraud_prob >= 75:
                    st.error("""
                    ### 🚨 High Scam Probability
                    
                    We strongly recommend:
                    
                    - ❌ Do not pay any registration fee
                    - ❌ Avoid sharing personal documents
                    - ❌ Verify the company website
                    - ❌ Search company reviews
                    - ❌ Apply only through official portals
                    """)
                elif fraud_prob >= 50:
                    st.warning("""
                    ### ⚠ Proceed Carefully
                    
                    - Verify recruiter identity
                    - Cross-check salary claims
                    - Confirm company registration
                    - Never send money before joining
                    """)
                else:
                    st.success("""
                    ### ✅ Appears Relatively Safe
                    
                    No major scam indicators were detected.
                    
                    Still verify:
                    
                    - Company website
                    - Recruiter email
                    - LinkedIn company page
                    - Official job portal
                    """)

            except requests.exceptions.Timeout:
                st.error(
                    "The backend is still waking up on Render's free tier. "
                    "Please wait about a minute and try again."
                )
            except requests.exceptions.RequestException as e:
                st.error(f"API request failed:\n{e}")
            except Exception as e:
                st.exception(e)
    
    st.markdown(
        '<div class="footer">🛡️ FraudScan AI — Powered by Random Forest + FastAPI + Streamlit | Trained on 17,000+ job postings</div>',
        unsafe_allow_html=True
    )

# ---- ANALYTICS DASHBOARD PAGE ----
if page == "📊 Analytics Dashboard":
    st.markdown("""
    <div class="hero">
        <h1>📊 Analytics Dashboard</h1>
        <p>Real-time insights from all analyzed job postings</p>
    </div>
    """, unsafe_allow_html=True)
    st.divider()

    try:
        response = requests.get(f"{API_BASE_URL}/history", timeout=90)
        response.raise_for_status()
        data = response.json()
        history = data.get("history", [])

        if not history:
            st.info(data.get("message", "No predictions yet. Analyze some job postings first!"))
        else:
            df = pd.DataFrame(history)
            df['created_at'] = pd.to_datetime(df['created_at'])
            df['label'] = df['prediction'].apply(
                lambda x: 'Fake' if 'Fake' in x else 'Real'
            )

            total = len(df)
            fake_count = len(df[df['label'] == 'Fake'])
            real_count = len(df[df['label'] == 'Real'])
            avg_fraud = df['fraud_probability'].mean()

            m1, m2, m3, m4 = st.columns(4)
            m1.metric("📋 Total Scans", total)
            m2.metric("🚨 Fake Detected", fake_count)
            m3.metric("✅ Real Postings", real_count)
            m4.metric("📈 Avg Fraud Risk", f"{avg_fraud:.1f}%")

            st.divider()

            col1, col2 = st.columns(2)

            with col1:
                st.markdown("#### 🥧 Fake vs Real Distribution")
            
                pie = px.pie(
                    values=df["label"].value_counts().values,
                    names=df["label"].value_counts().index,
                    hole=0.6,
                    color=df["label"].value_counts().index,
                    color_discrete_map={
                        "Fake": "#ff416c",
                        "Real": "#38ef7d"
                    }
                )
            
                pie.update_traces(
                    textinfo="percent+label",
                    textfont_size=14
                )
            
                pie.update_layout(
                    height=380,
                    margin=dict(l=20, r=20, t=20, b=20),
                    showlegend=True
                )
            
                st.plotly_chart(pie, use_container_width=True)

            with col2:
                st.markdown("#### 📈 Fraud Probability Distribution")
                st.bar_chart(df['fraud_probability'])

            st.markdown("#### 🕐 Recent Predictions")
            st.dataframe(
                df[['prediction', 'fraud_probability', 'created_at']]
                .sort_values('created_at', ascending=False)
                .head(20)
                .reset_index(drop=True),
                use_container_width=True
            )

    except requests.exceptions.Timeout:
        st.error(
            "The backend is still waking up on Render's free tier. "
            "Please wait about a minute and try again."
        )
    except requests.exceptions.RequestException as e:
        st.error(f"API request failed:\n{e}")
    except Exception as e:
        st.exception(e)