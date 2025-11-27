import streamlit as st
import pandas as pd

from resume_parser import extract_text_from_pdf, extract_text_from_docx, clean_text
from ats import compute_ats_score
from heatmap import plot_skill_gap
from coverletter import generate_cover_letter
from pdf_report import create_pdf_report
from db import init_db, save_resume

import tempfile
import os

# ============= INITIAL SETUP =============
st.set_page_config(page_title="CareerPilot AI", layout="wide")
st.title("🚀 CareerPilot AI — Smart Resume & Job Match Tool")

# Initialize database
init_db()

# Load job dataset
jobs = pd.read_csv("jobs.csv")

# ============= FILE UPLOAD =============
st.header("📄 Upload Your Resume")

uploaded_file = st.file_uploader("Upload PDF or DOCX", type=["pdf", "docx"])

resume_text = ""
skills_found = []

if uploaded_file:
    file_ext = uploaded_file.name.split(".")[-1].lower()

    with tempfile.NamedTemporaryFile(delete=False) as tmp_file:
        tmp_file.write(uploaded_file.read())
        temp_path = tmp_file.name

    if file_ext == "pdf":
        try:
            resume_text = extract_text_from_pdf(temp_path)
        except:
            st.error("Error reading PDF. Please upload a proper PDF file.")
    elif file_ext == "docx":
        resume_text = extract_text_from_docx(temp_path)

    os.remove(temp_path)

    resume_text = clean_text(resume_text)

    st.subheader("📌 Resume Text Extracted")
    st.text_area("Extracted Resume Content", resume_text, height=250)

    # Extract Skills
    all_skills = set()
    for skills in jobs["skills"]:
        for s in skills.split(","):
            all_skills.add(s.strip().lower())

    skills_found = [s for s in all_skills if s in resume_text]

    st.subheader("🧠 Skills Identified")
    st.write(", ".join(skills_found) if skills_found else "No skills found.")

    # ============= JOB MATCHING =============
    st.header("🎯 Job Match Results")

    job_scores = []
    for index, row in jobs.iterrows():
        job_skill_list = [s.strip().lower() for s in row["skills"].split(",")]

        matched = [s for s in job_skill_list if s in skills_found]
        missing = [s for s in job_skill_list if s not in skills_found]

        score = int((len(matched) / len(job_skill_list)) * 100)

        job_scores.append({
            "Job Role": row["job_title"],
            "Match Score (%)": score,
            "Skills Matched": matched,
            "Skills Missing": missing
        })

    job_scores = sorted(job_scores, key=lambda x: x["Match Score (%)"], reverse=True)
    top = job_scores[0]

    st.subheader("🏆 Best Match")
    st.write(f"**Role:** {top['Job Role']}")
    st.write(f"**Match Score:** {top['Match Score (%)']}%")
    st.write(f"**Matched Skills:** {', '.join(top['Skills Matched'])}")
    st.write(f"**Missing Skills:** {', '.join(top['Skills Missing'])}")

    st.write("---")
    st.header("✨ Advanced Resume Analysis")

    # ============= ATS SCORE =============
    if st.button("📊 Calculate ATS Score"):
        expected_skills = top["Skills Matched"] + top["Skills Missing"]
        score, breakdown = compute_ats_score(resume_text, expected_skills)
        st.success(f"ATS Score: {score}/100")
        st.json(breakdown)

    # ============= SKILL HEATMAP =============
    if st.button("🔥 Show Skill Gap Heatmap"):
        fig = plot_skill_gap(top["Skills Matched"] + top["Skills Missing"], skills_found)
        st.pyplot(fig)

    # ============= COVER LETTER =============
    st.subheader("📝 Generate Cover Letter")

    name_input = st.text_input("Your Name")
    company_input = st.text_input("Company Name")

    if st.button("✍ Generate Cover Letter"):
        if not name_input or not company_input:
            st.error("Enter your name & company name first.")
        else:
            cover_letter = generate_cover_letter(
                name=name_input,
                role=top["Job Role"],
                company=company_input,
                resume_text=resume_text,
                skills=skills_found
            )
            st.text_area("Your Cover Letter", cover_letter, height=300)

    # ============= PDF REPORT =============
    if st.button("📥 Download PDF Report"):
        breakdown = compute_ats_score(resume_text, skills_found)[1]
        pdf_buffer = create_pdf_report(
            name_input if name_input else "Candidate",
            top,
            breakdown,
            skills_found
        )

        st.download_button(
            label="Download PDF",
            data=pdf_buffer,
            file_name="CareerPilot_Report.pdf",
            mime="application/pdf"
        )

    # ============= SAVE TO DATABASE =============
    st.write("---")
    st.subheader("💾 Save Your Analysis")

    email_input = st.text_input("Your Email")

    if st.button("Save to Database"):
        if not name_input or not email_input:
            st.error("Enter your name & email before saving.")
        else:
            score, _ = compute_ats_score(resume_text, skills_found)
            save_resume(name_input, email_input, resume_text, skills_found,
                        top["Job Role"], score)
            st.success("Saved successfully! 🎉")

