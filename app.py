import streamlit as st
from resume_parser import extract_text_from_pdf, extract_text_from_docx, extract_text_from_text_input
from skill_extractor import extract_skills
from job_matching import match_jobs, load_jobs
from recommendation import show_recommendation

st.set_page_config(page_title="CareerPilot AI", page_icon="🚀", layout="centered")
st.title("CareerPilot AI — Resume → Best Job Match")

option = st.radio("Resume Input Method", ["Upload PDF", "Upload DOCX", "Paste Text"])
resume_text = ""

if option == "Upload PDF":
    pdf_file = st.file_uploader("Upload PDF Resume", type=["pdf"])
    if pdf_file is not None:
        resume_text = extract_text_from_pdf(pdf_file)

elif option == "Upload DOCX":
    docx_file = st.file_uploader("Upload DOCX Resume", type=["docx"])
    if docx_file is not None:
        resume_text = extract_text_from_docx(docx_file)

elif option == "Paste Text":
    text_input = st.text_area("Paste your Resume Text here")
    if st.button("Submit"):
        resume_text = extract_text_from_text_input(text_input)

if resume_text:
    st.success("Resume extracted successfully!")
    skills_found = extract_skills(resume_text)
    st.markdown("### 🟢 Skills Detected:")
    st.write(", ".join(skills_found) if skills_found else "No skills detected")
    
    jobs_df = load_jobs("jobs.csv")
    results = match_jobs(skills_found, jobs_df=jobs_df)
    top = results[0]
    rec = show_recommendation(top)

    st.subheader("🎯 Best Job Recommendation")
    st.write(f"**Role:** {rec['Job Role']}")
    st.write(f"**Match Score:** {rec['Match Score']}%")
    st.write(f"**Salary Range:** {rec['Salary Range']}")
    st.write(f"**Experience:** {rec['Experience']}")
    st.write("**Description:**")
    st.write(rec["Job Description"])

    st.write("### 🟢 Skills Matched:")
    st.write(", ".join(rec["Skills Matched"]) if rec["Skills Matched"] else "None")

    st.write("### 🔴 Skills Missing:")
    st.write(", ".join(rec["Skills Missing"]) if rec["Skills Missing"] else "None")

    st.write("### 📚 Recommended Courses:")
    for skill, links in rec["Courses"].items():
        if links:
            st.markdown(f"**{skill.upper()}**")
            for label, url in links:
                st.markdown(f"- [{label}]({url})")
        else:
            st.markdown(f"**{skill.upper()}** — (Coming soon)")
