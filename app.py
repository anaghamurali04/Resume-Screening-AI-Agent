import streamlit as st
import fitz
import docx
import os
import re
from dotenv import load_dotenv
from openai import OpenAI
load_dotenv()
client=OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
st.title("AI Resume Screening Agent")
st.write("Upload resumes and compare them with job description")
