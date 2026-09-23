// ==================================================
// ResumePilot AI - Results Page
// ==================================================


// --------------------------------------------------
// Load real analysis result
// --------------------------------------------------

const storedResult =
  sessionStorage.getItem("analysisResult");


if (!storedResult) {

  window.location.href =
    "analyze.html";
}


const result =
  JSON.parse(storedResult);


// --------------------------------------------------
// Extract backend data
// --------------------------------------------------

const ats =
  result.ats || {};

const components =
  ats.components || {};

const matching =
  result.matching || {};

const requirements =
  result.requirements || [];

const recommendations =
  result.recommendations || [];


// --------------------------------------------------
// Helper
// --------------------------------------------------

function escapeHTML(value) {

  return String(value ?? "")
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;")
    .replace(/"/g, "&quot;")
    .replace(/'/g, "&#039;");
}


// ==================================================
// ATS SCORE
// ==================================================

const atsScore =
  Number(ats.ats_score || 0);

const scoreRing =
  document.querySelector(
    ".score-ring.big"
  );

const scoreNumber =
  document.querySelector(
    ".score-ring.big strong"
  );


if (scoreRing) {

  scoreRing.style.setProperty(
    "--score",
    atsScore
  );
}


if (scoreNumber) {

  scoreNumber.textContent =
    Math.round(atsScore);
}


// Score heading
const scoreHeading =
  document.querySelector(
    ".score-copy h2"
  );

const scoreDescription =
  document.querySelector(
    ".score-copy p"
  );


if (scoreHeading) {

  if (atsScore >= 80) {

    scoreHeading.textContent =
      "Strong starting point";

  } else if (atsScore >= 60) {

    scoreHeading.textContent =
      "Good starting point";

  } else {

    scoreHeading.textContent =
      "Needs improvement";
  }
}


if (scoreDescription) {

  scoreDescription.textContent =
    `Your ResumePilot analysis score is ${Math.round(
      atsScore
    )}/100 based on skill matching, keyword coverage and resume structure.`;
}


// Remove fake potential improvement
const trend =
  document.querySelector(
    ".score-copy .trend"
  );


if (trend) {

  trend.textContent =
    "Based on ResumePilot's scoring model";
}


// ==================================================
// MATCH SUMMARY
// ==================================================

const matched =
  matching.matched || [];

const partial =
  matching.partial || [];

const missing =
  matching.missing || [];


// Summary rows
const summaryRows =
  document.querySelectorAll(
    ".summary-row"
  );


if (summaryRows.length >= 3) {

  summaryRows[0]
    .querySelector("strong")
    .textContent =
    matched.length;

  summaryRows[1]
    .querySelector("strong")
    .textContent =
    partial.length;

  summaryRows[2]
    .querySelector("strong")
    .textContent =
    missing.length;
}


// ==================================================
// SCORE COMPONENTS
// ==================================================

const skillScore =
  Number(
    components.skill_match || 0
  );

const keywordScore =
  Number(
    components.keyword_coverage || 0
  );

const structureScore =
  Number(
    components.resume_structure || 0
  );


// Existing metric blocks
const metrics =
  document.querySelectorAll(
    ".skill-panel .metric"
  );


// Skills
if (metrics[0]) {

  updateMetric(
    metrics[0],
    "Skills",
    skillScore
  );
}


// Keywords
if (metrics[1]) {

  updateMetric(
    metrics[1],
    "Keywords",
    keywordScore
  );
}


// The backend currently doesn't calculate
// separate experience/project/education/
// formatting scores.
//
// Don't display fake numbers.
if (metrics[2]) {

  updateMetric(
    metrics[2],
    "Resume Structure",
    structureScore
  );
}


if (metrics[3]) {

  metrics[3].style.display =
    "none";
}


if (metrics[4]) {

  metrics[4].style.display =
    "none";
}


if (metrics[5]) {

  metrics[5].style.display =
    "none";
}


// --------------------------------------------------
// Metric helper
// --------------------------------------------------

function updateMetric(
  metric,
  label,
  value
) {

  const labelElement =
    metric.querySelector(
      "span"
    );

  const valueElement =
    metric.querySelector(
      "b"
    );

  const bar =
    metric.querySelector(
      ".bar i"
    );


  if (labelElement) {

    labelElement.textContent =
      label;
  }


  if (valueElement) {

    valueElement.textContent =
      `${Math.round(value)}%`;
  }


  if (bar) {

    bar.style.width =
      `${Math.min(
        Math.max(value, 0),
        100
      )}%`;
  }
}


// ==================================================
// MATCH TABS
// ==================================================

const matchTabs =
  document.querySelectorAll(
    ".match-tabs span"
  );

const skillList =
  document.querySelector(
    ".skill-list"
  );


function showSkills(
  type
) {

  if (!skillList) return;


  let skills = [];

  let symbol = "✓";


  if (type === "matched") {

    skills = matched;
    symbol = "✓";

  } else if (type === "partial") {

    skills = partial;
    symbol = "!";

  } else {

    skills = missing;
    symbol = "×";
  }


  if (skills.length === 0) {

    skillList.innerHTML =
      "<span>No skills found.</span>";

    return;
  }


  skillList.innerHTML =
    skills
      .map(
        skill =>
          `<span>${symbol} ${escapeHTML(skill)}</span>`
      )
      .join("");
}


matchTabs.forEach(
  (tab, index) => {

    tab.addEventListener(
      "click",
      () => {

        matchTabs.forEach(
          t =>
            t.classList.remove(
              "active"
            )
        );

        tab.classList.add(
          "active"
        );


        if (index === 0) {

          showSkills(
            "matched"
          );

        } else if (index === 1) {

          showSkills(
            "partial"
          );

        } else {

          showSkills(
            "missing"
          );
        }
      }
    );
  }
);


// Initial state
showSkills("matched");


// Update tab counts
if (matchTabs.length >= 3) {

  matchTabs[0].textContent =
    `Matched (${matched.length})`;

  matchTabs[1].textContent =
    `Partial (${partial.length})`;

  matchTabs[2].textContent =
    `Missing (${missing.length})`;
}


// ==================================================
// REQUIREMENT EVIDENCE
// ==================================================

function findRequirement(
  skill
) {

  return requirements.find(
    item =>
      item.requirement
        .toLowerCase() ===
      skill.toLowerCase()
  );
}


function showEvidence(
  requirement
) {

  const item =
    findRequirement(
      requirement
    );


  if (!item) {

    alert(
      "No analysis evidence found."
    );

    return;
  }


  const evidence =
    item.evidence || [];


  if (evidence.length === 0) {

    alert(
      `No supporting resume evidence was found for "${requirement}".`
    );

    return;
  }


  const bestEvidence =
    evidence
      .map(
        item =>
          item.text
      )
      .join(
        "\n\n"
      );


  alert(
    `Resume evidence for ${requirement}:\n\n${bestEvidence}`
  );
}


// ==================================================
// IMPROVEMENTS
// ==================================================

const suggestionsContainer =
  document.querySelector(
    ".suggestions"
  );


if (
  suggestionsContainer &&
  recommendations.length > 0
) {

  suggestionsContainer.innerHTML =
    recommendations
      .map(
        recommendation => {

          const priority =
            recommendation.priority ||
            "low";

          const title =
            recommendation.requirement ||
            "Resume improvement";

          const description =
            recommendation.recommendation ||
            "Review this requirement.";

          const evidence =
            recommendation.evidence ||
            [];


          const evidenceText =
            evidence.length > 0
              ? "View evidence →"
              : "View suggestion →";


          return `
            <article class="suggestion ${escapeHTML(priority)}">

              <div class="priority">
                ${escapeHTML(
                  priority
                    .charAt(0)
                    .toUpperCase()
                    +
                  priority.slice(1)
                )}
                Priority
              </div>

              <h3>
                ${escapeHTML(title)}
              </h3>

              <p>
                ${escapeHTML(description)}
              </p>

              <a
                href="#"
                class="evidence-link"
                data-requirement="${escapeHTML(title)}"
              >
                ${evidenceText}
              </a>

            </article>
          `;
        }
      )
      .join("");


  // Evidence buttons
  document
    .querySelectorAll(
      ".evidence-link"
    )
    .forEach(
      link => {

        link.addEventListener(
          "click",
          event => {

            event.preventDefault();

            showEvidence(
              link.dataset.requirement
            );
          }
        );
      }
    );
}


// ==================================================
// MAIN TABS
// ==================================================

document
  .querySelectorAll(".tab")
  .forEach(
    tab => {

      tab.addEventListener(
        "click",
        () => {

          document
            .querySelectorAll(".tab")
            .forEach(
              t =>
                t.classList.remove(
                  "active"
                )
            );

          tab.classList.add(
            "active"
          );
        }
      );
    }
  );


// ==================================================
// JOB DESCRIPTION
// ==================================================

const jobDescription =
  sessionStorage.getItem(
    "jobDescription"
  );


// We don't have a structured job title
// yet, so don't invent one.


const jobTitle =
  document.querySelector(
    ".job-card h2"
  );


const jobCompany =
  document.querySelector(
    ".job-card p"
  );


if (jobTitle) {

  jobTitle.textContent =
    "Target Job Description";
}


if (jobCompany) {

  jobCompany.textContent =
    jobDescription
      ? `${jobDescription.substring(
          0,
          120
        )}${jobDescription.length > 120 ? "..." : ""}`
      : "Job description analyzed by ResumePilot AI";
}


// ==================================================
// Header message
// ==================================================

const resultsTitle =
  document.querySelector(
    ".results-head h1"
  );


if (resultsTitle) {

  if (atsScore >= 80) {

    resultsTitle.textContent =
      "Your resume shows strong alignment with this role.";

  } else if (atsScore >= 60) {

    resultsTitle.textContent =
      "Your resume shows moderate alignment with this role.";

  } else {

    resultsTitle.textContent =
      "Your resume has several areas to improve for this role.";
  }
}


// ==================================================
// Resume Name
// ==================================================

const resumeName =
  result.resume?.filename ||
  sessionStorage.getItem(
    "resumeName"
  );


// Optional: update resume preview title
const preview =
  document.querySelector(
    ".resume-preview .preview-head span"
  );

if (preview && resumeName) {

  preview.textContent =
    resumeName
      .split(".")
      .pop()
      .toUpperCase();
}
