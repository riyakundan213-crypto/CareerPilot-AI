import sqlite3

DB_NAME = "careerpilot.db"

def init_db():
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()
    
    cur.execute("""
    CREATE TABLE IF NOT EXISTS resumes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        email TEXT,
        resume_text TEXT,
        skills TEXT,
        top_job TEXT,
        ats_score REAL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)
    
    conn.commit()
    conn.close()

def save_resume(name, email, resume_text, skills, top_job, ats_score):
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()

    cur.execute("""
        INSERT INTO resumes (name, email, resume_text, skills, top_job, ats_score)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (name, email, resume_text, ",".join(skills), top_job, ats_score))

    conn.commit()
    conn.close()
