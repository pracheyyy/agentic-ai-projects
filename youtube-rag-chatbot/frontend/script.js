const API_BASE_URL = "http://127.0.0.1:8000";

const loadBtn = document.getElementById("loadBtn");
const youtubeUrl = document.getElementById("youtubeUrl");
const videoContainer = document.getElementById("videoContainer");
const recDot = document.getElementById("recDot");
const mainContent = document.getElementById("mainContent");

const sendBtn = document.getElementById("sendBtn");
const questionInput = document.getElementById("questionInput");
const chatMessages = document.getElementById("chatMessages");
const welcomeMessage = document.getElementById("welcomeMessage");
const suggestionChips = document.getElementById("suggestionChips");

const themeToggle = document.getElementById("themeToggle");


// =========================
// STATE
// =========================

let videoLoaded = false;


// =========================
// THEME
// =========================

function applyTheme(theme) {

    document.documentElement.setAttribute("data-theme", theme);

    themeToggle.setAttribute("aria-pressed", theme === "light");

    themeToggle.setAttribute(
        "aria-label",
        theme === "light"
            ? "Switch to dark theme"
            : "Switch to light theme"
    );

    try {
        localStorage.setItem("ytrag-theme", theme);
    } catch (error) {
        // Storage unavailable
    }
}


function getStoredTheme() {

    try {
        return localStorage.getItem("ytrag-theme");
    } catch (error) {
        return null;
    }
}


applyTheme(
    getStoredTheme() === "light"
        ? "light"
        : "dark"
);


themeToggle.addEventListener("click", () => {

    const current =
        document.documentElement.getAttribute("data-theme");

    applyTheme(
        current === "light"
            ? "dark"
            : "light"
    );

});


// =========================
// EXTRACT YOUTUBE VIDEO ID
// =========================

function getYoutubeVideoId(url) {

    try {

        const urlObject = new URL(url);

        // youtube.com/watch?v=VIDEO_ID
        if (urlObject.hostname.includes("youtube.com")) {

            return urlObject.searchParams.get("v");

        }

        // youtu.be/VIDEO_ID
        if (urlObject.hostname.includes("youtu.be")) {

            return urlObject.pathname.substring(1);

        }

        return null;

    } catch (error) {

        return null;

    }

}


// =========================
// LOAD VIDEO
// =========================

loadBtn.addEventListener("click", loadVideo);


async function loadVideo() {

    const url = youtubeUrl.value.trim();

    if (!url) {

        youtubeUrl.focus();

        return;
    }


    const videoId = getYoutubeVideoId(url);

    if (!videoId) {

        alert("Please enter a valid YouTube URL.");

        youtubeUrl.focus();

        return;
    }


    // Loading state
    loadBtn.disabled = true;
    loadBtn.textContent = "Loading...";


    try {

        // Send YouTube URL to FastAPI
        const response = await fetch(
            `${API_BASE_URL}/video/load`,
            {
                method: "POST",

                headers: {
                    "Content-Type": "application/json"
                },

                body: JSON.stringify({
                    youtube_url: url
                })
            }
        );


        const data = await response.json();


        // Backend returned an error
        if (!data.success) {

            throw new Error(
                data.message || "Could not load video."
            );
        }


        // =========================
        // LOAD YOUTUBE PLAYER
        // =========================

        videoContainer.innerHTML = `

            <iframe
                width="100%"
                height="100%"
                src="https://www.youtube.com/embed/${videoId}"
                title="YouTube video player"
                frameborder="0"
                allow="accelerometer;
                       autoplay;
                       clipboard-write;
                       encrypted-media;
                       gyroscope;
                       picture-in-picture;
                       web-share"
                allowfullscreen>
            </iframe>

        `;


        // Video successfully loaded
        videoLoaded = true;

        recDot.classList.add("live");

        mainContent.classList.remove("is-hidden");


        // Add system message
        if (welcomeMessage) {

            welcomeMessage.textContent =
                "Video loaded successfully! Ask me anything about the video.";

        }


        console.log("Video loaded successfully.");
        console.log("Video ID:", data.video_id);
        console.log("Transcript language:", data.language);


    } catch (error) {

        console.error("Load video error:", error);

        alert(
            "Could not load the video.\n\n" +
            error.message
        );

        videoLoaded = false;

    } finally {

        loadBtn.disabled = false;
        loadBtn.textContent = "Load Video";

    }

}


// =========================
// SEND MESSAGE
// =========================

sendBtn.addEventListener(
    "click",
    () => sendMessage()
);


questionInput.addEventListener(
    "keydown",
    (event) => {

        if (event.key === "Enter") {

            event.preventDefault();

            sendMessage();

        }

    }
);


suggestionChips.addEventListener(
    "click",
    (event) => {

        const chip =
            event.target.closest(".chip");

        if (!chip) return;

        sendMessage(chip.textContent);

    }
);


// =========================
// ADD MESSAGE
// =========================

function addMessage(text, sender) {

    const row =
        document.createElement("div");

    row.className =
        `msg-row ${sender}`;


    const bubble =
        document.createElement("div");

    bubble.className =
        "msg-bubble";

    bubble.textContent =
        text;


    row.appendChild(bubble);

    chatMessages.appendChild(row);

    chatMessages.scrollTop =
        chatMessages.scrollHeight;

}


// =========================
// SEND QUESTION TO BACKEND
// =========================

async function sendMessage(presetText) {

    const question =
        (presetText ?? questionInput.value).trim();


    if (!question) return;


    // Make sure video is loaded first
    if (!videoLoaded) {

        alert(
            "Please load a YouTube video first."
        );

        return;

    }


    // Remove welcome message
    if (welcomeMessage) {

        welcomeMessage.remove();

    }


    // Show user's question
    addMessage(
        question,
        "user"
    );


    questionInput.value = "";


    // Disable button while waiting
    sendBtn.disabled = true;


    // Temporary loading message
    const loadingRow =
        document.createElement("div");

    loadingRow.className =
        "msg-row bot";


    const loadingBubble =
        document.createElement("div");

    loadingBubble.className =
        "msg-bubble";

    loadingBubble.textContent =
        "Thinking...";


    loadingRow.appendChild(
        loadingBubble
    );

    chatMessages.appendChild(
        loadingRow
    );


    chatMessages.scrollTop =
        chatMessages.scrollHeight;


    try {

        // Send question to FastAPI
        const response = await fetch(
            `${API_BASE_URL}/chat`,
            {
                method: "POST",

                headers: {
                    "Content-Type": "application/json"
                },

                body: JSON.stringify({
                    question: question
                })
            }
        );


        const data =
            await response.json();


        // Remove "Thinking..."
        loadingRow.remove();


        if (!data.success) {

            throw new Error(
                data.message ||
                "Something went wrong."
            );

        }


        // Display actual LLM answer
        addMessage(
            data.answer,
            "bot"
        );


        // Useful for debugging
        console.log(
            "Retrieved context:",
            data.context
        );


    } catch (error) {

        console.error(
            "Chat error:",
            error
        );


        loadingRow.remove();


        addMessage(
            "Sorry, I couldn't generate an answer. " +
            error.message,
            "bot"
        );

    } finally {

        sendBtn.disabled = false;

        questionInput.focus();

    }

}