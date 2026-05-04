from datetime import date, timedelta


class Job:
    def __init__(self, title, company, salaryMin, salaryMax, postedDate, expDate=None):
        if not title or not company:
            raise ValueError("Title/company are required")

        if salaryMin is None or salaryMax is None:
            raise ValueError("Salary range is missing")

        if salaryMin <= 0 or salaryMax <= 0:
            raise ValueError("Salary should be positive")

        if salaryMin > salaryMax:
            raise ValueError("Minimum salary cant go over max")

        if expDate is None:
            expDate = postedDate + timedelta(days=30)

        self.title = title
        self.company = company
        self.salaryMin = salaryMin
        self.salaryMax = salaryMax
        self.postedDate = postedDate
        self.expDate = expDate
        self.applications = []


def isActiveJob(job, currentDate):
    return currentDate <= job.expDate


def filterActiveJobs(jobs, currentDate):
    return [job for job in jobs if isActiveJob(job, currentDate)]


def jobSearch(jobs, keyword, currentDate):
    keyword = keyword.strip().lower()
    activeJobs = filterActiveJobs(jobs, currentDate)

    if keyword == "":
        return activeJobs

    results = []
    for job in activeJobs:
        if keyword in job.title.lower() or keyword in job.company.lower():
            results.append(job)

    return results


def applyJob(job, personEmail, currentDate):
    if not personEmail:
        raise ValueError("Applicant email required")

    if not isActiveJob(job, currentDate):
        return False

    if personEmail in job.applications:
        return False

    job.applications.append(personEmail)
    return True


def archivedExpJobs(jobs, currentDate):
    active = []
    archived = []

    for job in jobs:
        if isActiveJob(job, currentDate):
            active.append(job)
        else:
            archived.append(job)

    return active, archived