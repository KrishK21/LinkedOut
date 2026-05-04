import sqlite3
import os
from flask import g, current_app

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATABASE = os.path.join(BASE_DIR, "instance", "linkedout.db")

def get_db():
    """Open a new database connection"""
    if "db" not in g:
        db_path = current_app.config.get("DATABASE", DATABASE)
        g.db = sqlite3.connect(db_path)
        g.db.row_factory = sqlite3.Row
    return g.db

def close_db(e=None):
    """Close the database connection at end"""
    db = g.pop("db", None)
    if db is not None:
        db.close()

def init_db():
    """Create tables from schema.sql."""
    db = sqlite3.connect(DATABASE)
    with open(os.path.join(BASE_DIR, "schema.sql"), "r", encoding="utf-8") as f:
        db.executescript(f.read())
    db.close()

#This will create a table where we will be storing our job postings.
def init_job_table():
    db = sqlite3.connect(DATABASE)
    try:
        db.execute("""
            CREATE TABLE IF NOT EXISTS jobs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL, 
                company TEXT NOT NULL,
                location TEXT,
                salary_min INTEGER,
                salary_max INTEGER,
                posted_at TEXT NOT NULL DEFAULT (datetime('now')),
                expiration_date TEXT NOT NULL,
                status TEXT NOT NULL DEFAULT 'ACTIVE',
                posted_by INTEGER,
                applications TEXT DEFAULT '[]'
            )
        """)

 # This will help with making our job searching faster using indexes. 
        db.execute("CREATE INDEX IF NOT EXISTS idx_jobs_expiration ON jobs(expiration_date)")
        db.execute("CREATE INDEX IF NOT EXISTS idx_jobs_title ON jobs(title)")
        db.execute("CREATE INDEX IF NOT EXISTS idx_jobs_company ON jobs(company)")
        db.commit()
        print("Jobs table while init successfully")
    except Exception as e:
        print(f"Error while init jobs table: {e}")
    finally:
        db.close()
