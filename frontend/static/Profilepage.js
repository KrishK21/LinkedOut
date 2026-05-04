// Krish Kanda
// This handles all the profile page logic, loading data, editing, skills and experience.

document.addEventListener("DOMContentLoaded", () => {
  // This checks if the user is logged in, if not sends them back to login.
  const userId = localStorage.getItem("user_id");
  const username = localStorage.getItem("username");

  if (!userId) {
    window.location.href = "/";
  }

  // This puts the username on the page right away from localStorage.
  document.getElementById("display-username").textContent = "@" + username;
  document.getElementById("display-name").textContent = username;

  // This loads the skills and experience from localStorage so they persist on refresh.
  let skills = JSON.parse(localStorage.getItem("skills")) || [];
  let experience = JSON.parse(localStorage.getItem("experience")) || [];

  // This tries to load the saved profile name and bio from the backend.
  fetch("/profile?user_id=" + userId)
    .then((res) => res.json())
    .then((data) => {
      if (data.name) {
        document.getElementById("display-name").textContent = data.name;
      }
      if (data.bio) {
        document.getElementById("display-bio").textContent = data.bio;
      }
      if (data.resume) {
        showResume(data.resume);
      }
    })
    .catch((err) => {
      // This just means no profile saved yet, thats fine.
      console.log("No profile found yet", err);
    });

  // This handles the edit button toggling the edit form.
  document.getElementById("toggle-edit-btn").addEventListener("click", () => {
    const form = document.getElementById("edit-form");
    if (form.style.display === "none") {
      form.style.display = "block";
      // This pre fills the inputs with whatever is already showing.
      document.getElementById("input-name").value =
        document.getElementById("display-name").textContent;
      document.getElementById("input-bio").value =
        document.getElementById("display-bio").textContent === "No bio yet."
          ? ""
          : document.getElementById("display-bio").textContent;
    } else {
      form.style.display = "none";
    }
  });

  // This handles closing the edit form with cancel.
  document.getElementById("cancel-btn").addEventListener("click", () => {
    document.getElementById("edit-form").style.display = "none";
  });

  // This handles saving the profile name and bio to the backend.
  document.getElementById("save-btn").addEventListener("click", () => {
    const name = document.getElementById("input-name").value.trim();
    const bio = document.getElementById("input-bio").value.trim();

    const formData = new FormData();
    formData.append("user_id", userId);
    formData.append("name", name);
    formData.append("bio", bio);

    fetch("/profile", {
      method: "POST",
      body: formData,
    })
      .then((res) => res.json())
      .then((data) => {
        if (data.message) {
          // This updates the display on the page after saving.
          if (name) document.getElementById("display-name").textContent = name;
          if (bio) document.getElementById("display-bio").textContent = bio;
          document.getElementById("save-msg").textContent = "Profile saved!";
          setTimeout(() => {
            document.getElementById("save-msg").textContent = "";
            document.getElementById("edit-form").style.display = "none";
          }, 1500);
        } else {
          document.getElementById("save-msg").textContent =
            data.error || "Something went wrong";
        }
      })
      .catch(() => {
        document.getElementById("save-msg").textContent =
          "Error saving profile";
      });
  });

  // This handles rendering the skills list on the page.
  function renderSkills() {
    const list = document.getElementById("skills-list");
    if (skills.length === 0) {
      list.innerHTML = '<p class="empty-msg">No skills added yet.</p>';
      return;
    }
    list.innerHTML = "";
    skills.forEach((skill, i) => {
      const tag = document.createElement("span");
      tag.className = "skill-tag";
      tag.innerHTML = `${skill} <button onclick="removeSkill(${i})"><i class="ph ph-x"></i></button>`;
      list.appendChild(tag);
    });
  }

  // This handles removing a skill by its index.
  window.removeSkill = function (index) {
    skills.splice(index, 1);
    localStorage.setItem("skills", JSON.stringify(skills));
    renderSkills();
  };

  // This toggles the skill input area when you click the plus button.
  document.getElementById("add-skill-btn").addEventListener("click", () => {
    const area = document.getElementById("skill-input-area");
    area.style.display = area.style.display === "none" ? "flex" : "none";
  });

  // This handles adding a skill to the list.
  document.getElementById("save-skill-btn").addEventListener("click", () => {
    const input = document.getElementById("skill-input");
    const val = input.value.trim();
    if (!val) return;
    skills.push(val);
    localStorage.setItem("skills", JSON.stringify(skills));
    input.value = "";
    document.getElementById("skill-input-area").style.display = "none";
    renderSkills();
  });

  // This handles rendering the experience list on the page.
  function renderExperience() {
    const list = document.getElementById("exp-list");
    if (experience.length === 0) {
      list.innerHTML = '<p class="empty-msg">No experience added yet.</p>';
      return;
    }
    list.innerHTML = "";
    experience.forEach((exp, i) => {
      const entry = document.createElement("div");
      entry.className = "exp-entry";
      entry.innerHTML = `
        <h3>${exp.title} <button onclick="removeExp(${i})" style="background:transparent;border:none;color:var(--text-muted);cursor:pointer;font-size:12px;"><i class="ph ph-x"></i></button></h3>
        <p>${exp.company} &nbsp;|&nbsp; ${exp.years}</p>
      `;
      list.appendChild(entry);
    });
  }

  // This handles removing an experience entry.
  window.removeExp = function (index) {
    experience.splice(index, 1);
    localStorage.setItem("experience", JSON.stringify(experience));
    renderExperience();
  };

  // This toggles the experience input area.
  document.getElementById("add-exp-btn").addEventListener("click", () => {
    const area = document.getElementById("exp-input-area");
    area.style.display = area.style.display === "none" ? "flex" : "none";
  });

  // This handles adding a new experience entry.
  document.getElementById("save-exp-btn").addEventListener("click", () => {
    const title = document.getElementById("exp-title").value.trim();
    const company = document.getElementById("exp-company").value.trim();
    const years = document.getElementById("exp-years").value.trim();
    if (!title || !company) return;
    experience.push({ title, company, years });
    localStorage.setItem("experience", JSON.stringify(experience));
    document.getElementById("exp-title").value = "";
    document.getElementById("exp-company").value = "";
    document.getElementById("exp-years").value = "";
    document.getElementById("exp-input-area").style.display = "none";
    renderExperience();
  });

  // This toggles the resume upload input when you click the upload button.
  document.getElementById("upload-resume-btn").addEventListener("click", () => {
    const area = document.getElementById("resume-input-area");
    area.style.display = area.style.display === "none" ? "flex" : "none";
  });

  // This handles uploading the resume directly from the resume section.
  document.getElementById("save-resume-btn").addEventListener("click", () => {
    const resumeFile = document.getElementById("resume-file-input").files[0];
    if (!resumeFile) return;

    const formData = new FormData();
    formData.append("user_id", userId);
    formData.append("resume", resumeFile);

    fetch("/profile", {
      method: "POST",
      body: formData,
    })
      .then((res) => res.json())
      .then((data) => {
        if (data.message) {
          showResume(resumeFile.name);
          document.getElementById("resume-input-area").style.display = "none";
          document.getElementById("resume-save-msg").textContent =
            "Resume uploaded!";
          setTimeout(() => {
            document.getElementById("resume-save-msg").textContent = "";
          }, 1500);
        }
      })
      .catch(() => {
        document.getElementById("resume-save-msg").textContent =
          "Error uploading resume";
      });
  });

  // This shows the uploaded resume filename in the resume section.
  function showResume(filename) {
    const section = document.getElementById("resume-section");
    section.innerHTML = `<div class="resume-file"><i class="ph ph-file-text"></i> ${filename}</div>`;
  }

  // This handles the logout button.
  document.getElementById("logout-btn").addEventListener("click", () => {
    localStorage.clear();
    window.location.href = "/";
  });

  // Load whatever is already saved.
  renderSkills();
  renderExperience();
});
