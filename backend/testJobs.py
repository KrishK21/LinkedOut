# Krish Kanda, I went through and created job.py which holds all my functions that I wanted to use for test
# Each funciton has what is is and how I am testing it with its required tests.
# This file does contain more then 12 assertions just to be safe

import pytest
from datetime import date, timedelta

# Import my jobs that I created for testing
from backend.job import Job, isActiveJob, filterActiveJobs, jobSearch, applyJob, archivedExpJobs


# black box unit test: The point of this test is to treat jobs creation like a black box and checks the externally visable
# requirements tied to the cool cam:
# default expiration date is 30 days after posting
# salary range is required
# salary values must be positive
# minimum salary cannot exceed maximum
def testJobCreationBlackBox():
    posted = date(2026, 2, 20)

    job = Job("Software Engineer", "Amaon", 80000, 120000, posted)

    assert job.title == "Software Engineer"
    assert job.company == "Amaon"
    assert job.salaryMin == 80000
    assert job.salaryMax == 120000
    assert job.expDate == posted + timedelta(days=30)

    with pytest.raises(ValueError):
        Job("Analyst", "DataCorp", None, 90000, posted)

    with pytest.raises(ValueError):
        Job("Analyst", "DataCorp", 50000, None, posted)

    with pytest.raises(ValueError):
        Job("Analyst", "DataCorp", -1, 90000, posted)

    with pytest.raises(ValueError):
        Job("Analyst", "DataCorp", 100000, 90000, posted)


# white box unit test
# Coverage type 100% branch coverage of applyJob
#
# Function under test:
# def applyJob(job, personEmail, currentDate):
#     if not personEmail:
#         raise ValueError("Applicant email required")
#
#     if not isActiveJob(job, currentDate):
#         return False
#
#     if personEmail in job.applications:
#         return False
#
#     job.applications.append(personEmail)
#     return True
#
# branches covered in this test:
# missing email will raise ValueError
# expired job will return false
# duplicate applicant will return false
# valid application will return tru
def testapplyJobWhiteBox():
    posted = date(2026, 2, 20)

    activeJob = Job("Backend Developer", "CloudCore", 90000, 130000, posted)
    expJobs = Job(
        "Old Listing",
        "GhostCorp",
        70000,
        85000,
        posted,
        date(2026, 2, 21)
    )

    current = date(2026, 2, 25)
    afterExp = date(2026, 2, 22)

    with pytest.raises(ValueError):
        applyJob(activeJob, "", current)

    assert applyJob(expJobs, "person@example.com", afterExp) is False

    assert applyJob(activeJob, "person@example.com", current) is True
    assert "person@example.com" in activeJob.applications

    assert applyJob(activeJob, "person@example.com", current) is False


# integration test
# Units being tested together are jobSearch and filterActiveJobs
# This test makes sure that searching depends on the active job filter and that
# expired jobs are automatically hidden from candidate search results
def testJobSearchFilter():
    posted = date(2026, 2, 20)
    current = date(2026, 2, 25)

    jobs = [
        Job("Frontend Developer", "PixelForge", 75000, 95000, posted),
        Job("Backend Developer", "CloudCore", 90000, 130000, posted),
        Job("Data Analyst", "Insight Labs", 70000, 90000, posted),
        Job("Software Engineer", "GhostTech", 85000, 110000, posted, date(2026, 2, 21)),
    ]

    activeJobs = filterActiveJobs(jobs, current)
    searchResults = jobSearch(jobs, "developer", current)
    allSeenResults = jobSearch(jobs, "", current)

    assert len(activeJobs) == 3
    assert all(isActiveJob(job, current) for job in activeJobs)

    assert len(searchResults) == 2
    assert searchResults[0].title == "Frontend Developer"
    assert searchResults[1].title == "Backend Developer"

    assert len(allSeenResults) == 3
    assert all(job.company != "GhostTech" for job in allSeenResults)


# integration test
# Units being tested together: archivedExpJobs and isActiveJob
# This test verifies that expired jobs are separated from active jobs correctly.
def testArchiveJobs():
    posted = date(2026, 2, 20)
    current = date(2026, 2, 25)

    activeJob1 = Job("Software Engineer", "Amaon", 80000, 120000, posted)
    activeJob2 = Job("QA Engineer", "BugTrack", 70000, 95000, posted)
    expJobs1 = Job("Old Analyst Role", "ArchiveOne", 65000, 85000, posted, date(2026, 2, 21))
    expJobs2 = Job("Expired Dev Role", "ArchiveTwo", 90000, 110000, posted, date(2026, 2, 24))

    jobs = [activeJob1, activeJob2, expJobs1, expJobs2]

    active, archived = archivedExpJobs(jobs, current)

    assert len(active) == 2
    assert len(archived) == 2
    assert all(isActiveJob(job, current) for job in active)
    assert all(not isActiveJob(job, current) for job in archived)