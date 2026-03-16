import streamlit as st
import google.generativeai as genai
import os
from dotenv import load_dotenv
from docx import Document
import PyPDF2


# ==============================
# Load Environment Variables
# ==============================

load_dotenv()

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

model = genai.GenerativeModel("gemini-3-flash-preview")


# ==============================
# Extract Text Functions
# ==============================

def extract_text_from_docx(file):

    try:
        doc = Document(file)
        text = "\n".join([p.text for p in doc.paragraphs])
        return text

    except:
        return None


def extract_text_from_pdf(file):

    try:
        pdf_reader = PyPDF2.PdfReader(file)

        text = ""

        for page in pdf_reader.pages:
            text += page.extract_text()

        return text

    except:
        return None


# ==============================
# AI Resume Optimization
# ==============================

def optimize_resume(resume_text, mode, focus_areas, enhancements):

    prompt = f"""
You are an expert ATS (Applicant Tracking System) resume optimizer.

Optimization Mode:
{mode}

Focus Areas:
{focus_areas}

Enhancements:
{enhancements}

Resume Content:
{resume_text}

Tasks:

1. Rewrite the resume to improve ATS compatibility
2. Improve keyword matching
3. Suggest improvements
4. Provide an ATS score out of 100
"""

    response = model.generate_content(prompt)

    return response.text


# ==============================
# Streamlit Page Config
# ==============================

st.set_page_config(
    page_title="ATS Resume Optimizer",
    page_icon="📄",
    layout="wide"
)

st.title("📄 ATS Resume Optimizer")
st.markdown("Transform your resume into an ATS optimized document")


# ==============================
# Sidebar Settings
# ==============================

with st.sidebar:

    st.header("⚙️ Optimization Settings")

    optimization_mode = st.selectbox(
        "Optimization Mode",
        [
            "Aggressive",
            "Balanced",
            "Conservative",
            "Industry-Specific"
        ]
    )

    focus_areas = st.multiselect(
        "Focus Areas",
        [
            "Software Engineering",
            "Data Science",
            "Product Management",
            "Marketing",
            "Finance",
            "Consulting"
        ],
        default=["Software Engineering"]
    )

    enhancements = st.multiselect(
        "Enhancements",
        [
            "Impact-Driven Language",
            "Keyword Density",
            "Achievement Highlights",
            "Skills Alignment"
        ]
    )


# ==============================
# Resume Input
# ==============================

col1, col2 = st.columns(2)

resume_text = ""

with col1:

    st.subheader("Upload Resume")

    uploaded_file = st.file_uploader(
        "Upload PDF or DOCX",
        type=["pdf", "docx"]
    )

    if uploaded_file:

        if uploaded_file.name.endswith(".pdf"):
            resume_text = extract_text_from_pdf(uploaded_file)

        elif uploaded_file.name.endswith(".docx"):
            resume_text = extract_text_from_docx(uploaded_file)


with col2:

    st.subheader("Or Paste Resume")

    resume_text_input = st.text_area(
        "Paste Resume Text",
        height=200
    )

if resume_text_input:
    resume_text = resume_text_input


# ==============================
# Optimize Button
# ==============================

if st.button("🚀 Optimize Resume", use_container_width=True):

    if not resume_text:
        st.error("Please upload or paste resume text")
        st.stop()

    with st.spinner("AI optimizing resume..."):

        result = optimize_resume(
            resume_text,
            optimization_mode,
            focus_areas,
            enhancements
        )

    st.markdown("---")

    st.header("Optimization Results")

    tab1, tab2 = st.tabs(["Optimized Resume", "Analysis"])

    with tab1:

        st.markdown(result)

        st.download_button(
            "Download Result",
            result,
            file_name="optimized_resume.txt",
            mime="text/plain"
        )

    with tab2:

        st.text_area(
            "Original Resume",
            resume_text,
            height=300
        )