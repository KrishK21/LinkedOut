// Mustaph Mohamed
// This is file with the javascript program to handle the connection of our frontend to the backend page.
// This also handles the creation of an account if we have a new user and login for users with account.
// Below are all the resources utiized in the making of this program.
// Javascript.info -  This helped in writing this javascript, anytime I didn't know how to implement something this website was useful in order to guide me on how to implement and how it works.
// Fetch, Async/Await, Dom munipulation, and events were influenced by this website. it was very instrumental in making me understand how all these connect and why they are used.
// Another tool utlized was also geeksforgeeks.org -  This website was my learning tool on the actual implementation of the js functions I am using here, it is what explained the functions and
// and the code in general in detail.
// Another tool utilized was the Flask.palletsprojects.com, this is all the flask documentation and this is where i got my information on flask, as I have rarely used Flask and prefer Springboot as I used that more often.
// FFlask documentation taught me how flask handles json requests and responses which were utilized in the login and signup functions.
// ANother tool utilized was https://developer.mozilla.org/en-US/ -  which is the mdn web docs and it was helpful as it was similiar to the javascript.info but just more detailed.
// ANother very helpful tool utilized was youtube especially the chanel FreeCodeCamp and especially this video. https://www.youtube.com/watch?v=yBDHkveJUf4

const BASE_URL = "http://127.0.0.1:5000";
// Use if we are running into port issues
// const BASE_URL = "";

document.addEventListener("DOMContentLoaded", () => {
  // This handles the grabbing of the elements we made in our html file and then storing them in a js variable to be used.
  const loginForm = document.getElementById("login-form");
  const signupForm = document.getElementById("signup-form");
  const showSignupLink = document.getElementById("show-signup");
  const showLoginLink = document.getElementById("show-login");
  const togglePwBtn = document.getElementById("toggle-pw");

  // This handles he switching from the login page to the sign up page for new users looking to create an account.
  showSignupLink.addEventListener("click", (e) => {
    // The listener is just there for when a new user clicks on the no account option.
    e.preventDefault();
    loginForm.style.display = "none";
    // This handles the hiding of the login page after we switch to the sign up page.
    signupForm.style.display = "flex";
    // This handles the creation and signing up of new users.
    clearErrors();
  });

  // This does the exact same thing as the function above but in reverse.
  // This is for when a user already has an account and they click on that option, they are taken to the login page.
  showLoginLink.addEventListener("click", (e) => {
    e.preventDefault();
    signupForm.style.display = "none";
    loginForm.style.display = "flex";
    clearErrors();
  });

  // This handles the logic of the toggle password button, so that users can see what they have typed ino the password box.
  togglePwBtn.addEventListener("click", () => {
    const pwInput = document.getElementById("password");
    const icon = togglePwBtn.querySelector("i");

    // If password is hidden then it switches to the visible mode.
    if (pwInput.type === "password") {
      pwInput.type = "text";
      icon.className = "ph ph-eye-slash";
    } else {
      // If password is visible then it switches to the hidden mode.
      pwInput.type = "password";
      icon.className = "ph ph-eye";
      // This is using the css class i made in my html file that we imported from the library called phosphor icon.
    }
  });

  // This section is a helpful function i made so that when ever something goes wrong, the erros is shown and also clears it.
  function showError(elementId, message, isSuccess = false) {
    // This will find the error id.
    const el = document.getElementById(elementId);
    if (!el) return;
    el.textContent = message;
    el.style.display = "block";
    el.style.color = isSuccess ? "#4ade80" : "var(--danger)";
    // TThis is color coded for better visibility and recognizing of the error, green for success and red for not passing and error.
  }

  // This function is also a helper and used multiple times.
  // This will clear and reset the error messages we get.
  // I am using this functiom when switching from the login to signup page and vice versa and also when we start a new submission every time.
  function clearErrors() {
    [
      "username-error",
      "pw-error",
      "new-username-error",
      "new-pw-error",
    ].forEach((id) => {
      const el = document.getElementById(id);
      if (el) {
        el.textContent = "";
        el.style.display = "none";
      }
    });
  }

  // This function works with the showerror function, if we have error the color red is displayed if not we reset.
  function highlightInput(inputEl, hasError) {
    inputEl.style.borderColor = hasError ? "var(--danger)" : "";
  }

  // This is a visual clue i made for the user to make them see something is happening when a fetch request is made
  // I basically made a spinner to tell users something is happening, in the case the fetch takes longer than expeced.
  function setLoading(btn, isLoading) {
    isLoading ? btn.classList.add("loading") : btn.classList.remove("loading");
  }

  // This function handles the showcassing of the success of login in or signing up of new users.
  // IIt is called in both the lgin and sign up functions with messages displayed depending on which.
  function setSuccess(btn, message) {
    btn.classList.remove("loading");
    btn.style.background = "#22c55e";
    btn.innerHTML = `<span class="btn-text" style="display:block">
      <i class="ph ph-check-circle" style="vertical-align:middle; font-size:20px; margin-right:6px;"></i>
      ${message}
    </span>`;
  }

  // In he case a sign up or login fails, the button resets allowing the user to try again.
  function resetBtn(btn, label) {
    btn.style.background = "";
    btn.innerHTML = `<span class="btn-text">${label}</span><i class="ph ph-spinner-gap spinner"></i>`;
  }

  // This function handles all the login form for users that already have accounts to our web page.
  loginForm.addEventListener("submit", async (e) => {
    e.preventDefault();
    clearErrors();
    // This handles the clearing of all prevoious error before letting user try to login.

    // This handles the grabbing of the elements and their value, also it removes any unnecesary white spaces.
    const usernameEl = document.getElementById("username");
    const passwordEl = document.getElementById("password");
    const username = usernameEl.value.trim();
    const password = passwordEl.value.trim();

    // This handles the client Client-side validation, it makes sure all required fields are filled before sending the request to flask.
    let hasError = false;
    if (!username) {
      showError("username-error", "Username is required.");
      highlightInput(usernameEl, true);
      hasError = true;
    }
    if (!password) {
      showError("pw-error", "Password is required.");
      highlightInput(passwordEl, true);
      hasError = true;
    }
    if (hasError) return;
    // If any required field isn't filled then we stop and don't end a request to the backend until those required fills are filled in.

    const btn = document.getElementById("login-btn");
    setLoading(btn, true);
    // This is the visual clue i was talking about, it is a spinner that shows up when a request is sent and a response is been waited for.

    try {
      // This handles the sending of the username and the password to the backend.
      const response = await fetch(`${BASE_URL}/login`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ username, password }),
      });

      const data = await response.json();

      if (response.ok) {
        // If the credentials sent to the backend is correct we make sure to save and log the user in.
        localStorage.setItem("user_id", data.user_id);
        localStorage.setItem("username", data.username);
        setSuccess(btn, "Welcome back!!!");
        setTimeout(() => {
          window.location.href = "/home";
        }, 1500);
        // This handles the redicrection of the user
      } else {
        // If any of the credentials sent to the backend is wrong we return an error, wrong password or user not found.
        resetBtn(btn, "Sign In");
        showError("pw-error", data.error || "wrong credentials.");
        highlightInput(passwordEl, true);
      }
    } catch (err) {
      // This handles the case where the flask isn't running at all and there is an error we have to check in order to get the flask running and processing info.
      resetBtn(btn, "Sign In");
      showError(
        "pw-error",
        "Not able to reach the server. Are you sure Flask is connected and running?",
      );
    }
  });

  // This function handles the sign up form for new users creating an account in order to user our appplication.
  // This function is similiar to the login function and does mostly the same thing, and it just makes sure new users are able to create an account.
  signupForm.addEventListener("submit", async (e) => {
    e.preventDefault();
    clearErrors();
    // This handles the clearing of all prevoious error before letting user try to sign up.

    // This handles the grabbing of the elements and their value, also it removes any unnecesary white spaces.
    const usernameEl = document.getElementById("new-username");
    const passwordEl = document.getElementById("new-password");
    const username = usernameEl.value.trim();
    const password = passwordEl.value.trim();

    // This handles the client Client-side validation, it makes sure all required fields are filled before sending the request to flask.
    let hasError = false;
    if (!username) {
      showError(
        "new-username-error",
        "Username is required in order to make an account.",
      );
      highlightInput(usernameEl, true);
      hasError = true;
    }
    if (password.length < 6) {
      showError(
        "new-pw-error",
        "Password must be at least 6 characters for your safety.",
      );
      highlightInput(passwordEl, true);
      hasError = true;
    }
    if (hasError) return;

    const btn = document.getElementById("signup-btn");
    setLoading(btn, true);
    // This is the visual clue i was talking about, it is a spinner that shows up when a request is sent and a response is been waited for.

    try {
      // This handles the sending of the username and the password to the backend.
      const response = await fetch(`${BASE_URL}/signup`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ username, password }),
      });

      const data = await response.json();

      if (response.ok) {
        // This handles the display of a successfully created account and tells the new user to go back and now login into their new account.
        setSuccess(btn, "Account Created!!!");
        setTimeout(() => {
          signupForm.style.display = "none";
          // This will hide the sign up form and take the user to the login page in order to get them to login into their new account.
          loginForm.style.display = "flex";
          resetBtn(document.getElementById("login-btn"), "Sign In");
          document.getElementById("username").value = username;
          showError(
            "username-error",
            "Account created Successfully! Please sign in.",
            true,
          );
        }, 1500);
      } else {
        // If username is taken we return an error telling the user such.
        resetBtn(btn, "Create Account");
        showError(
          "new-username-error",
          data.error || "Error! Could not create an account.",
        );
        highlightInput(usernameEl, true);
      }
    } catch (err) {
      // This handles the case where our flask ins't connecting to the frontend page.
      resetBtn(btn, "Create Account");
      showError(
        "new-pw-error",
        "Not able to reach the server. Are you sure Flask is connected and running?",
      );
    }
  });
});
