import streamlit as st
import fitz  
from docx import Document
from sentence_transformers import SentenceTransformer, util
import numpy as np
import os
st.title(" AI Resume Screening Agent")
def load_model():
    return SentenceTransformer("all-MiniLM-L6-v2")
model = load_model()
def extract_pdf_text(uploaded_file):
    doc = fitz.open(stream=uploaded_file.read(), filetype="pdf")
    text = ""
    for page in doc:
        text += page.get_text()
    return text
def extract_docx_text(uploaded_file):
    doc = Document(uploaded_file)
    return "\n".join([para.text for para in doc.paragraphs])
def extract_txt_text(uploaded_file):
    return uploaded_file.read().decode("utf-8")
uploaded_resume = st.file_uploader("Upload resume (PDF / DOCX / TXT)", type=["pdf", "docx", "txt"])
job_description = st.text_area("Paste Job Description")
if st.button("Run Screening"):
    if uploaded_resume is None or job_description.strip() == "":
        st.error("Please upload a resume and enter a job description.")
    else:
        if uploaded_resume.name.endswith(".pdf"):
            resume_text = extract_pdf_text(uploaded_resume)
        elif uploaded_resume.name.endswith(".docx"):
            resume_text = extract_docx_text(uploaded_resume)
        else:
            resume_text = extract_txt_text(uploaded_resume)
        resume_emb = model.encode(resume_text)
        jd_emb = model.encode(job_description)
        similarity = util.cos_sim(resume_emb, jd_emb).item()
        score = round(similarity * 100, 2)

        st.subheader("Result")
        st.write(f"### Resume Match Score: **{score}%**")

        if score > 75:
            st.success("Excellent match ✔")
        elif score > 50:
            st.warning("Moderate match ⚠")
        else:
            st.error("Low match ❌")
        with st.expander("View Extracted Resume Text"):
            st.write(resume_text)
