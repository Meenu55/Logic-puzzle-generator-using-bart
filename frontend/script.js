async function generatePuzzle() {
    const instruction = document.getElementById("instruction").value;
    const puzzleType = document.getElementById("puzzleType").value;
    const difficulty = document.getElementById("difficulty").value;

    if (!instruction || !puzzleType || !difficulty) {
        alert("Please enter all fields: instruction, puzzle type, and difficulty.");
        return;
    }

    const loader = document.getElementById("loader");
    const output = document.getElementById("output");
    const puzzleText = document.getElementById("puzzleText");
    const answerText = document.getElementById("answerText");
    const answerBox = document.getElementById("answerBox");

    output.classList.add("hidden");
    answerBox.classList.add("hidden");
    loader.classList.remove("hidden");

    try {
        const response = await fetch("http://127.0.0.1:5000/generate", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({
                input: instruction,
                puzzle_type: puzzleType,
                difficulty: difficulty
            })
        });

        const data = await response.json();

        puzzleText.innerText = data.puzzle;
        answerText.innerText = data.answer;

        loader.classList.add("hidden");
        output.classList.remove("hidden");

    } catch (error) {
        loader.classList.add("hidden");
        alert("Backend is not running. Please start the server.");
    }
}
function toggleAnswer() {
    document.getElementById("answerBox").classList.toggle("hidden");
}
