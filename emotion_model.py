
from pathlib import Path

import numpy as np
import onnxruntime as ort
from tokenizers import Tokenizer

MODEL_DIR = Path(__file__).resolve().parent / "models" / "emotion-onnx"

LABELS = [
    "anger",
    "disgust",
    "fear",
    "joy",
    "neutral",
    "sadness",
    "surprise",
]

tokenizer = None
session = None


def get_model():
    global tokenizer, session

    if session is None:
        tokenizer = Tokenizer.from_file(
            str(MODEL_DIR / "tokenizer.json")
        )
        tokenizer.enable_truncation(max_length=128)

        session = ort.InferenceSession(
            str(MODEL_DIR / "model-int8.onnx"),
            sess_options=ort.SessionOptions(),
            providers=["CPUExecutionProvider"],
        )

    return tokenizer, session


def detect_emotion(text):
    current_tokenizer, current_session = get_model()

    encoding = current_tokenizer.encode(text)

    input_ids = np.array(
        [encoding.ids], dtype=np.int64
    )
    attention_mask = np.array(
        [encoding.attention_mask], dtype=np.int64
    )

    model_inputs = {
        "input_ids": input_ids,
        "attention_mask": attention_mask,
    }

    required_inputs = {
        item.name for item in current_session.get_inputs()
    }

    model_inputs = {
        name: value
        for name, value in model_inputs.items()
        if name in required_inputs
    }

    logits = current_session.run(
        None, model_inputs
    )[0][0]

    probabilities = np.exp(logits - np.max(logits))
    probabilities /= probabilities.sum()

    index = int(np.argmax(probabilities))

    return {
        "emotion": LABELS[index],
        "confidence": round(
            float(probabilities[index]), 4
        ),
    }
