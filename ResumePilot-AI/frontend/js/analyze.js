const form = document.getElementById("analyzeForm");
const fileInput = document.getElementById("resumeFile");
const dropZone = document.getElementById("dropZone");
const fileName = document.getElementById("fileName");
const uploadTitle = document.getElementById("uploadTitle");
const uploadText = document.getElementById("uploadText");
const jd = document.getElementById("jobDescription");
const charCount = document.getElementById("charCount");


// Backend API
const API_URL = "http://127.0.0.1:8000/api/analyze";


// --------------------------------------------------
// File Upload
// --------------------------------------------------

function showFile(file) {

  if (!file) return;

  const allowed = [".pdf", ".docx", ".txt"];

  const ext =
    "." +
    file.name
      .split(".")
      .pop()
      .toLowerCase();

  if (!allowed.includes(ext)) {

    alert(
      "Please upload a PDF, DOCX or TXT file."
    );

    return;
  }

  if (file.size > 5 * 1024 * 1024) {

    alert(
      "File must be smaller than 5 MB."
    );

    return;
  }

  fileName.textContent = file.name;

  uploadTitle.textContent =
    "Resume ready";

  uploadText.textContent =
    "Click to choose a different file";

  dropZone.classList.add("dragging");
}


// File picker
fileInput.addEventListener(
  "change",
  (e) => {
    showFile(e.target.files[0]);
  }
);


// --------------------------------------------------
// Drag & Drop
// --------------------------------------------------

["dragenter", "dragover"].forEach(
  (type) => {

    dropZone.addEventListener(
      type,
      (e) => {

        e.preventDefault();

        dropZone.classList.add(
          "dragging"
        );
      }
    );
  }
);


["dragleave", "drop"].forEach(
  (type) => {

    dropZone.addEventListener(
      type,
      (e) => {

        e.preventDefault();

        if (type === "dragleave") {

          dropZone.classList.remove(
            "dragging"
          );
        }
      }
    );
  }
);


dropZone.addEventListener(
  "drop",
  (e) => {

    const file =
      e.dataTransfer.files[0];

    showFile(file);

    // Put dropped file into the file input
    try {

      const dataTransfer =
        new DataTransfer();

      dataTransfer.items.add(file);

      fileInput.files =
        dataTransfer.files;

    } catch (error) {

      console.log(
        "Could not assign dropped file:",
        error
      );
    }
  }
);


// --------------------------------------------------
// Job Description Character Counter
// --------------------------------------------------

jd.addEventListener(
  "input",
  () => {

    charCount.textContent =
      `${jd.value.length.toLocaleString()} / 10,000`;
  }
);


// --------------------------------------------------
// Analyze Resume
// --------------------------------------------------

form.addEventListener(
  "submit",
  async (e) => {

    e.preventDefault();


    // ----------------------------------------------
    // Validate Resume
    // ----------------------------------------------

    const resumeFile =
      fileInput.files[0];

    if (!resumeFile) {

      alert(
        "Please upload your resume first."
      );

      return;
    }


    // ----------------------------------------------
    // Validate Job Description
    // ----------------------------------------------

    const jobDescription =
      jd.value.trim();

    if (jobDescription.length < 80) {

      alert(
        "Please paste a complete job description."
      );

      return;
    }


    // ----------------------------------------------
    // Show loading state
    // ----------------------------------------------

    const submitButton =
      form.querySelector(
        'button[type="submit"]'
      );

    const originalButtonText =
      submitButton
        ? submitButton.textContent
        : "";

    if (submitButton) {

      submitButton.disabled = true;

      submitButton.textContent =
        "Analyzing...";
    }


    try {

      // --------------------------------------------
      // Create multipart/form-data
      // --------------------------------------------

      const formData =
        new FormData();

      formData.append(
        "resume",
        resumeFile
      );

      formData.append(
        "job_description",
        jobDescription
      );


      // --------------------------------------------
      // Send request to FastAPI
      // --------------------------------------------

      const response =
        await fetch(
          API_URL,
          {
            method: "POST",
            body: formData
          }
        );


      // --------------------------------------------
      // Read response
      // --------------------------------------------

      const data =
        await response.json();


      // --------------------------------------------
      // Handle backend errors
      // --------------------------------------------

      if (!response.ok) {

        const message =
          data.detail ||
          "Something went wrong while analyzing the resume.";

        throw new Error(message);
      }


      // --------------------------------------------
      // Save analysis result
      // --------------------------------------------

      sessionStorage.setItem(
        "resumeName",
        resumeFile.name
      );

      sessionStorage.setItem(
        "jobDescription",
        jobDescription
      );

      sessionStorage.setItem(
        "analysisResult",
        JSON.stringify(data)
      );


      // --------------------------------------------
      // Go to analysis page
      // --------------------------------------------

      window.location.href =
        "analysis.html";

    } catch (error) {

      console.error(
        "Analysis error:",
        error
      );

      alert(
        `Analysis failed: ${error.message}`
      );

      if (submitButton) {

        submitButton.disabled =
          false;

        submitButton.textContent =
          originalButtonText;
      }
    }
  }
);