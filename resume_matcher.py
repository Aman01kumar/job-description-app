import fitz  # PyMuPDF
from preprocess import preprocess_text
from matcher import compute_similarity


def extract_text_from_pdf(pdf_path):
    doc = fitz.open(pdf_path)
    text = ""
    for page in doc:
        text += page.get_text()
    return text


def match_resume_to_job(job_desc, resume_paths):
    """
    job_desc: raw job description text (string)
    resume_paths: list of file paths to resume files

    Returns:
        best_resume_path (str)
        best_score (float)
        ranked_list (list of tuples): [(resume_path, score), ...] sorted by score descending
    """
    processed_job_desc = preprocess_text(job_desc)
    similarity_results = []

    for resume_path in resume_paths:
        if resume_path.endswith('.txt'):
            with open(resume_path, 'r', encoding='utf-8') as f:
                resume_text = f.read()
        elif resume_path.endswith('.pdf'):
            resume_text = extract_text_from_pdf(resume_path)
        else:
            continue  # skip unsupported formats

        processed_resume = preprocess_text(resume_text)
        score = compute_similarity(processed_job_desc, processed_resume)
        similarity_results.append((resume_path, score))

    # Sort resumes by similarity score descending
    ranked_list = sorted(similarity_results, key=lambda x: x[1], reverse=True)

    # Get best match
    best_resume_path, best_score = ranked_list[0] if ranked_list else (None, -1)

    return best_resume_path, best_score, ranked_list
