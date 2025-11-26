course_links = {
    "sql": [
        ("YouTube", "https://youtu.be/HXV3zeQKqGY")
    ],
    "power bi": [
        ("YouTube", "https://youtu.be/_-08VWQZ_cQ")
    ],
    "python": [
        ("YouTube", "https://youtu.be/_uQrJ0TkZlc")
    ],
    "excel": [
        ("YouTube", "https://youtu.be/8lXerJ0BB94")
    ],
    "communication": [
        ("YouTube", "https://youtu.be/1m0FYH8ZkkI")
    ],
    "content writing": [
        ("YouTube", "https://youtu.be/OnZ88om1eig")
    ]
}

def show_recommendation(top_job):
    out = top_job.copy()
    courses = {}

    for skill in top_job["Skills Missing"]:
        skill_lower = skill.lower()
        if skill_lower in course_links:
            courses[skill_lower] = course_links[skill_lower]
        else:
            courses[skill_lower] = []

    out["Courses"] = courses
    return out
