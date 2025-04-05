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

# --- Upload Job Description ---
st.subheader("Step 1: Upload a Job Description (.txt or .pdf)")
job_file = st.file_uploader("Upload Job Description", type=["txt", "pdf"])

# --- Use resumes from a local folder ---
st.subheader("Step 2: Matching Against Resume Folder")
resume_folder_path = "resumes"  # Update this to the actual folder path with resumes

if st.button("🔍 Match Best Resume") and job_file:
    with st.spinner("Processing..."):

        # Save job description to temp and extract text
        job_path = save_uploaded_file(job_file)
        if job_file.name.endswith('.pdf'):
            job_text = extract_text_from_pdf(job_path)
        else:
            with open(job_path, 'r', encoding='utf-8') as f:
                job_text = f.read()

        # Make sure resume folder exists
        if not os.path.exists(resume_folder_path) or not os.listdir(resume_folder_path):
            st.error(f"❌ Resume folder not found or is empty: `{resume_folder_path}`")
        else:
            # Match best resume from the folder
            best_resume_path, score = match_resume_to_job(job_text, resume_folder_path)

            if best_resume_path:
                best_resume_name = os.path.basename(best_resume_path)
                st.success(f"✅ Best Matching Resume: **{best_resume_name}**")
                st.info(f"🧠 Similarity Score: **{score:.2f}**")
            else:
                st.warning("No matching resume found.")
