import streamlit as st
import fitz 
import docx
import re
from openai import OpenAI
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
st.title("Resume Screening AI Agent")
st.write("Upload multiple resumes and compare them with a job description.")
def extract_text(file):
    if file.type == "application/pdf":
        pdf = fitz.open(stream=file.read(), filetype="pdf")
        text = ""
        for page in pdf:
            text += page.get_text()
        return text

    elif file.type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
        document = docx.Document(file)
        return "\n".join([para.text for para in document.paragraphs])
    return ""
def extract_score(text):
    match = re.search(r"(\d{1,3})\s*/?\s*100", text)
    if match:
        return min(int(match.group(1)),100)
    match = re.search(r"\b(\d{1,3})\b", text)
    if match:
        return min(int(match.group(1)), 100)
    return 0
job_description = st.text_area("Enter Job Description", height=200)
uploaded_files = st.file_uploader("Upload Multiple Resumes (PDF or DOCX)",type=["pdf", "docx"],accept_multiple_files=True)
start_btn = st.button("Start Screening")
results = []  
if start_btn and uploaded_files and job_description.strip():
    st.subheader("Screening Results")
    for resume_file in uploaded_files:
        st.write(f"###  {resume_file.name}")
        try:
            resume_text = extract_text(resume_file)
        except:
            st.error(f"Could not parse {resume_file.name}")
            continue
        if not resume_text.strip():
            st.error(f"No text extracted from: {resume_file.name}")
            continue
        with st.spinner(f"Analyzing {resume_file.name}..."):
            try:
                response = client.responses.create(model="gpt-4.1",input=f"""Compare this resume with the job description and return:

Match Score: X/100  
Strengths  
Weaknesses  
Summary  

Job Description:
{job_description}
                   

Resume:
{resume_text}
"""
                )

                analysis = response.output_text
                score = extract_score(analysis)

                results.append({"name": resume_file.name,"score": score,"details": analysis})

                st.success("Analysis Complete")

            except Exception as e:
                st.error(f"Error analyzing {resume_file.name}: {str(e)}")
    st.subheader("Final Ranking of Candidates")
    if results:
        results_sorted = sorted(results, key=lambda x: x["score"], reverse=True)
        st.write("### Ranked Results")
        st.table(
            {
                "Rank": [i + 1 for i in range(len(results_sorted))],
                "Candidate": [r["name"] for r in results_sorted],
                "Match Score": [r["score"] for r in results_sorted]
            }
        )
        st.write("---")
        st.write("## Detailed Analysis for Each Resume")
        for idx, r in enumerate(results_sorted):
            st.write(f"### Rank {idx + 1}: {r['name']} (Score: {r['score']}/100)")
            st.write(r["details"])
            st.write("---")
else:
    st.info("Upload resumes and enter job description to begin.")
