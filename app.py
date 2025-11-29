import streamlit as st
import os
from sentence_transformers import SentenceTransformer,util
import fitz
import docx
model=SentenceTransformer('all-MiniLM-L6-v2')
def read_pdf(file):
  text=""
  pdf=fitz.open(stream=file.read(),filetype="pdf")
  for page in pdf:
    text+=page.get_text()
  return text
def read_docx(file):
  doc=docx.Document(file)
  return "\n".join([p.text for p in doc.paragraphs])
def read_txt(file):
    return file.read().decode("utf-8")
def extract_text(file):
  if file.type=="application/pdf":
    return read_pdf(file)
  elif file.type=="application/vnd.openxmlformats-officedocument.wordprocessingml.document":
    return read_docx(file)
  elif file.type=="text/plain":
    return read_txt(file)
  else:
    return None

st.title("Resume Screening AI Agent")
st.write("Upload resumes and the job description to get a similarity score.")
job_desc_file=st.file_uploader("Upload the Job Description (PDF/DOCX/TXT)",type=["pdf","docx","txt"])
resume_files=st.file_uploader("Upload Resumes ",type=["pdf","docx","txt"],accept_mutliple_files=True)
if st.button("Run Screening"):
  if job_desc_file and resume_files:
    job_desc_text=extract_text(job_desc_file)
    jd_embedding=model.encode(job_desc_text,convert_to_tensor=True)
    st.subheader("Results: ")
    for resume in resume_files:
      resume_text=extract_text(resume)
      resume_embedding=model.encode(resume_text,convert_to_tensor=True)
      similarity=util.cos_sim(jd_embedding,resume_embedding)[0][0].item()
      score=round(similarity*100,2)
      st.write(f"### {resume.name}")
      st.write(f"**Match Score:**{score}%")
  else:
    st.error("Please upload both the job description and resumes.")
