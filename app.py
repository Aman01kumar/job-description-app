import streamlit as st
import os
import tempfile

from resume_matcher import match_resume_to_job, extract_text_from_pdf

def save_uploaded_file(uploaded_file):
    with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(uploaded_file.name)[-1]) as tmp_file:
        tmp_file.write(uploaded_file.read())
        return tmp_file.name

st.set_page_config(page_title="📄 Resume Matcher", layout="centered")
st.title("📄 Resume Matcher for Job Descriptions")

# --- Step 1: Upload Job Description ---
st.subheader("Step 1: Upload a Job Description (.txt or .pdf)")
job_file = st.file_uploader("Upload Job Description", type=["txt", "pdf"])

# --- Step 2: Upload Resumes ---
st.subheader("Step 2: Upload Resumes (.txt or .pdf)")
resume_files = st.file_uploader("Upload one or more resumes", type=["txt", "pdf"], accept_multiple_files=True)

# --- Match Button ---
match_clicked = st.button("🔍 Match Best Resume")

if match_clicked:
    if job_file and resume_files:
        with st.spinner("Processing..."):

            # Save and extract job description text
            job_path = save_uploaded_file(job_file)
            if job_file.name.endswith('.pdf'):
                job_text = extract_text_from_pdf(job_path)
            else:
                with open(job_path, 'r', encoding='utf-8') as f:
                    job_text = f.read()

            # Save resumes and collect paths
            resume_paths = []
            for resume_file in resume_files:
                resume_path = save_uploaded_file(resume_file)
                resume_paths.append(resume_path)

            # Match best resume
            best_resume_path, score, _ = match_resume_to_job(job_text, resume_paths)

            if best_resume_path:
                best_resume_name = os.path.basename(best_resume_path)
                st.success(f"✅ Best Matching Resume: **{best_resume_name}**")
                st.info(f"🧠 Similarity Score: **{score:.2f}**")

                # Show resume content
                st.subheader("📄 Resume Preview")
                if best_resume_path.endswith(".pdf"):
                    resume_text = extract_text_from_pdf(best_resume_path)
                else:
                    with open(best_resume_path, "r", encoding="utf-8") as f:
                        resume_text = f.read()

                st.text_area("Resume Content", resume_text, height=400)
            else:
                st.warning("⚠️ No matching resume found.")
    else:
        st.warning("⚠️ Please upload both a job description and at least one resume.")
