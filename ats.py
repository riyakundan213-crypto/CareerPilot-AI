# ats.py
import re

def compute_ats_score(resume_text, skills_expected, min_length=200):
    """
    Simple ATS scoring:
    - Length score (max 20)
    - Skills match score (max 50)
    - Important keywords score (max 30)
    Returns ATS score (0–100) and breakdown.
    """
    text = resume_text.lower()
    length = len(text)
    length_score = min(1.0, length / (min_length*2)) * 20  # up to 20 pts

    # Skills check
    skills_expected = [s.lower() for s in skills_expected]
    found_skills = [s for s in skills_expected if re.search(r"\b" + re.escape(s) + r"\b", text)]
    skills_score = (len(found_skills) / len(skills_expected)) * 50 if skills_expected else 0

    # Keyword check
    keywords = ["education", "experience", "projects", "skills", "certifications"]
    kw_found = sum(1 for k in keywords if k in text)
    kw_score = (kw_found / len(keywords)) * 30  # up to 30 pts

    total = round(length_score + skills_score + kw_score, 2)
    if total > 100:
        total = 100.0
    
    breakdown = {
        "length_score": round(length_score,2),
        "skills_score": round(skills_score,2),
        "keyword_score": round(kw_score,2),
        "found_skills": found_skills,
        "total": total
    }
    return total, breakdown
