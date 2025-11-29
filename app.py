import streamlit as st
import os
from sentence_transformers import SentenceTransformer,util
import numpy as np
import fitz
import docx
from dotenv import load_dotenv
load_dotenv()
model=SentenceTransformer('all-MiniLM-L6-v2')
st.set_page_config(page_title="Resume Screening AI Agent",layout="wide")
st.title("Resume Screening AI Agent")
st.write("Upload a resume and job description to get an AI-powered compatibility score.")
def extract_text_from_pdf(file):
  pdf=fitz.open(stream=file.read(),filetype="pdf")
  text=""
  for page in pdf:
    text+=page.get_text()
  return text
def extract_text_from_docx(file):
  doc=docx.Document(file)
  return "\n".join([para.text for para in doc.paragraphs])
def extract_text_from_txt(file):
  return file.read().decode("utf-8")
def calculate_match_score(resume_text,jd_text):
  resume_emb=model.encode(resume_text,convert_to_tensor=True)
  jd_emb=model.encode(jd_text,convert_to_tensor=True)
  score=util.cos_sim(resume_emb,jd_emd).item()
  return round(score*100,2)
uploaded_file=st.file_uploader("Upload Resume (PDF,DOCX,TXT)",type=["pdf","docx","txt"])
job_description=st.text_area("Attach Job Description",height=250)
if st.button("Analyse Resume"):
  if uploaded_file is None:
    st.error("Please upload a resume file.")
  elif job_description.strip()=="":
    st.error("Please attach a job description.")
  else:
    ext=uploaded_file.name.split(".")[-1].lower()
    if ext=="pdf":
      resume_text=extract_text_from_pdf(uploaded_file)
    elif ext=="docx":
      resume_text=extract_text_from_docx(uploaded_file)
    elif ext=="txt":
      resume_text=extract_text_from_txt(uploaded_file)
    else:
      st.error("Unsupported filr format.")
      st.stop()
    score=calculate_match_score(resume_text,job_description)
    st.subheader("Feedback")
    if score>75:
      st.success("Excellent match! This resume aligns strongly with the job requirements.")
    elif score>50:
      st.warning("Moderate match. The resume could be improved to align better with the JD.")
    else:
      st.error("Low match. Skills and experience do not align well with job description.")
