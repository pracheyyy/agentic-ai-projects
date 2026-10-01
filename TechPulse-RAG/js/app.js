const $ = (selector) => document.querySelector(selector);

const API_BASE = "http://127.0.0.1:8000";

// -----------------------------
// Utility helpers
// -----------------------------

function escapeHTML(value) {
  if (value === null || value === undefined) return "";
  return String(value)
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;")
    .replace(/"/g, "&quot;")
    .replace(/'/g, "&#039;");
}

function formatTime(dateString) {
  if (!dateString) return "Recently";

  const date = new Date(dateString);
  if (Number.isNaN(date.getTime())) return dateString;

  const diff = Math.floor((Date.now() - date.getTime()) / 1000);

  if (diff < 60) return "Just now";
  if (diff < 3600) return `${Math.floor(diff / 60)} min ago`;
  if (diff < 86400) return `${Math.floor(diff / 3600)} hrs ago`;
  if (diff < 604800) return `${Math.floor(diff / 86400)} days ago`;

  return date.toLocaleDateString();
}

function showToast(message) {
  const toast = $("#toast");
  if (!toast) return;

  toast.textContent = message;
  toast.classList.add("show");

  setTimeout(() => toast.classList.remove("show"), 2200);
}

// -----------------------------
// Real news from FastAPI
// -----------------------------

async function fetchNews() {
  try {
    const response = await fetch(`${API_BASE}/api/news/?limit=20`);

    if (!response.ok) {
      throw new Error(`News API returned ${response.status}`);
    }

    const data = await response.json();

    if (!data.articles || data.articles.length === 0) {
      showToast("No news available right now.");
      return;
    }

    renderBackendNews(data.articles);
  } catch (error) {
    console.error("News API error:", error);
    showToast("Could not connect to the news backend.");
  }
}

function renderBackendNews(articles) {
  const featured = articles[0];

  if ($("#featuredNews") && featured) {
    $("#featuredNews").innerHTML = `
      <article class="featured-card">
        <span class="article-tag">${escapeHTML(featured.source)}</span>
        <h3>${escapeHTML(featured.title)}</h3>
        <div class="article-meta">
          ${escapeHTML(featured.source)}
          &nbsp;·&nbsp;
          ${formatTime(featured.published)}
        </div>
      </article>
    `;
  }

  if ($("#newsList")) {
    $("#newsList").innerHTML = articles.slice(1).map(article => `
      <article class="news-item">
        <div>
          <span class="article-tag">${escapeHTML(article.source)}</span>
          <h3>${escapeHTML(article.title)}</h3>
          <p>${escapeHTML(article.source)} · ${formatTime(article.published)}</p>
        </div>
        <a
          class="news-arrow"
          href="${escapeHTML(article.url)}"
          target="_blank"
          rel="noopener noreferrer"
        >↗</a>
      </article>
    `).join("");
  }
}

// Keep these names so the original UI structure remains compatible.
function renderFeatured() {}
function renderNews() {}

// -----------------------------
// Topics
// -----------------------------

function renderTopics() {
  if (!$("#topicGrid") || typeof TOPICS === "undefined") return;

  $("#topicGrid").innerHTML = TOPICS.map(t => `
    <button class="topic-card" onclick="topicMessage('${escapeHTML(t[2])}')">
      <span class="topic-number">${escapeHTML(t[0])}</span>
      <h3>${escapeHTML(t[1])}</h3>
      <p>${escapeHTML(t[2])}</p>
    </button>
  `).join("");

  if ($("#topicMarquee")) {
    $("#topicMarquee").innerHTML = TOPICS.slice(0, 6).map(t =>
      `<span>${escapeHTML(t[1]).toUpperCase()}</span><b>✦</b>`
    ).join("");
  }
}

function topicMessage(topic) {
  if ($("#heroInput")) $("#heroInput").value = topic;
  if ($("#askInput")) $("#askInput").value = topic;
  openAI(topic);
}

// -----------------------------
// Real RAG
// -----------------------------

async function openAI(question) {
  const q = (question || "").trim();

  if (!q) {
    showToast("Ask TechPulse a question first.");
    return;
  }

  if ($("#modalTitle")) $("#modalTitle").textContent = q;
  if ($("#answerModal")) $("#answerModal").classList.remove("hidden");
  if ($("#loading")) $("#loading").classList.remove("hidden");
  if ($("#answer")) $("#answer").classList.add("hidden");
  if ($("#sources")) $("#sources").innerHTML = "";

  try {
    const response = await fetch(`${API_BASE}/api/rag/ask`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        question: q,
        top_k: 6
      })
    });

    const data = await response.json();

    if (!response.ok) {
      throw new Error(data.detail || "RAG request failed.");
    }

    if ($("#answer")) {
      $("#answer").innerHTML = formatAnswer(data.answer);
    }

    if ($("#sources")) {
      if (data.sources && data.sources.length > 0) {
        $("#sources").innerHTML = data.sources.map(source => `
          <a
            class="source-row"
            href="${escapeHTML(source.url || "#")}"
            target="_blank"
            rel="noopener noreferrer"
          >
            <strong>${escapeHTML(source.title || "Source")}</strong>
            <span>
              ${escapeHTML(source.source || "TechPulse")}
              · ${source.score !== undefined ? `Relevance ${Number(source.score).toFixed(2)}` : ""}
            </span>
          </a>
        `).join("");
      } else {
        $("#sources").innerHTML = `
          <div class="source-row">
            <span>No supporting sources were found.</span>
          </div>
        `;
      }
    }

    if ($("#loading")) $("#loading").classList.add("hidden");
    if ($("#answer")) $("#answer").classList.remove("hidden");
  } catch (error) {
    console.error("RAG error:", error);

    if ($("#loading")) $("#loading").classList.add("hidden");
    if ($("#answer")) {
      $("#answer").classList.remove("hidden");
      $("#answer").innerHTML = `
        <div class="answer-error">
          <strong>TechPulse couldn't answer right now.</strong>
          <p>${escapeHTML(error.message)}</p>
          <p>Make sure the FastAPI backend is running on 127.0.0.1:8000.</p>
        </div>
      `;
    }

    showToast("RAG request failed.");
  }
}

function formatAnswer(text) {
  if (!text) return "<p>No answer generated.</p>";

  return String(text)
    .split("\n")
    .filter(line => line.trim())
    .map(line => `<p>${escapeHTML(line)}</p>`)
    .join("");
}

// -----------------------------
// Input events
// -----------------------------

if ($("#heroAsk")) {
  $("#heroAsk").addEventListener("click", () => {
    openAI($("#heroInput")?.value.trim());
  });
}

if ($("#heroInput")) {
  $("#heroInput").addEventListener("keydown", event => {
    if (event.key === "Enter") openAI(event.target.value.trim());
  });
}

if ($("#askButton")) {
  $("#askButton").addEventListener("click", () => {
    openAI($("#askInput")?.value.trim());
  });
}

if ($("#askInput")) {
  $("#askInput").addEventListener("keydown", event => {
    if (event.key === "Enter") openAI(event.target.value.trim());
  });
}

document.querySelectorAll(".quick-prompts button").forEach(button => {
  button.addEventListener("click", () => {
    const question = button.textContent.trim();
    if ($("#heroInput")) $("#heroInput").value = question;
    openAI(question);
  });
});

document.querySelectorAll(".question-chips button").forEach(button => {
  button.addEventListener("click", () => {
    const question = button.textContent.trim();
    if ($("#askInput")) $("#askInput").value = question;
    openAI(question);
  });
});

// -----------------------------
// Modal
// -----------------------------

if ($("#modalClose")) {
  $("#modalClose").addEventListener("click", () => {
    $("#answerModal").classList.add("hidden");
  });
}

if ($("#answerModal")) {
  $("#answerModal").addEventListener("click", event => {
    if (event.target.id === "answerModal") {
      $("#answerModal").classList.add("hidden");
    }
  });
}

// -----------------------------
// Load more
// -----------------------------

if ($("#loadMore")) {
  $("#loadMore").addEventListener("click", () => {
    showToast("Refreshing latest stories...");
    fetchNews();
  });
}

// -----------------------------
// Theme
// -----------------------------

const savedTheme = localStorage.getItem("techpulse-theme");

if (savedTheme) {
  document.documentElement.dataset.theme = savedTheme;
}

function updateThemeIcon() {
  if (!$("#themeIcon")) return;

  $("#themeIcon").textContent =
    document.documentElement.dataset.theme === "light" ? "☾" : "☼";
}

if ($("#themeBtn")) {
  $("#themeBtn").addEventListener("click", () => {
    const current = document.documentElement.dataset.theme;
    const next = current === "light" ? "dark" : "light";

    document.documentElement.dataset.theme = next;
    localStorage.setItem("techpulse-theme", next);
    updateThemeIcon();
  });
}

updateThemeIcon();

// -----------------------------
// Initialize
// -----------------------------

renderTopics();
fetchNews();
