# matcher.py

import pandas as pd
import json

def parse_job_data(raw_text):
    lines = raw_text.strip().split('\n')
    jobs = []
    for line in lines:
        if '\t' in line:
            title, description = line.split('\t', 1)
            jobs.append({"Job Title": title.strip(), "Job Description": description.strip()})
    return jobs

def save_data(jobs, csv_path='data/job_data.csv', json_path='data/job_data.json'):
    df = pd.DataFrame(jobs)
    df.to_csv(csv_path, index=False)
    with open(json_path, 'w') as f:
        json.dump(jobs, f, indent=2)

def load_jobs(csv_path='data/job_data.csv'):
    return pd.read_csv(csv_path)
