async function generatePuzzle() {
    const instruction = document.getElementById("instruction").value;
    const puzzleType = document.getElementById("puzzleType").value;
    const difficulty = document.getElementById("difficulty").value;

    if (!instruction || !puzzleType || !difficulty) {
        alert("Please enter all fields: instruction, puzzle type, and difficulty.");
        return;
    }

    const loader = document.getElementById("loader");
    const modal = document.getElementById("puzzleModal");
    const answerBox = document.getElementById("modalAnswerBox");

    loader.classList.remove("hidden");

    try {
        const response = await fetch("http://127.0.0.1:5050/generate", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({
                input: instruction,
                puzzle_type: puzzleType,
                difficulty: difficulty
            })
        });

        const data = await response.json();

        // populate modal content
        document.getElementById("modalPuzzleText").innerText = data.puzzle || "";
        document.getElementById("modalQuestionText").innerText = data.question || "";
        document.getElementById("modalAnswerText").innerText = data.answer || "";
        // reset modal answer visibility to hidden
        answerBox.classList.add("hidden");
        document.getElementById("modalShowAnswer").innerText = "Show Answer";

        loader.classList.add("hidden");
        // show modal and prevent page scroll
        modal.classList.remove("hidden");
        document.body.style.overflow = "hidden";

    } catch (error) {
        loader.classList.add("hidden");
        alert("Backend is not running. Please start the server.");
    }
}
function toggleAnswer() {
    document.getElementById("answerBox").classList.toggle("hidden");
}

// Modal controls
document.addEventListener("DOMContentLoaded", () => {
    const modal = document.getElementById("puzzleModal");
    const closeBtn = document.getElementById("closeModal");
    const showBtn = document.getElementById("modalShowAnswer");
    const answerBox = document.getElementById("modalAnswerBox");

    if (closeBtn) {
        closeBtn.addEventListener("click", () => {
            modal.classList.add("hidden");
            document.body.style.overflow = "auto";
        });
    }

    // Toggle answer inside modal
    if (showBtn) {
        showBtn.addEventListener("click", (e) => {
            e.preventDefault();
            e.stopPropagation();
            if (answerBox.classList.contains("hidden")) {
                answerBox.classList.remove("hidden");
                showBtn.innerText = "Hide Answer";
            } else {
                answerBox.classList.add("hidden");
                showBtn.innerText = "Show Answer";
            }
        });
    }

    // Close on Escape
    document.addEventListener("keydown", (e) => {
        if (e.key === "Escape" && !modal.classList.contains("hidden")) {
            modal.classList.add("hidden");
            document.body.style.overflow = "auto";
        }
    });
});
