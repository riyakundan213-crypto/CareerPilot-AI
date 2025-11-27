def generate_cover_letter(name, role, company, resume_text, skills):
    top_skills = ", ".join(skills[:3]) if skills else "key skills"

    text_excerpt = resume_text[:250].replace("\n", " ") if resume_text else ""

    letter = f"""
Dear Hiring Manager at {company},

My name is {name}, and I am excited to apply for the position of {role} at your organization.
With hands-on experience in areas such as {top_skills}, I believe I can make a strong contribution to your team.

My background includes:

- Practical experience with the skills mentioned above
- A strong passion for continuous learning and problem-solving
- The ability to work in both team-based and independent environments

Below is a short summary from my experience:
\"\"\"{text_excerpt}...\"\"\"

I would be grateful for an opportunity to discuss how my skills align with the role at {company}.
Thank you for considering my application.

Sincerely,  
{name}
"""
    return letter
