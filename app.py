
from flask import Flask, jsonify, request, render_template
from emotion_model import detect_emotion

app = Flask(__name__)

EMOTIONS = {
    "joy": {
        "name": "Радість",
        "emoji": "😊",
        "advice": "Чудово! Насолоджуйся позитивними моментами."
    },
    "sadness": {
        "name": "Сум",
        "emoji": "😢",
        "advice": "Дай собі час на відпочинок і підтримку."
    },
    "anger": {
        "name": "Гнів",
        "emoji": "😠",
        "advice": "Спробуй зробити паузу та заспокоїтися."
    },
    "fear": {
        "name": "Страх",
        "emoji": "😨",
        "advice": "Спробуй зосередитися на тому, що можеш контролювати."
    },
    "surprise": {
        "name": "Здивування",
        "emoji": "😲",
        "advice": "Нові враження можуть бути цікавими!"
    },
    "disgust": {
        "name": "Відраза",
        "emoji": "🤢",
        "advice": "Зверни увагу на власні відчуття та межі."
    },
    "neutral": {
        "name": "Нейтральна",
        "emoji": "😐",
        "advice": "Спокійний стан теж може бути корисним."
    }
}

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/analyze", methods=["POST"])
def analyze_emotion():
    data = request.get_json(silent=True)

    if not isinstance(data, dict):
        return jsonify({"error": "Invalid JSON data"}), 400

    text = data.get("text")

    if not isinstance(text, str) or not text.strip():
        return jsonify({"error": "Please enter some text"}), 400

    try:
        result = detect_emotion(text.strip())

        emotion = result["emotion"]
        details = EMOTIONS.get(emotion, EMOTIONS["neutral"])

        return jsonify({
            "text": text.strip(),
            "emotion": emotion,
            "emotion_uk": details["name"],
            "emoji": details["emoji"],
            "confidence": result["confidence"],
            "advice": details["advice"]
        })

    except Exception:
        app.logger.exception("Emotion analysis failed")
        return jsonify({"error": "Emotion analysis failed"}), 500


if __name__ == "__main__":
    app.run(debug=True)
