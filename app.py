import streamlit as st
import os
import tempfile
import pandas as pd
import matplotlib.pyplot as plt

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

            # Save resumes and compute scores
            results = []
            for resume_file in resume_files:
                resume_path = save_uploaded_file(resume_file)
                score = match_resume_to_job(job_text, [resume_path])[1]  # assuming returns (path, score)
                results.append((resume_file.name, resume_path, score))

            # Sort by score descending
            results.sort(key=lambda x: x[2], reverse=True)

            # Best match
            best_resume_name, best_resume_path, best_score = results[0]
            st.success(f"✅ Best Matching Resume: **{best_resume_name}**")
            st.info(f"🧠 Similarity Score: **{best_score * 10:.2f} / 10**")

            # Resume Preview
            st.subheader("📄 Resume Preview")
            if best_resume_path.endswith(".pdf"):
                resume_text = extract_text_from_pdf(best_resume_path)
            else:
                with open(best_resume_path, "r", encoding="utf-8") as f:
                    resume_text = f.read()
            st.text_area("Best Resume Content", resume_text, height=400)

            # Create DataFrame for all results
            df_results = pd.DataFrame([
                {"Resume Name": name, "Score (out of 10)": round(score * 10, 2)}
                for name, _, score in results
            ])

            # Download Button
            st.download_button(
                label="📥 Download Results as CSV",
                data=df_results.to_csv(index=False).encode('utf-8'),
                file_name='resume_scores.csv',
                mime='text/csv'
            )

            # Bar Chart
            st.subheader("📊 Resume Matching Scores")
            st.bar_chart(df_results.set_index("Resume Name"))

            # Resume Preview Selector
            st.subheader("📂 Preview Any Resume")
            selected_resume_name = st.selectbox("Select a resume to preview", [name for name, _, _ in results])
            selected_path = next(path for name, path, _ in results if name == selected_resume_name)

            if selected_path.endswith(".pdf"):
                preview_text = extract_text_from_pdf(selected_path)
            else:
                with open(selected_path, "r", encoding="utf-8") as f:
                    preview_text = f.read()

            st.text_area("Selected Resume Content", preview_text, height=400)

    else:
        st.warning("⚠️ Please upload both a job description and at least one resume.")
