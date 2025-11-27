import matplotlib.pyplot as plt
import numpy as np

def plot_skill_gap(all_job_skills, candidate_skills):
    skills = all_job_skills
    have = [1 if s in candidate_skills else 0 for s in skills]
    missing = [1 - h for h in have]

    fig, ax = plt.subplots(figsize=(6, max(1, len(skills)*0.4)))
    y = np.arange(len(skills))

    ax.barh(y, have, color='green', label='Have')
    ax.barh(y, missing, left=have, color='red', label='Missing')

    ax.set_yticks(y)
    ax.set_yticklabels(skills)
    ax.set_xlim(0,1)
    ax.set_xlabel("Skill Match")
    ax.set_title("Skill Gap Heatmap")
    ax.legend()

    plt.tight_layout()
    return fig
