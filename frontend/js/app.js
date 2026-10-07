const resumeInput = document.getElementById("resume");
const uploadArea = document.getElementById("uploadArea");
const fileName = document.getElementById("fileName");

const jobDescription = document.getElementById("jobDescription");
const charCount = document.getElementById("charCount");

const analyzeBtn = document.getElementById("analyzeBtn");
const buttonText = document.getElementById("buttonText");
const loadingSpinner = document.getElementById("loadingSpinner");

const results = document.getElementById("results");
const errorBox = document.getElementById("errorBox");

const matchScore = document.getElementById("matchScore");
const scoreDescription = document.getElementById("scoreDescription");

const scoreCircle = document.getElementById("scoreCircle");
const ringScore = document.getElementById("ringScore");

const skillCoverage = document.getElementById("skillCoverage");
const contentSimilarity = document.getElementById("contentSimilarity");

const category = document.getElementById("category");
const matchStatus = document.getElementById("matchStatus");

const matchedSkills = document.getElementById("matchedSkills");
const missingSkills = document.getElementById("missingSkills");

const matchedCount = document.getElementById("matchedCount");
const missingCount = document.getElementById("missingCount");

const suggestions = document.getElementById("suggestions");


// ==========================================
// FILE SELECTION
// ==========================================

resumeInput.addEventListener("change", function () {

    if (!this.files.length) {
        fileName.textContent = "";
        return;
    }

    const file = this.files[0];

    const extension = file.name
        .split(".")
        .pop()
        .toLowerCase();

    if (!["pdf", "txt"].includes(extension)) {

        showError(
            "Only PDF and TXT files are supported."
        );

        this.value = "";
        fileName.textContent = "";

        return;
    }

    hideError();

    fileName.textContent =
        `Selected: ${file.name}`;

    results.classList.add("hidden");
});


// ==========================================
// DRAG & DROP
// ==========================================

uploadArea.addEventListener("dragover", function (event) {

    event.preventDefault();

    uploadArea.classList.add("dragging");
});


uploadArea.addEventListener("dragleave", function () {

    uploadArea.classList.remove("dragging");
});


uploadArea.addEventListener("drop", function (event) {

    event.preventDefault();

    uploadArea.classList.remove("dragging");

    const files = event.dataTransfer.files;

    if (!files.length) {
        return;
    }

    const file = files[0];

    const extension = file.name
        .split(".")
        .pop()
        .toLowerCase();

    if (!["pdf", "txt"].includes(extension)) {

        showError(
            "Only PDF and TXT files are supported."
        );

        return;
    }

    resumeInput.files = files;

    fileName.textContent =
        `Selected: ${file.name}`;

    hideError();

    results.classList.add("hidden");
});


// ==========================================
// CHARACTER COUNTER
// ==========================================

jobDescription.addEventListener("input", function () {

    const count = this.value.length;

    charCount.textContent =
        count.toLocaleString();
});


// ==========================================
// ANALYZE BUTTON
// ==========================================

analyzeBtn.addEventListener(
    "click",
    analyzeResume
);


async function analyzeResume() {

    hideError();

    const resume = resumeInput.files[0];

    const jd = jobDescription.value.trim();


    // Validation

    if (!resume) {

        showError(
            "Please upload your resume first."
        );

        return;
    }


    if (!jd) {

        showError(
            "Please paste the job description."
        );

        return;
    }


    // Loading

    setLoading(true);


    const formData = new FormData();

    formData.append(
        "resume",
        resume
    );

    formData.append(
        "job_description",
        jd
    );


    try {

        const response = await fetch(
            "/analyze",
            {
                method: "POST",
                body: formData
            }
        );


        const data = await response.json();


        if (!response.ok || data.error) {

            throw new Error(
                data.error ||
                "Unable to analyze the resume."
            );
        }


        displayResults(data);


    } catch (error) {

        console.error(error);

        showError(
            error.message ||
            "Something went wrong. Please try again."
        );


    } finally {

        setLoading(false);
    }
}


// ==========================================
// DISPLAY RESULTS
// ==========================================

function displayResults(data) {

    results.classList.remove("hidden");


    const score = Number(
        data.match_score || 0
    );

    const skillScore = Number(
        data.skill_coverage || 0
    );

    const similarityScore = Number(
        data.content_similarity || 0
    );


    // Overall score

    matchScore.textContent =
        formatScore(score);

    ringScore.textContent =
        `${formatScore(score)}%`;


    // Circular progress

    const circumference = 314;

    if (scoreCircle) {

        scoreCircle.style.strokeDashoffset =
            circumference -
            (
                circumference *
                Math.min(score, 100) /
                100
            );
    }


    // Skill coverage

    skillCoverage.textContent =
        `${formatScore(skillScore)}%`;


    // Content similarity

    contentSimilarity.textContent =
        `${formatScore(similarityScore)}%`;


    // Predicted role

    category.textContent =
        data.predicted_category ||
        "Not available";


    // Match status

    setMatchStatus(score);


    // Description

    setScoreDescription(score);


    // Matched skills

    const matched =
        data.matched_skills || [];

    renderSkills(
        matchedSkills,
        matched,
        "matched"
    );

    matchedCount.textContent =
        matched.length;


    // Missing skills

    const missing =
        data.missing_skills || [];

    renderSkills(
        missingSkills,
        missing,
        "missing"
    );

    missingCount.textContent =
        missing.length;


    // Suggestions

    renderSuggestions(
        data.suggestions || []
    );


    // Scroll

    setTimeout(() => {

        results.scrollIntoView({
            behavior: "smooth",
            block: "start"
        });

    }, 150);
}


// ==========================================
// MATCH STATUS
// ==========================================

function setMatchStatus(score) {

    let label;
    let background;
    let color;


    if (score >= 80) {

        label = "Strong Match";
        background = "#edf8f0";
        color = "#16803c";

    } else if (score >= 65) {

        label = "Good Match";
        background = "#eff6ff";
        color = "#2563eb";

    } else if (score >= 45) {

        label = "Partial Match";
        background = "#fffbeb";
        color = "#a16207";

    } else {

        label = "Low Match";
        background = "#fef3f2";
        color = "#b42318";
    }


    matchStatus.textContent = label;

    matchStatus.style.background =
        background;

    matchStatus.style.color =
        color;
}


// ==========================================
// SCORE DESCRIPTION
// ==========================================

function setScoreDescription(score) {

    if (score >= 80) {

        scoreDescription.textContent =
            "Your resume aligns strongly with this role.";

    } else if (score >= 65) {

        scoreDescription.textContent =
            "Your resume has a good overall alignment with this role.";

    } else if (score >= 45) {

        scoreDescription.textContent =
            "Your resume partially matches the requirements.";

    } else {

        scoreDescription.textContent =
            "Several requirements may need attention.";
    }
}


// ==========================================
// RENDER SKILLS
// ==========================================

function renderSkills(
    container,
    skills,
    type
) {

    container.innerHTML = "";


    if (!skills.length) {

        const message =
            document.createElement("span");

        message.className =
            "empty-message";

        message.textContent =
            type === "matched"
                ? "No matching skills detected."
                : "No missing skills detected.";

        container.appendChild(message);

        return;
    }


    skills.forEach(skill => {

        const pill =
            document.createElement("span");

        pill.className =
            "skill-pill " +
            (
                type === "matched"
                    ? "matched-pill"
                    : "missing-pill"
            );

        pill.textContent =
            formatSkill(skill);

        container.appendChild(pill);
    });
}


// ==========================================
// RENDER SUGGESTIONS
// ==========================================

function renderSuggestions(items) {

    suggestions.innerHTML = "";


    if (!items.length) {

        const item =
            document.createElement("div");

        item.className =
            "suggestion-item";

        item.textContent =
            "No additional recommendations at this time.";

        suggestions.appendChild(item);

        return;
    }


    items.forEach((suggestion, index) => {

        const item =
            document.createElement("div");

        item.className =
            "suggestion-item";


        const number =
            document.createElement("span");

        number.className =
            "suggestion-number";

        number.textContent =
            index + 1;


        const text =
            document.createElement("span");

        text.textContent =
            suggestion;


        item.appendChild(number);
        item.appendChild(text);

        suggestions.appendChild(item);
    });
}


// ==========================================
// FORMAT SKILLS
// ==========================================

function formatSkill(skill) {

    const names = {

        "c++": "C++",

        "c#": "C#",

        "javascript": "JavaScript",

        "typescript": "TypeScript",

        "node.js": "Node.js",

        "nodejs": "Node.js",

        "spring boot": "Spring Boot",

        "rest api": "REST API",

        "rest apis": "REST APIs",

        "machine learning":
            "Machine Learning",

        "deep learning":
            "Deep Learning",

        "artificial intelligence":
            "Artificial Intelligence",

        "natural language processing":
            "Natural Language Processing",

        "scikit-learn":
            "Scikit-learn",

        "data structures":
            "Data Structures",

        "object oriented programming":
            "Object-Oriented Programming",

        "operating systems":
            "Operating Systems",

        "computer networks":
            "Computer Networks",

        "database management":
            "Database Management"
    };


    if (names[skill]) {
        return names[skill];
    }


    return skill
        .split(" ")
        .map(
            word =>
                word.charAt(0).toUpperCase() +
                word.slice(1)
        )
        .join(" ");
}


// ==========================================
// LOADING STATE
// ==========================================

function setLoading(isLoading) {

    analyzeBtn.disabled =
        isLoading;


    if (isLoading) {

        buttonText.textContent =
            "Analyzing...";

        loadingSpinner.classList.remove(
            "hidden"
        );

    } else {

        buttonText.textContent =
            "Analyze Resume";

        loadingSpinner.classList.add(
            "hidden"
        );
    }
}


// ==========================================
// ERROR
// ==========================================

function showError(message) {

    errorBox.textContent =
        message;

    errorBox.classList.remove(
        "hidden"
    );
}


function hideError() {

    errorBox.textContent = "";

    errorBox.classList.add(
        "hidden"
    );
}


// ==========================================
// SCORE FORMAT
// ==========================================

function formatScore(value) {

    const number = Number(value);

    if (Number.isNaN(number)) {
        return "0";
    }

    return Number(
        number.toFixed(1)
    ).toString();
}