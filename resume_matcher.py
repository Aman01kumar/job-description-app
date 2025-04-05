# resume_matcher.py

import os
import fitz  # PyMuPDF
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def extract_text_from_pdf(pdf_path):
    text = ""
    try:
        with fitz.open(pdf_path) as doc:
            for page in doc:
                text += page.get_text()
    except Exception as e:
        print(f"Error reading {pdf_path}: {e}")
    return text

def match_resumes_to_jobs(resume_folder, job_data_path, top_n=3):
    resumes = []
    for filename in os.listdir(resume_folder):
        if filename.endswith(".pdf"):
            path = os.path.join(resume_folder, filename)
            text = extract_text_from_pdf(path)
            resumes.append({"filename": filename, "text": text})

    jobs_df = pd.read_csv(job_data_path)
    job_texts = jobs_df["Job Description"].tolist()
    job_titles = jobs_df["Job Title"].tolist()

    results = []

    for resume in resumes:
        combined_docs = [resume["text"]] + job_texts
        vectorizer = TfidfVectorizer(stop_words="english")
        tfidf_matrix = vectorizer.fit_transform(combined_docs)
        similarities = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:]).flatten()
        top_indices = similarities.argsort()[::-1][:top_n]

        matched_jobs = [{"job_title": job_titles[i], "score": float(similarities[i])} for i in top_indices]
        results.append({
            "resume": resume["filename"],
            "matches": matched_jobs
        })

    return results
    