from flask import Blueprint, request, jsonify, render_template
from datetime import date, timedelta
from db import get_db
import urllib.request
import urllib.parse
import json

jobs_bp = Blueprint("jobs", __name__)


@jobs_bp.route("/create", methods=["POST"])
def createJob():
    data = request.get_json() or {}
    title = data.get("title", "").strip()
    company = data.get("company", "").strip()

    if not title or not company:
        return jsonify({"error": "title and company are required"}), 400

    # This makes sure the employer actually put in a salary range before posting
    salaryMin = data.get("salary_min")
    salaryMax = data.get("salary_max")

    if salaryMin is None or salaryMax is None:
        return jsonify({"error": "salary_min and salary_max are required"}), 400

    try:
        salaryMin = int(salaryMin)
        salaryMax = int(salaryMax)
    except (ValueError, TypeError):
        return jsonify({"error": "salary_min and salary_max must be integers"}), 400

    if salaryMin <= 0 or salaryMax <= 0:
        return jsonify({"error": "Salary values must be positive"}), 400

    if salaryMin > salaryMax:
        return jsonify({"error": "salary_min cant go over salary_max"}), 400

    # This handles the expiration date, defaults to 30 days from today if not given
    today = date.today()
    rawExp = data.get("expiration_date")

    if rawExp:
        try:
            expDate = date.fromisoformat(rawExp)
        except ValueError:
            return jsonify({"error": "expiration_date must be YYYY-MM-DD format"}), 400
        if expDate <= today:
            return jsonify({"error": "expiration_date must be in the future"}), 400
    else:
        expDate = today + timedelta(days=30)

    location = data.get("location", "").strip() or None
    postedBy = data.get("posted_by")

    try:
        db = get_db()

        # This creates the jobs table if it doesnt exist yet
        db.execute("""
            CREATE TABLE IF NOT EXISTS jobs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                company TEXT NOT NULL,
                location TEXT,
                salary_min INTEGER NOT NULL,
                salary_max INTEGER NOT NULL,
                posted_at TEXT NOT NULL DEFAULT (date('now')),
                expiration_date TEXT NOT NULL,
                status TEXT NOT NULL DEFAULT 'ACTIVE',
                posted_by INTEGER,
                applications TEXT DEFAULT '[]'
            )
        """)
        db.execute("CREATE INDEX IF NOT EXISTS idx_jobs_expiration ON jobs(expiration_date)")
        db.execute("CREATE INDEX IF NOT EXISTS idx_jobs_title ON jobs(title)")
        db.execute("CREATE INDEX IF NOT EXISTS idx_jobs_company ON jobs(company)")

        cursor = db.execute("""
            INSERT INTO jobs
                (title, company, location, salary_min, salary_max, posted_at, expiration_date, status, posted_by)
            VALUES (?, ?, ?, ?, ?, ?, ?, 'ACTIVE', ?)
        """, (title, company, location, salaryMin, salaryMax, today.isoformat(), expDate.isoformat(), postedBy))

        db.commit()
        return jsonify({"message": "Job listing created!", "job_id": cursor.lastrowid, "expiration_date": expDate.isoformat()}), 201

    except Exception as e:
        return jsonify({"error": f"Error while creating job: {str(e)}"}), 500


@jobs_bp.route("/search", methods=["GET"])
def searchJobs():
    keyword = request.args.get("q", "").strip().lower()
    location = request.args.get("location", "").strip().lower()
    today = date.today().isoformat()

    try:
        db = get_db()

        # This only pulls jobs where the expiration date hasnt passed yet, so expired ones stay hidden
        query = "SELECT * FROM jobs WHERE expiration_date >= ?"
        params = [today]

        if keyword:
            query += " AND (LOWER(title) LIKE ? OR LOWER(company) LIKE ?)"
            like = f"%{keyword}%"
            params += [like, like]

        if location:
            query += " AND LOWER(location) LIKE ?"
            params += [f"%{location}%"]

        query += " ORDER BY posted_at DESC"

        rows = db.execute(query, params).fetchall()
        jobs = [dict(r) for r in rows]

        return jsonify({"count": len(jobs), "jobs": jobs}), 200

    except Exception as e:
        return jsonify({"error": f"Error while searching jobs: {str(e)}"}), 500


@jobs_bp.route("/", methods=["GET"])
def listJobs():
    today = date.today().isoformat()

    try:
        db = get_db()

        # This grabs all active jobs expired ones are automatically excluded
        rows = db.execute(
            "SELECT * FROM jobs WHERE expiration_date >= ? ORDER BY posted_at DESC",
            (today,)
        ).fetchall()

        jobs = [dict(r) for r in rows]
        return jsonify({"count": len(jobs), "jobs": jobs}), 200

    except Exception as e:
        return jsonify({"error": f"Error while getting jobs: {str(e)}"}), 500


@jobs_bp.route("/<int:jobId>", methods=["GET"])
def getJob(jobId):
    today = date.today().isoformat()

    try:
        db = get_db()
        row = db.execute("SELECT * FROM jobs WHERE id = ?", (jobId,)).fetchone()

        if not row:
            return jsonify({"error": "Job not found"}), 404

        job = dict(row)

        # This checks if the job is expired and hides it from the user if it is
        if job["expiration_date"] < today:
            return jsonify({"error": "This job listing has expired"}), 404

        return jsonify(job), 200

    except Exception as e:
        return jsonify({"error": f"Error while getting job: {str(e)}"}), 500

@jobs_bp.route("/browse", methods=["GET"])
def browseJobs():
    return render_template("jobs.html")



# For this project, We have decided to use an API that allows us to have real jobs on our webpage where users can apply to those jobs.
# Muse API allows us to use their technology without the need of us registrying our application, and they allow upto 500 request an hour.
# Since it is free for us to use this API we have no need for a key, therefore we don't need to have a code that considers and looks for a key.
MUSE_API_URL = "https://www.themuse.com/api/public/jobs"

@jobs_bp.route("/api/jobs", methods=["GET"])
def apiJobs():
    # This handles when a user filters their job search in the search bar. 
    page     = request.args.get("page",     "1")
    category = request.args.get("category", "").strip()
    location = request.args.get("location", "").strip()
    level    = request.args.get("level",    "").strip()

    # We always send page and sort order, then only add filters if the user actually typed something.
    # This way we don't send empty strings to the Muse API and get weird results back.
    params = {"page": page, "descending": "true"}
    if category: params["category"] = category
    if location: params["location"] = location
    if level:    params["level"]    = level

    try:
        # We have to take the filters the users types in, plus the page number and then we make a full functioning URL and send our request to our API.
        url = MUSE_API_URL + "?" + urllib.parse.urlencode(params)
        # This is what tells the API to send back a json, if we didn't have this, the APi might send us data we can't read.
        req = urllib.request.Request(url, headers={
            "Accept": "application/json",
            "User-Agent": "Mozilla/5.0"
        })
        # Once we send the request we wait for 10 seconds to get a response back.
        # The 10 second is the worst case scenerio, and this timeout makes sure we don't hang forever waiting for a response if the API is down
        with urllib.request.urlopen(req, timeout=10) as resp:
            # Once we get a response back we decode it from bytes into strings and then parse it.
            raw = json.loads(resp.read().decode())

        # We create an empty list in order to fill it with the jobs data we get from the API
        jobs = []
        # The job data sent back by the API is under a result, therefore we have to loop through all the jobs one by one.
        # In the case we get empty data we use an empty list in order not to crush our webpage.
        for job in raw.get("results", []):
            jobs.append({
                "title":           job.get("name", "Untitled"),
                "company":         job.get("company", {}).get("name", "Unknown Company"),
                "location":        job["locations"][0]["name"] if job.get("locations") else "Remote / Not specified",
                "category":        job["categories"][0]["name"] if job.get("categories") else "",
                "level":           job["levels"][0]["short_name"] if job.get("levels") else "",
                "publishedAt":     job.get("publication_date", ""),
                "descriptionHtml": job.get("contents", ""),
                "applyUrl":        job.get("refs", {}).get("landing_page", "#"),
            })

        # Once we have looped through all the jobs we got back and build a clean list and then send it back to be viewed by the user. 
        # We also send back the page count, in order to be able to show the load more jobs button or to hide it if we don't have anymore jobs to load.
        return jsonify({
            "jobs":      jobs,
            "pageCount": raw.get("page_count", 1),
            "total":     raw.get("count", 0),
        }), 200 # if we get the 200, then we know everything well.

    except Exception as e:
        # If the Muse API is down or something goes wrong we let the frontend know and then timeout rather than freezing and waiting on a white page.
        # We send a 500 error code, and that is displayed on the jobs tab to let the user know.
        return jsonify({"error": f"Could not reach The Muse API: {str(e)}"}), 500
