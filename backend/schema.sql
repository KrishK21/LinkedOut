CREATE TABLE IF NOT EXISTS jobs (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  title TEXT NOT NULL,
  company TEXT NOT NULL,
  location TEXT,
  salary_min INTEGER,
  salary_max INTEGER,
  posted_at TEXT NOT NULL DEFAULT (datetime('now')),
  expiration_date TEXT NOT NULL,
  status TEXT NOT NULL DEFAULT 'ACTIVE'
);

CREATE INDEX IF NOT EXISTS idx_jobs_expiration ON jobs(expiration_date);
CREATE INDEX IF NOT EXISTS idx_jobs_title ON jobs(title);