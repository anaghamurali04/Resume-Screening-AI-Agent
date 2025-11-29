import streamlit as st
import google.generativeai as genai
import PyPDF2
import tempfile
import os
import re
genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
st.title("Resume Screening AI Agent")
st.write("Upload esumes and compare them against a job description.")
def extract_text_from_pdf(uploaded_file):
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
        tmp.write(uploaded_file.read())
        tmp_path = tmp.name
    reader = PyPDF2.PdfReader(tmp_path)
    text = ""
    for page in reader.pages:
        try:
            page_text = page.extract_text()
            if page_text:
                text += page_text
        except:
            continue
    return text.strip()
def evaluate_resume(resume_text, job_description):

    prompt = f"""You are an expert HR evaluator. Analyze the following resume against the job description.

JOB DESCRIPTION:
{job_description}

RESUME:
{resume_text}

Provide the following in structured format:

Score (0-100):
Strengths:
Weaknesses:
Final Recommendation:"""
    model = genai.GenerativeModel("models/text-bison-001")
    try:
        response = model.generate_content(prompt)
        return response.text if response else "No response received."
    except Exception as e:
        return f"AI Model Error: {e}"
job_description_file = st.file_uploader("Upload Job Description (PDF)", type=["pdf"])
resume_files = st.file_uploader("Upload Multiple Resumes (PDF)", type=["pdf"], accept_multiple_files=True)
if st.button("Analyze Resumes"):
    if not job_description_file:
        st.error("Please upload a job description!")
    elif not resume_files:
        st.error("Please upload at least one resume!")
    else:
        st.success("Processing...")
        job_text = extract_text_from_pdf(job_description_file)
        results = []
        for resume in resume_files:
            with st.spinner(f"Analyzing {resume.name} ..."):
                resume_text = extract_text_from_pdf(resume)
                analysis = evaluate_resume(resume_text, job_text)
                match = re.search(r"(\d{1,3})", analysis)
                score = int(match.group(1)) if match else 0
                results.append({"name": resume.name,"score": score,"analysis": analysis})
        results = sorted(results, key=lambda x: x["score"], reverse=True)
        st.subheader("Ranked Results")
        for idx, r in enumerate(results, 1):
            st.write(f"### {idx}. {r['name']} — **Score: {r['score']}**")
            st.write(r["analysis"])
            st.markdown("---")
