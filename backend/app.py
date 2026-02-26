from flask import Flask, request, jsonify
from flask_cors import CORS
import torch
import pickle
import json
from pathlib import Path
from transformers import DistilBertTokenizerFast, DistilBertForSequenceClassification

app = Flask(__name__)
CORS(app)

# Resolve paths relative to this file's location
ROOT = Path(__file__).resolve().parent.parent
MODEL_PATH = ROOT / "models" / "distilbert"
CHECKPOINT_PATH = MODEL_PATH / "checkpoint-300"
LABEL_ENCODER_PATH = ROOT / "training" / "label_encoder.pkl"
DATASET_PATH = ROOT / "dataset" / "bert_dataset.json"

print("Loading DistilBERT tokenizer...")
tokenizer = DistilBertTokenizerFast.from_pretrained(str(MODEL_PATH))
print("Loading DistilBERT model...")
model = DistilBertForSequenceClassification.from_pretrained(str(CHECKPOINT_PATH))

print("Loading label encoder...")
with open(LABEL_ENCODER_PATH, "rb") as f:
    label_encoder = pickle.load(f)

model.eval()

# Prompt builder
def build_prompt(puzzle_type, difficulty):
    return f"""
Generate a {difficulty.lower()} level {puzzle_type.lower()} logic puzzle.

Rules:
- Logically solvable
- One correct answer
- Clear explanation
"""


@app.route("/generate", methods=["POST"])
def generate():
    data = request.json
    user_input = data.get("input", "")
    puzzle_type = data.get("puzzle_type", "")
    difficulty = data.get("difficulty", "")

    try:
        # Load dataset
        with open(DATASET_PATH, "r", encoding="utf-8") as f:
            dataset = json.load(f)

        # If puzzle_type and difficulty are provided, use them directly
        if puzzle_type and difficulty:
            # Find a matching puzzle
            filtered = [item for item in dataset if item["puzzle_type"] == puzzle_type and item["difficulty"] == difficulty]
            if filtered:
                puzzle = filtered[0].get("puzzle", "")
                answer = filtered[0].get("answer", "")
                question = filtered[0].get("question", "")
            else:
                puzzle = "No puzzle found for this type and difficulty."
                answer = "N/A"
                question = ""
            return jsonify({
                "puzzle_type": puzzle_type,
                "difficulty": difficulty,
                "puzzle": puzzle,
                "question": question,
                "answer": answer
            })
        else:
            # Fallback: use BERT classifier
            inputs = tokenizer(user_input, return_tensors="pt", truncation=True, padding=True)
            with torch.no_grad():
                outputs = model(**inputs)
                prediction = torch.argmax(outputs.logits, dim=1)
            label = label_encoder.inverse_transform(prediction.numpy())[0]
            puzzle_type, difficulty = label.split("_")
            
            filtered = [item for item in dataset if item["puzzle_type"] == puzzle_type and item["difficulty"] == difficulty]
            if filtered:
                puzzle = filtered[0].get("puzzle", "")
                answer = filtered[0].get("answer", "")
                question = filtered[0].get("question", "")
            else:
                puzzle = "No puzzle found for this type and difficulty."
                answer = "N/A"
                question = ""
            return jsonify({
                "puzzle_type": puzzle_type,
                "difficulty": difficulty,
                "puzzle": puzzle,
                "question": question,
                "answer": answer
            })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5050, debug=True)
