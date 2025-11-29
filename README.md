# Resume Screening AI Agent
An AI Streamlit application that evaluates multiple resumes against a job description using **Google Gemini** model. This tool extracts the text from PDFs, analyses candidate fit, assigns a score and ranks the resumes, thereby making shortlisting faster and more accurate.
---
##Features
- Upload **multiple resumes(PDF)**
- Upload **Job Description(PDF)**
- Automatic PDF text extraction using PyPDF2
- Resume evaluation using **Gemini 2.0 Flash**
- Detailed analysis: Strengths, weaknesses, recommendation
- Streamlit-based UI, deployable on Streamlit Cloud
---
## System Architecture
1. **User Uploads PDFs** -> Job Description + Resume PDFs
2. **PDF Text Extractor** -> reads text using PyPDF2
3. **Gemini Model API** -> receives promtp + extracted text
4. Model returns:
   - Score (0-100)
   - Strengths
   - Weaknesses
   - Recommendation
5. **Streamlit App** -> Ranks resumes and displays results
---
## Tech Stack
- Frontend UI -> Streamlit
- Language -> Python
- AI Model -> Google Gemini 2.0 Flash
- PDF Reader -> PyPDF2
- Deployment -> Streamlit Cloud
---
## Project Structure
Resume-Screening-AI-Agent
|--app.py
|--requirements.txt
|--README.md
|--diagram/architecture_diagram
---
## To Run Locally
1. Clone the Repository
2. Create and activate a virtual environment
3. Install Dependencies
4. Run the application
---
## Deployment to Streamlit Cloud
1. Push the project to GitHub Public Repository
2. Go to share.streamlit.io
3. Connect GitHub repo
4. Add Gemini API key in Secrets Management
5. Deploy
---
## Guide to use the Streamlit App
1. Upload **Job Description PDF**
2. Upload **Multiple Resume PDFs**
3. Click **Analyze Resumes**
4. View:
   - Score out of 100
   - Strengths
   - Weaknesses
   - Final Recommendations
---
## Limitations
- PDF extraction may struggle with scanned PDFs and images inside PDF
- The Gemini scoring may vary slightly per request
- Requires stable network connection for API calls
---
## Future Improvements
- Support for DOCX resumes
- Visual bar chart scoring
- Export results as PDF or Excel
- Multi-language resume support
---
## License
This project is open for educational and demo use.
---
## Author 
By Anagha Murali
