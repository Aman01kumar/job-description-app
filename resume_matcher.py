import fitz  # PyMuPDF
from preprocess import preprocess_text
from matcher import compute_similarity


def extract_text_from_pdf(pdf_path):
    """Extracts all text from a PDF file using PyMuPDF."""
    try:
        with fitz.open(pdf_path) as doc:
            text = ""
            for page in doc:
                text += page.get_text()
            return text
    except Exception as e:
        print(f"Error reading PDF {pdf_path}: {e}")
        return ""


def match_resume_to_job(job_desc, resume_paths):
    """
    Matches resumes against a job description using cosine similarity.

    Args:
        job_desc (str): Raw job description text.
        resume_paths (list): List of file paths to resumes (.pdf or .txt).

    Returns:
        best_resume_path (str): Path to the best-matching resume.
        best_score (float): Cosine similarity score for the best match.
        ranked_list (list): List of tuples (resume_path, score) sorted by score descending.
    """
    processed_job_desc = preprocess_text(job_desc)
    similarity_results = []

    for resume_path in resume_paths:
        try:
            if resume_path.endswith('.txt'):
                with open(resume_path, 'r', encoding='utf-8') as f:
                    resume_text = f.read()
            elif resume_path.endswith('.pdf'):
                resume_text = extract_text_from_pdf(resume_path)
            else:
                print(f"Unsupported file format: {resume_path}")
                continue

            processed_resume = preprocess_text(resume_text)
            score = compute_similarity(processed_job_desc, processed_resume)
            similarity_results.append((resume_path, score))
        except Exception as e:
            print(f"Error processing {resume_path}: {e}")
            continue

    # Sort resumes by score (highest first)
    ranked_list = sorted(similarity_results, key=lambda x: x[1], reverse=True)
    best_resume_path, best_score = ranked_list[0] if ranked_list else (None, -1)

    return best_resume_path, best_score, ranked_list
