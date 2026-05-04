import sqlite3
import os

# This connects directly to the db and drops in some test jobs
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
db = sqlite3.connect(os.path.join(BASE_DIR, "instance", "linkedout.db"))

jobs = [
    ("Software Engineer", "Amazon", "Seattle, WA", 110000, 150000, "2026-05-03"),
    ("Frontend Developer", "Google", "Remote", 95000, 130000, "2026-05-15"),
    ("Data Analyst", "Microsoft", "Redmond, WA", 85000, 110000, "2026-04-20"),
    ("Backend Developer", "Stripe", "Remote", 120000, 160000, "2026-06-01"),
    ("DevOps Engineer", "Netflix", "Los Angles, CA", 130000, 170000, "2026-05-10"),
]

for title, company, location, salaryMin, salaryMax, expDate in jobs:
    db.execute("""
        INSERT INTO jobs (title, company, location, salary_min, salary_max, posted_at, expiration_date, status)
        VALUES (?, ?, ?, ?, ?, date('now'), ?, 'ACTIVE')
    """, (title, company, location, salaryMin, salaryMax, expDate))

db.commit()
db.close()

print("5 test jobs added successfully")