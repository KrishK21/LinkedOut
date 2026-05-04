# LinkedOut

> Cut The Chase. Find The Job.

LinkedOut is a full stack job board web application built to solve the ghost job problem on platforms like LinkedIn. Every job listing has a required expiration date and salary range, keeping the platform clean, transparent, and honest. No social feeds, no likes, no endorsements — just jobs.

---

## The Problem

LinkedIn and similar platforms are plagued with:
- **Ghost jobs** — listings that are expired or were never meant to be filled
- **Hidden salaries** — job posts with no compensation info leaving candidates in the dark
- **Social clutter** — feeds, endorsements, and engagement metrics that get in the way of actually finding a job

LinkedOut strips all of that away.

---

## Features

- **Job Expiration System** — every job automatically expires after 30 days. Expired listings are hidden from all search results and direct links without anyone having to manually delete anything
- **Salary Transparency** — employers are required to enter a salary range before a job can be published. No exceptions
- **Job Search** — search active listings by keyword and location. Expired jobs never appear in results
- **User Authentication** — secure signup and login with hashed passwords
- **Profile Page** — users can set their name, bio, add skills, log experience, and upload a resume
- **Resume Upload** — supports PDF, DOC, and DOCX file uploads stored securely on the server

---

## Tech Stack

**Backend**
- Python 3
- Flask
- SQLite
- Werkzeug

**Frontend**
- HTML
- CSS
- Vanilla JavaScript
- Phosphor Icons

---

## Project Structure

```
LinkedOut/
├── backend/
│   ├── auth.py          # login, signup, profile routes
│   ├── jobs.py          # job listing routes (Blueprint)
│   ├── job.py           # Job class and core logic
│   ├── web.py           # main Flask app entry point
│   ├── db.py            # database connection
│   ├── schema.sql       # database schema
│   ├── seed.py          # adds test job listings
│   └── testJobs.py      # unit and integration tests
├── frontend/
│   ├── templates/
│   │   ├── index.html        # login page
│   │   ├── homepage.html     # home dashboard
│   │   ├── jobs.html         # browse jobs page
│   │   └── Profilepage.html  # user profile page
│   └── static/
│       ├── style.css
│       ├── homepage.css
│       ├── homepage.js
│       ├── jobs.css
│       ├── jobs.js
│       ├── Profilepage.css
│       └── Profilepage.js
└── requirements.txt
```

---

## Getting Started

### Prerequisites
- Python 3.10+
- pip

### Installation

**1. Clone the repo**
```bash
git clone https://github.com/Mustaph7/LinkedOut.git
cd LinkedOut
```

**2. Create and activate a virtual environment**

Mac/Linux:
```bash
python3 -m venv .venv
source .venv/bin/activate
```

Windows:
```bash
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

**3. Install dependencies**
```bash
pip install -r requirements.txt
```

**4. Run the app**
```bash
cd backend
python web.py
```

**5. Open your browser and go to**
```
http://127.0.0.1:5000
```

### Seed the database with test jobs (optional)
```bash
cd backend
python seed.py
```

---

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/signup` | Create a new account |
| POST | `/login` | Login to existing account |
| GET/POST | `/profile` | Get or update user profile |
| POST | `/jobs/create` | Create a new job listing |
| GET | `/jobs/` | List all active jobs |
| GET | `/jobs/search?q=keyword` | Search active jobs by keyword |
| GET | `/jobs/<id>` | Get a single job by ID |
| GET | `/jobs/browse` | Browse jobs page |

---

## Running Tests

```bash
cd backend
pytest testJobs.py
```

The test suite includes:
- Black box tests for job creation and validation
- White box tests for branch coverage on `applyJob`
- Integration tests for search filtering and archiving

---

## Team

| Name | GitHub | Role |
|------|--------|------|
| Krish Kanda | [@KrishK21](https://github.com/KrishK21) | Backend — job expiration logic, API routes, profile page |
| Mustaph Mohamed | [@Mustaph7](https://github.com/Mustaph7) | Frontend — UI design, homepage, job browsing page |

---

## Course

**CS 320 — Introduction to Software Engineering**
Semester Long Project — Spring 2026

---

## License

MIT License

Copyright (c) 2026 Krish Kanda and Mustaph Mohamed

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.