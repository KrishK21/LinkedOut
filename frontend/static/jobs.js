// Mustaph Mohamed
// This holds the Javascript code for our jobs page, and this is what makes our html code working
// Below are the sources utilized on this code.
// https://developer.mozilla.org/en-US/docs/Learn_web_development/Extensions/Client-side_APIs/Introduction - This helped with the use of api and how to integrate and call it in my code.
// https://www.geeksforgeeks.org/javascript/javascript-trigger-a-button-on-enter-key/ - The enter trigger on the search button function.
// https://www.themuse.com/developers/api/v2 - The API been utilized for getting real jobs.
// https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Date/toLocaleDateString - This was used on the displaying of the readable date from what we got from the api.

// This handles the tracking of our current state.
let currentPage = 1;
let currentCategory = "";
let currentLocation = "";
let currentLevel = "";
let totalPageCount = 1;
 
// This handles the getting of our DOM (Document Object Model) whenever we load into the jobs page.
// It helps us avoid only displaying text on that page and losing track on what has been loaded.
const jobsList = document.getElementById("jobsList");
const statusArea = document.getElementById("statusArea");
const loadMoreBtn = document.getElementById("loadMoreBtn");
const searchBtn = document.getElementById("searchBtn");
const categoryInput = document.getElementById("categoryInput");
const locationInput = document.getElementById("locationInput");
const levelInput = document.getElementById("levelInput");

// This handles the cleaning of our api's html into a clean preview in order to keep our page and it's elements sizing the same.
function cleanDescription(htmlString) {
    if (!htmlString) return "No description provided.";
    const temp = document.createElement("div");
    temp.innerHTML = htmlString;
    const text = temp.textContent || temp.innerText || "";
    const trimmed = text.trim().replace(/\s+/g, " ");
    return trimmed.length > 260 ? trimmed.slice(0, 260) + "..." : trimmed;
}
 
// This handles the formatting of our API's iso date format into something that is readable and are able to show on our page. 
function formatDate(isoString) {
    if (!isoString) return "";
    const d = new Date(isoString);
    if (isNaN(d.getTime())) return "";
    return d.toLocaleDateString(undefined, { year: "numeric", month: "short", day: "numeric" });
}


// This handles the building of a complete job card from the api.
function buildJobCard(job) {
    const card = document.createElement("article");
    card.className = "jobCard";
 
    const header = document.createElement("div");
    header.className = "jobCardHeader";
 
    const titleBlock = document.createElement("div");
    titleBlock.className = "jobCardTitle";
    const h2 = document.createElement("h2");
    h2.textContent = job.title;
    const company = document.createElement("div");
    company.className = "company";
    company.textContent = job.company;
    titleBlock.appendChild(h2);
    titleBlock.appendChild(company);
 
    const applyLink = document.createElement("a");
    applyLink.className = "applyBtn";
    applyLink.href = job.applyUrl;
    applyLink.target = "_blank";
    applyLink.rel = "noopener noreferrer";
    applyLink.textContent = "Apply";
    header.appendChild(titleBlock);
    header.appendChild(applyLink);
 
    const meta = document.createElement("div");
    meta.className = "jobMeta";
 
    const locSpan = document.createElement("span");
    locSpan.className = "location";
    locSpan.textContent = job.location;
    meta.appendChild(locSpan);
 
    if (job.category) {
        const catSpan = document.createElement("span");
        catSpan.textContent = job.category;
        meta.appendChild(catSpan);
    }
    if (job.level) {
        const lvlSpan = document.createElement("span");
        lvlSpan.textContent = job.level;
        meta.appendChild(lvlSpan);
    }
    const dateStr = formatDate(job.publishedAt);
    if (dateStr) {
        const dateSpan = document.createElement("span");
        dateSpan.className = "date";
        dateSpan.textContent = "Posted " + dateStr;
        meta.appendChild(dateSpan);
    }
 
    const desc = document.createElement("p");
    desc.className = "jobDescription";
    desc.textContent = cleanDescription(job.descriptionHtml);
    card.appendChild(header);
    card.appendChild(meta);
    card.appendChild(desc);
    return card;
}

// This handles the writing of the status message.
// This also allows us to color this message to let us know where we are passing or failing.
function setStatus(msg, isError = false) {
    statusArea.textContent = msg;
    statusArea.className = "statusArea" + (isError ? " error" : "");
}
 
// This handles the fetching of our jobs from the api from our flask backend. 
async function loadJobs(resetList = false) {
    if (resetList) {
        jobsList.innerHTML = "";
        currentPage = 1;
    }
    setStatus("Loading jobs...");
    loadMoreBtn.disabled = true;
 
    // This handles the building of our webpage that will be sent to the backend, and since we are supporting filtering, we also have to include thos filters. 
    // Since we can filter, our user may choose to use some of the filters and we have to take that into account so that when we send the request to our backend we don't error out.
    const params = new URLSearchParams();
    params.set("page", currentPage);
    if (currentCategory) params.set("category", currentCategory);
    if (currentLocation) params.set("location", currentLocation);
    if (currentLevel) params.set("level", currentLevel);
    try {
        const resp = await fetch("/jobs/api/jobs?" + params.toString());
        if (!resp.ok) {
            const errData = await resp.json().catch(() => ({}));
            throw new Error(errData.error || "Server returned " + resp.status);
        }
        const data = await resp.json();
        totalPageCount = data.pageCount || 1;
 
        if (!data.jobs || data.jobs.length === 0) {
            if (resetList) {
                setStatus(" Try different filter, No jobs found.");
            } else {
                setStatus("No more jobs to load.");
            }
            loadMoreBtn.style.display = "none";
            return;
        }
 
        data.jobs.forEach(job => jobsList.appendChild(buildJobCard(job)));
        setStatus("Showing page " + currentPage + " of " + totalPageCount + ".");
 
        // This handles the loading of pages, but only if there are pages available, if there are no more pages available we don't give the user the ability to load more. 
        if (currentPage < totalPageCount) {
            loadMoreBtn.style.display = "inline-block";
            loadMoreBtn.disabled = false;
        } else {
            loadMoreBtn.style.display = "none";
        }
    } catch (err) {
        setStatus("Unfortunately could not load jobs: " + err.message, true);
        loadMoreBtn.style.display = "none";
    }
}

// This handles the searching when a user searches, also we should keep in mind the filters the users used and we use them across all pages the user will load after. 
searchBtn.addEventListener("click", () => {
    currentCategory = categoryInput.value.trim();
    currentLocation = locationInput.value.trim();
    currentLevel = levelInput.value.trim();
    loadJobs(true);
});
 
// This is a feature I personally love having, which is when ever I type a filter for job search and press enter it should lead to the search rather than me havng to reach for the mouse evrytime and click on search.
// Since It is a function I personally like, I decided to make it part of the page.
[categoryInput, locationInput, levelInput].forEach(inp => {
    inp.addEventListener("keydown", e => {
        if (e.key === "Enter") searchBtn.click();
    });
});
 
// This handles keeping track and incrementing the page whenever the user loads a new page. 
loadMoreBtn.addEventListener("click", () => {
    currentPage += 1;
    loadJobs(false);
});
 
 // THis handles the initial load when we first open the page.
 loadJobs(true);
