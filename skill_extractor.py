import re

skills_list = [
    "python","java","sql","excel","power bi","tableau","machine learning","deep learning",
    "nlp","data analysis","data visualization","statistics","r","html","css","javascript",
    "django","flask","react","node","communication","leadership","problem solving","canva",
    "ms office","content writing","graphic designing"
]

def extract_skills(resume_text):
    resume_text = resume_text.lower()
    found = []
    for skill in skills_list:
        pattern = r"\b" + re.escape(skill) + r"\b"
        if re.search(pattern, resume_text):
            found.append(skill)
    return sorted(list(set(found)))
