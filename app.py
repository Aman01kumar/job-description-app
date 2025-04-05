# app.py

import streamlit as st
import pandas as pd
from matcher import load_jobs

st.set_page_config(layout="wide", page_title="Job Descriptions Viewer")

st.title("📋 Job Descriptions Browser")

# Load job data
df = load_jobs()

# Sidebar filters
job_titles = sorted(df["Job Title"].unique())
selected_jobs = st.sidebar.multiselect("Filter by Job Title", job_titles, default=job_titles)

search_query = st.sidebar.text_input("Search within descriptions")

filtered_df = df[df["Job Title"].isin(selected_jobs)]

if search_query:
    filtered_df = filtered_df[filtered_df["Job Description"].str.contains(search_query, case=False, na=False)]

st.markdown(f"### {len(filtered_df)} Matching Job(s)")

for _, row in filtered_df.iterrows():
    with st.expander(f"🧑‍💻 {row['Job Title']}"):
        st.write(row['Job Description'])

# Download buttons
st.download_button("📥 Download CSV", data=filtered_df.to_csv(index=False), file_name="filtered_jobs.csv", mime="text/csv")
st.download_button("📥 Download JSON", data=filtered_df.to_json(orient="records", indent=2), file_name="filtered_jobs.json", mime="application/json")
