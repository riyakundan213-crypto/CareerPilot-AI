import pandas as pd

def load_jobs(path="jobs.csv"):
    return pd.read_csv(path)

def match_jobs(candidate_skills, jobs_df=None, jobs_path="jobs.csv"):
    if jobs_df is None:
        jobs_df = load_jobs(jobs_path)

    results = []
    candidate_skills = set([s.lower().strip() for s in candidate_skills])
    
    for _, row in jobs_df.iterrows():
        job_skills = [s.strip().lower() for s in row["Required Skills"].split(",")]
        matched = candidate_skills & set(job_skills)
        
        score = (len(matched) / len(job_skills)) * 100 if len(job_skills) else 0
        
        results.append({
            "Job Role": row["Job Role"],
            "Match Score (%)": round(score, 2),
            "Skills Matched": sorted(list(matched)),
            "Skills Missing": sorted(list(set(job_skills) - candidate_skills)),
            "Salary Range": row["Salary Range"],
            "Experience": row["Experience"],
            "Job Description": row["Job Description"]
        })

    # Highest match score first
    return sorted(results, key=lambda x: x["Match Score (%)"], reverse=True)
