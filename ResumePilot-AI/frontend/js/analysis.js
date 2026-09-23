const steps = [
  ...document.querySelectorAll(".timeline-item")
];

const bar =
  document.getElementById("progressBar");

const progressText =
  document.getElementById("progressText");


// --------------------------------------------------
// Check whether real analysis exists
// --------------------------------------------------

const storedResult =
  sessionStorage.getItem("analysisResult");


// If user directly opens analysis.html
// without analyzing anything first
if (!storedResult) {

  window.location.href =
    "analyze.html";
}


// --------------------------------------------------
// Analysis Animation
// --------------------------------------------------

let current = 0;

const stepProgress = [
  18,
  38,
  60,
  82,
  100
];


function update() {

  // ----------------------------------------------
  // Mark previous step as completed
  // ----------------------------------------------

  if (current > 0) {

    steps[current - 1]
      .classList.remove("active");

    steps[current - 1]
      .classList.add("done");
  }


  // ----------------------------------------------
  // Activate current step
  // ----------------------------------------------

  if (current < steps.length) {

    steps[current]
      .classList.add("active");

    const dot =
      steps[current]
        .querySelector(".timeline-dot");

    if (dot) {

      dot.textContent = "•";
    }
  }


  // ----------------------------------------------
  // Update progress
  // ----------------------------------------------

  const progress =
    stepProgress[current];

  bar.style.width =
    `${progress}%`;

  progressText.textContent =
    `${progress}%`;


  current++;


  // ----------------------------------------------
  // Continue animation
  // ----------------------------------------------

  if (current < steps.length) {

    setTimeout(
      update,
      700
    );

  } else {

    // Complete final step
    setTimeout(
      () => {

        // Make sure the final step is marked done
        if (steps.length > 0) {

          steps[steps.length - 1]
            .classList.remove("active");

          steps[steps.length - 1]
            .classList.add("done");
        }


        // Go to real results
        setTimeout(
          () => {

            window.location.href =
              "results.html";

          },
          500
        );

      },
      700
    );
  }
}


// Start animation
setTimeout(
  update,
  500
);