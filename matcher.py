import os
import pandas as pd
import json
import re
import logging
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

logging.basicConfig(level=logging.INFO)

# --- Text Preprocessing ---
def preprocess(text):
    text = text.lower()
    text = re.sub(r'[^a-z\s]', ' ', text)
    text = re.sub(r'\s+', ' ', text).strip()
    return text

# --- Parse job data from raw tab-separated text ---
def parse_job_data(raw_text):
    lines = raw_text.strip().split('\n')
    jobs = []
    for i, line in enumerate(lines):
        if '\t' in line:
            title, description = line.split('\t', 1)
            jobs.append({"Job Title": title.strip(), "Job Description": description.strip()})
        else:
            logging.warning(f"⚠️ Skipping line {i + 1}: No tab separator found.")
    return jobs

# --- Save job data to CSV and JSON ---
def save_data(jobs, csv_path='data/job_data.csv', json_path='data/job_data.json'):
    df = pd.DataFrame(jobs)
    os.makedirs(os.path.dirname(csv_path), exist_ok=True)
    df.to_csv(csv_path, index=False)
    with open(json_path, 'w') as f:
        json.dump(jobs, f, indent=2)
    logging.info(f"✅ Job data saved to {csv_path} and {json_path}")

# --- Load jobs from CSV ---
def load_jobs(csv_path="data/job_data.csv"):
    if not os.path.exists(csv_path):
        raise FileNotFoundError(f"📁 File not found: {csv_path}. Make sure it's in your GitHub repo.")
    return pd.read_csv(csv_path)

# --- Compute similarity between two texts ---
def compute_similarity(text1, text2):
    vectorizer = TfidfVectorizer()
    tfidf_matrix = vectorizer.fit_transform([preprocess(text1), preprocess(text2)])
    return cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])[0][0]

# --- Compute similarity of job text with multiple resumes ---
def match_resume_to_job(job_text, resume_paths):
    job_text = preprocess(job_text)
    resume_texts = []
    filenames = []

    for path in resume_paths:
        with open(path, 'r', encoding='utf-8', errors='ignore') as f:
            text = f.read()
            resume_texts.append(preprocess(text))
            filenames.append(path)

    # Compute bulk similarity
    vectorizer = TfidfVectorizer()
    tfidf_matrix = vectorizer.fit_transform([job_text] + resume_texts)
    similarity_scores = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:])[0]

    # Get the best match
    if similarity_scores.size == 0:
        return None, 0, []
    
    best_idx = similarity_scores.argmax()
    return filenames[best_idx], round(similarity_scores[best_idx] * 10, 1), list(similarity_scores * 10)

# --- CLI Example ---
if __name__ == "__main__":
    raw_path = "data/raw_data.txt"
    if os.path.exists(raw_path):
        with open(raw_path, "r", encoding="utf-8") as f:
            raw_text = f.read()
        jobs = parse_job_data(raw_text)
        save_data(jobs)
    else:
        logging.error(f"File not found: {raw_path}")
