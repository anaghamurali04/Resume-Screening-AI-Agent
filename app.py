import streamlit as st
import os
from dotenv import load_dotenv
from sentence_transformers import SentenceTransformer,util
import fitz
import docx
import numpy as np
from openai import OpenAI
load_dotenv()
client=OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
model=SentenceTransformer('all-MiniLM-L6-v2')
st.title("Resume Screening Agent")
st.write("Upload resumes and compare them with the job description")
def load_jd():
  with open("job_description/jd.txt","r",encoding="utf-8") as f:
    return f.read()
job_description=load_jd()
jd_embedding=model.encode(job_description)
def read_pdf(path):
  text=""
  pdf=fitz.open(path)
  for page in pdf:
    text+=page.get_text()
  return text
def read_docx(path):
  doc=docx.Document(path)
  return "\n".join([p.text for p in doc.paragraphs])
def read_txt(path):
  with open(path,"r",encoding="utf-8") as f:
    return f.read()
def read_resume(file_path):
  if file_path.endswith(".pdf"):
    return read_pdf(file_path)
  elif file_path.endswith(".docx"):
    return read_docx(file_path)
  elif file_path.endswith(".txt"):
    return read_txt(file_path)
  else:
    return ""
def score_resume(resume_text):
  resume_embedding=model.encode(resume_text)
  similarity=util.cos_sim(jd_embedding,resume_embedding)
  return float(similarity)
uploaded_files=st.file_uploader("Upload Resumes",type=["pdf","docx","txt"],accept_multiple_files=True)
if st.button("Process Resumes"):
  if uploaded_files:
    results=[]
  for file in uploaded_files:
    file_path=os.path.join("resumes",file.name)
    with open(file_path,"wb") as f:
      f.write(file.getbuffer())
    text=read_resume(file_path)
    score=score_resume(text)
    results.append((file.name,score))
  sorted_results=sorted(results,key=lambda x:x[1],reverse=True)
  st.subheader("Ranking Results: ")
  for name,score in sorted_results:
    st.write(f"**{name}** - Match Score: {round(score*100,2)}%")
else:
  st.warning("Please upload atleast one resume.")
