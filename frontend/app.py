import requests
import streamlit as st

API_URL = st.sidebar.text_input("Backend URL", "http://127.0.0.1:8000")

st.set_page_config(page_title="JobGuard AI", page_icon="📄", layout="centered")
st.title("JobGuard AI")
st.caption("Resume matching and job-risk analysis")

try:
    jobs = requests.get(f"{API_URL}/api/jobs", timeout=5).json()
except Exception:
    jobs = []
    st.error("Backend is not running. Start the FastAPI server first.")

uploaded = st.file_uploader("Upload Resume", type=["pdf", "docx"])

if jobs:
    labels = {f"{j['id']}. {j['job_title']} — {j['category']}": j for j in jobs}
    selected = st.selectbox("Select a job", list(labels))
    job = labels[selected]
else:
    job = None

if st.button("Analyze", type="primary", use_container_width=True):
    if not uploaded or not job:
        st.warning("Upload a resume and select a job.")
    else:
        files = {"resume": (uploaded.name, uploaded.getvalue(), uploaded.type)}
        data = {"job_id": str(job["id"])}
        with st.spinner("Analyzing resume..."):
            response = requests.post(f"{API_URL}/api/analyze", files=files, data=data, timeout=120)
        if response.ok:
            result = response.json()
            matching = result["matching"]
            risk = result["scam_risk"]
            st.success("Analysis complete")
            st.metric("Match Score", f"{matching['match_score']}%")
            st.write(f"**Semantic Score:** {matching['semantic_score']}%")
            st.write(f"**Skill Score:** {matching['skill_score']}%")
            st.subheader("Matching Skills")
            st.write(", ".join(matching["matching_skills"]) or "None found")
            st.subheader("Missing Skills")
            st.write(", ".join(matching["missing_skills"]) or "None")
            st.subheader("Job Risk")
            st.write(f"**{risk['risk_level']} — {risk['risk_score']}/100**")
            for reason in risk["reasons"]:
                st.write(f"- {reason}")
        else:
            st.error(response.text)
