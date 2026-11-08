
const form = document.getElementById("emotionForm");
const textInput = document.getElementById("textInput");
const analyzeBtn = document.getElementById("analyzeBtn");
const status = document.getElementById("status");
const result = document.getElementById("result");

form.addEventListener("submit", async function (event) {
    event.preventDefault();

    const text = textInput.value.trim();

    if (!text) {
        status.textContent = "Будь ласка, введіть текст.";
        return;
    }

    result.classList.add("hidden");
    analyzeBtn.disabled = true;
    status.textContent = "Штучний інтелект аналізує текст...";

    try {
        const response = await fetch("/analyze", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({ text: text })
        });

        const data = await response.json();

        if (!response.ok) {
            throw new Error(data.error || "Помилка аналізу");
        }

        document.getElementById("emotionEmoji").textContent = data.emoji;
        document.getElementById("emotionName").textContent = data.emotion_uk;
        document.getElementById("confidence").textContent =
            "Впевненість моделі: " +
            (data.confidence * 100).toFixed(2) + "%";
        document.getElementById("advice").textContent = data.advice;

        result.classList.remove("hidden");
        status.textContent = "";
    } catch (error) {
        status.textContent = "Помилка: " + error.message;
    } finally {
        analyzeBtn.disabled = false;
    }
});
