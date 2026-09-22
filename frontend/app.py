import requests
import streamlit as st

API_URL = "https://jobguard-ai-backend.onrender.com"

st.set_page_config(
    page_title="JobGuard AI", 
    page_icon="🛡️", 
    layout="wide"
)

st.title("🛡️ JobGuard AI")
st.caption("AI-powered Resume Matching & Scam/Fake Job Detection")

# Fetch available jobs from backend
@st.cache_data(ttl=60)
def fetch_jobs():
    try:
        requests.get(f"{API_URL}/health", timeout=10)
        res = requests.get(f"{API_URL}/api/jobs", timeout=15)
        if res.ok:
            return res.json()
    except Exception:
        pass
    return []

jobs = fetch_jobs()

if not jobs:
    st.warning("⚠️ Backend is starting up or temporarily unavailable. If jobs fail to load, please refresh in a few seconds.")

# Navigation Tabs
tab_matcher, tab_detector = st.tabs(["📄 Resume Matcher", "🚨 Fake Job Detector"])

# ==========================================
# TAB 1: RESUME MATCHER
# ==========================================
with tab_matcher:
    st.header("Resume Matching & Skill Analysis")
    st.write("Upload your resume and select a job position to check match compatibility and potential risk factors.")

    col1, col2 = st.columns(2)
    with col1:
        uploaded = st.file_uploader("Upload Resume", type=["pdf", "docx"], key="matcher_resume")
    with col2:
        if jobs:
            labels = {f"{j['id']}. {j['job_title']} — {j['category']}": j for j in jobs}
            selected = st.selectbox("Select Target Job", list(labels.keys()), key="matcher_job")
            job = labels[selected]
        else:
            job = None
            st.info("No jobs available.")

    if st.button("Analyze Resume & Match", type="primary", use_container_width=True, key="btn_match"):
        if not uploaded or not job:
            st.warning("Please upload a resume and select a job position.")
        else:
            files = {"resume": (uploaded.name, uploaded.getvalue(), uploaded.type)}
            data = {"job_id": str(job["id"])}
            
            with st.spinner("Analyzing resume matching and risk metrics..."):
                try:
                    response = requests.post(f"{API_URL}/api/analyze", files=files, data=data, timeout=120)
                    if response.ok:
                        result = response.json()
                        matching = result.get("matching", {})
                        risk = result.get("scam_risk", {})

                        st.success("Analysis complete!")

                        # Metric Display
                        m_col1, m_col2, m_col3 = st.columns(3)
                        m_col1.metric("Overall Match", f"{matching.get('match_score', 0)}%")
                        m_col2.metric("Semantic Match", f"{matching.get('semantic_score', 0)}%")
                        m_col3.metric("Skill Match", f"{matching.get('skill_score', 0)}%")

                        st.divider()

                        s_col1, s_col2 = st.columns(2)
                        with s_col1:
                            st.subheader("✅ Matching Skills")
                            matching_skills = matching.get("matching_skills", [])
                            if matching_skills:
                                for skill in matching_skills:
                                    st.write(f"- {skill}")
                            else:
                                st.write("No matching skills found.")

                        with s_col2:
                            st.subheader("⚠️ Missing Skills")
                            missing_skills = matching.get("missing_skills", [])
                            if missing_skills:
                                for skill in missing_skills:
                                    st.write(f"- {skill}")
                            else:
                                st.write("No missing skills identified.")

                        st.divider()
                        st.subheader("🛡️ Job Scam Risk Summary")
                        risk_level = risk.get("risk_level", "Unknown")
                        risk_score = risk.get("risk_score", 0)

                        if risk_level.lower() == "low":
                            st.success(f"Risk Level: **{risk_level}** ({risk_score}/100)")
                        elif risk_level.lower() == "medium":
                            st.warning(f"Risk Level: **{risk_level}** ({risk_score}/100)")
                        else:
                            st.error(f"Risk Level: **{risk_level}** ({risk_score}/100)")

                        reasons = risk.get("reasons", [])
                        if reasons:
                            st.write("**Risk Factors Identified:**")
                            for reason in reasons:
                                st.write(f"- 🚩 {reason}")

                    else:
                        st.error(f"Server error: {response.text}")
                except Exception as e:
                    st.error(f"Failed to reach the API server: {e}")

# ==========================================
# TAB 2: FAKE JOB DETECTOR
# ==========================================
with tab_detector:
    st.header("Fake & Scam Job Detector")
    st.write("Detect potential fraud, phishing, or fake job listings by inspecting database listings or raw job text.")

    detector_option = st.radio(
        "Detection Mode",
        ["Inspect Database Job", "Analyze Custom Job Description Text"],
        horizontal=True
    )

    if detector_option == "Inspect Database Job":
        if jobs:
            labels_detector = {f"{j['id']}. {j['job_title']} — {j['category']}": j for j in jobs}
            selected_det = st.selectbox("Select Job to Inspect", list(labels_detector.keys()), key="detector_select")
            det_job = labels_detector[selected_det]

            with st.expander("📄 View Full Job Details", expanded=True):
                st.write(f"**Job Title:** {det_job.get('job_title')}")
                st.write(f"**Category:** {det_job.get('category')}")
                if "company" in det_job:
                    st.write(f"**Company:** {det_job.get('company')}")
                if "description" in det_job:
                    st.write(f"**Description:** {det_job.get('description')}")

            if st.button("Check Job Scam Risk", type="primary", key="btn_detect_existing"):
                # Pass dummy resume payload to query backend risk endpoint
                files = {"resume": ("sample.txt", b"Sample profile", "text/plain")}
                data = {"job_id": str(det_job["id"])}

                with st.spinner("Scanning job posting for scam patterns..."):
                    try:
                        res = requests.post(f"{API_URL}/api/analyze", files=files, data=data, timeout=60)
                        if res.ok:
                            risk = res.json().get("scam_risk", {})
                            risk_level = risk.get("risk_level", "Unknown")
                            risk_score = risk.get("risk_score", 0)

                            st.subheader("Detection Result")
                            if risk_level.lower() == "low":
                                st.success(f"🟢 **Legitimate / Low Risk** (Score: {risk_score}/100)")
                            elif risk_level.lower() == "medium":
                                st.warning(f"🟡 **Moderate Risk** (Score: {risk_score}/100)")
                            else:
                                st.error(f"🔴 **High Scam Risk Detected** (Score: {risk_score}/100)")

                            reasons = risk.get("reasons", [])
                            if reasons:
                                st.markdown("### Risk Analysis & Red Flags:")
                                for reason in reasons:
                                    st.write(f"- 🚩 {reason}")
                        else:
                            st.error(res.text)
                    except Exception as e:
                        st.error(f"Error inspecting job risk: {e}")
        else:
            st.info("No jobs available to select.")

    else:
        st.subheader("Analyze Custom Text / Email Offer")
        custom_text = st.text_area(
            "Paste Job Description, Email, or Offer Message",
            height=200,
            placeholder="Paste text here (e.g., salary details, interview instructions, requirement list)..."
        )

        if st.button("Run Fake Job Scan", type="primary", key="btn_detect_custom"):
            if not custom_text.strip():
                st.warning("Please paste some job text to analyze.")
            else:
                with st.spinner("Scanning text for suspicious indicators..."):
                    # Rapid heuristic check for common scam indicators
                    text_lower = custom_text.lower()
                    red_flags = []

                    scam_triggers = [
                        ("telegram", "Requests communication via unverified messaging app (Telegram)"),
                        ("whatsapp", "Requests communication via unverified messaging app (WhatsApp)"),
                        ("wire transfer", "Mentions payment via wire transfer"),
                        ("pay for training", "Requires upfront payment for equipment or training"),
                        ("cashier check", "Mentions cashier's checks or advance fee payment"),
                        ("crypto", "Mentions cryptocurrency payments"),
                        ("western union", "Mentions wire transfer services"),
                        ("bank account details", "Requests sensitive banking details early in process"),
                        ("no experience required", "Suspiciously high pay with no experience required"),
                        ("fee", "Mentions application or processing fees")
                    ]

                    for keyword, description in scam_triggers:
                        if keyword in text_lower:
                            red_flags.append(description)

                    score = min(100, len(red_flags) * 25 + (15 if len(red_flags) > 0 else 0))

                    st.subheader("Detection Result")
                    if score >= 60:
                        st.error(f"🔴 **High Scam Risk** (Estimated Risk Score: {score}/100)")
                    elif score >= 25:
                        st.warning(f"🟡 **Moderate Scam Risk** (Estimated Risk Score: {score}/100)")
                    else:
                        st.success(f"🟢 **Low Risk Detected** (Estimated Risk Score: {score}/100)")

                    if red_flags:
                        st.markdown("### Flagged Indicators:")
                        for flag in red_flags:
                            st.write(f"- 🚩 {flag}")
                    else:
                        st.write("No typical scam indicators found in the provided text.")
