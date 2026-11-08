
from transformers import pipeline

MODEL_NAME = "j-hartmann/emotion-english-distilroberta-base"

emotion_classifier = None


def get_classifier():
    global emotion_classifier

    if emotion_classifier is None:
        emotion_classifier = pipeline(
            task="text-classification",
            model=MODEL_NAME,
            device=-1
        )

    return emotion_classifier


def detect_emotion(text):
    classifier = get_classifier()

    result = classifier(text, truncation=True)[0]

    return {
        "emotion": result["label"],
        "confidence": round(result["score"], 4)
    }


if __name__ == "__main__":
    text = "I am very happy today!"
    result = detect_emotion(text)

    print("Text:", text)
    print("Emotion:", result["emotion"])
    print("Confidence:", result["confidence"])
