import streamlit as st

# Page title & config
st.set_page_config(page_title="Resume & Job Matcher", page_icon="📄", layout="centered")

st.title("📄 Resume & Job Description Matcher")
st.write("Upload your resume and enter the target job description.")

st.divider()

# 1. Resume Upload Button
uploaded_file = st.file_uploader(
    "1. Upload Resume", 
    type=["pdf", "docx", "txt"],
    help="Upload file in PDF, DOCX, or TXT format"
)

# 2. Job Description Paste Box
job_description = st.text_area(
    "2. Paste Job Description", 
    height=200, 
    placeholder="Paste job description here..."
)

# Analyze Button
analyze_btn = st.button("Analyze Match", type="primary", use_container_width=True)

st.divider()

# 3. Result Show Area
st.subheader("3. Match Result")

if analyze_btn:
    if uploaded_file is not None and job_description.strip() != "":
        st.success("Analysis Complete!")
        
        # Placeholder for actual Backend/AI logic output
        st.metric(label="Match Score", value="85%", delta="High Match")
        
        st.write("**File Details:**", uploaded_file.name)
        st.write("**Key Matching Skills:** Python, Streamlit, Frontend Development")
    else:
        st.error("Please upload a resume file and enter the job description.")
else:
    st.info("After uploading and pasting, click the 'Analyze Match' button.")
