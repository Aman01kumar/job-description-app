import streamlit as st
import pandas as pd

st.set_page_config(page_title="Job Descriptions Browser", page_icon="📋")

st.title("📋 Job Descriptions Browser")

# Load CSV data
try:
    df = pd.read_csv("data/jobs.csv")
    st.success("Data loaded successfully!")
    
    # Show filter
    job_titles = df["Job Title"].unique()
    selected_job = st.selectbox("Choose a job role:", job_titles)

    # Show selected job
    job_info = df[df["Job Title"] == selected_job]["Job Description"].values[0]
    st.subheader(f"{selected_job} Description")
    st.write(job_info)

except FileNotFoundError:
    st.error("❌ Data file not found. Make sure `data/jobs.csv` exists.")

