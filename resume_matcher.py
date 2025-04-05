import os
import json
import fitz  # PyMuPDF
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def extract_text_from_pdf(pdf_path):
    """Extract text from a single PDF file."""
    try:
        with fitz.open(pdf_path) as doc:
            return "\n".join(page.get_text() for page in doc)
    except Exception as e:
        return ""

def match_resumes_to_jobs(resume_folder, job_json_path, top_n=1):
    """Match resumes to job descriptions using cosine similarity."""
    # Load job descriptions
    if not os.path.exists(job_json_path):
        return {}

    with open(job_json_path, "r", encoding="utf-8") as f:
        jobs = json.load(f)

    job_texts = [job["Job Description"] for job in jobs]
    job_titles = [job["Job Title"] for job in jobs]

    matches = {}

    # Process each resume
    for resume_file in os.listdir(resume_folder):
        if resume_file.lower().endswith(".pdf"):
            resume_path = os.path.join(resume_folder, resume_file)
            resume_text = extract_text_from_pdf(resume_path)

            if resume_text.strip():
                # Combine job descriptions and the resume
                texts = job_texts + [resume_text]
                tfidf = TfidfVectorizer(stop_words="english").fit_transform(texts)

                # Calculate similarity between resume and each job
                sim_scores = cosine_similarity(tfidf[-1], tfidf[:-1]).flatten()
                top_indices = sim_scores.argsort()[::-1][:top_n]

                matches[resume_file] = {
                    "Top Match": job_titles[top_indices[0]],
                    "Score": round(float(sim_scores[top_indices[0]]), 3),
                    "Top 3 Matches": [
                        {"Job Title": job_titles[i], "Score": round(float(sim_scores[i]), 3)}
                        for i in top_indices[:3]
                    ],
                }

    return matches
