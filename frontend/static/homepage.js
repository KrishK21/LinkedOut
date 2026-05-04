// mustaph Mohamed
// Javascript code for our homepage.
// Citations down below.
// The fade anim ations and hover effects are from, https://javascript.info/js-animation. This is where the inspo came from.
// The delayed animation inspo using the setTimeOut are from, https://developer.mozilla.org/en-US/docs/Web/API/Window/setTimeout
// ALso from, https://www.w3schools.com/jsref/met_win_setTimeout.asp
// https://developer.mozilla.org/en-US/docs/Web/API/Storage/getItem

document.addEventListener("DOMContentLoaded", () => {
  // This handles the case where a user isn't logged in, in which they are sent back to the log in page to log in or create an account.
  if (!localStorage.getItem("user_id")) {
    window.location.href = "/";
  }

  // When the user is logged in, we grab their data and store in a variable to be used later.
  const username = localStorage.getItem("username") || "User";

  // Once the user logs in and their data is pulled, their username is displayed on the page.
  document.getElementById("nav-username").textContent = username;
  document.getElementById("banner-username").textContent = username;

  // This is the data that is displayed on the homepage, since we have no real users yet, the data is hardcoded to show how the function works.
  // If we were to have real users then this would be pulling live data from a database.
  const mockUserData = {
    stats: {
      all: {
        applied: { count: 32, recent: "Software Engineer at Google" },
        interviews: { count: 4, recent: "Frontend Dev at Meta" },
        offers: { count: 1, recent: "Web Dev at Amazon ($115k)" },
      },
      month: {
        applied: { count: 12, recent: "Software Engineer at Google" },
        interviews: { count: 1, recent: "Frontend Dev at Meta" },
        offers: { count: 0, recent: "—" },
      },
      week: {
        applied: { count: 3, recent: "Data Analyst at Netflix" },
        interviews: { count: 0, recent: "—" },
        offers: { count: 0, recent: "—" },
      },
      three: {
        applied: { count: 25, recent: "Backend Engineer at Spotify" },
        interviews: { count: 3, recent: "Full Stack at Stripe" },
        offers: { count: 1, recent: "Web Dev at Amazon ($115k)" },
      },
    },
  };

  // This function handles our dropdiwn menu, which has the settings and the log out function
  const avatarBtn = document.getElementById("avatar-btn");
  const avatarMenu = document.getElementById("avatar-menu");
  avatarBtn.addEventListener("click", (e) => {
    e.stopPropagation();
    avatarMenu.classList.toggle("open");
  });

  // When the user clicks anywhere else on our page while they have the drop down menu they close the drop down menu
  document.addEventListener("click", (e) => {
    if (!avatarMenu.contains(e.target)) {
      avatarMenu.classList.remove("open");
    }
  });

  const filterBtns = document.querySelectorAll(".filter-btn");
  const trackerGrid = document.querySelector(".tracker-grid");

  // This handles the animation of our tracker.
  trackerGrid.style.transition = "opacity 0.2s ease-in-out";
  const updateTrackerData = (timeframe) => {
    const data = mockUserData.stats[timeframe];
    trackerGrid.style.opacity = "0";
    setTimeout(() => {
      // This is how we put our hardcoded data onto our website tracker cards.
      document.getElementById("count-applied").textContent = data.applied.count;
      document.getElementById("recent-applied").textContent =
        data.applied.recent;
      document.getElementById("count-interviews").textContent =
        data.interviews.count;
      document.getElementById("recent-interviews").textContent =
        data.interviews.recent;
      document.getElementById("count-offers").textContent = data.offers.count;
      document.getElementById("recent-offers").textContent = data.offers.recent;
      trackerGrid.style.opacity = "1";
    }, 200);
  };

  // This handles the filter buttons and puts a listening tracker on each card.
  // It also handles the animation and the color shifting on the cards when they are clicked on.
  filterBtns.forEach((btn) => {
    btn.addEventListener("click", (e) => {
      filterBtns.forEach((b) => b.classList.remove("active"));
      e.target.classList.add("active");

      // This handles the fetching of the data of the card clicked on.
      const filterType = e.target.getAttribute("data-filter");
      updateTrackerData(filterType);
    });
  });

  updateTrackerData("all");

  // This handles the logout button, when clicked it logs the user out and sends the user back to login.
  document.getElementById("logout-btn").addEventListener("click", (e) => {
    e.preventDefault();
    localStorage.clear();
    window.location.href = "/";
  });
});
