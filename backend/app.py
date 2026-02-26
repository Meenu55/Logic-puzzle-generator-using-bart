from flask import Flask, request, jsonify
from flask_cors import CORS
import torch
import pickle
from transformers import DistilBertTokenizerFast, DistilBertForSequenceClassification

app = Flask(__name__)
CORS(app)

# Load DistilBERT tokenizer and model
tokenizer = DistilBertTokenizerFast.from_pretrained("models/distilbert")
model = DistilBertForSequenceClassification.from_pretrained(
    "models/distilbert/checkpoint-300"
)

# Load label encoder
with open("training/label_encoder.pkl", "rb") as f:
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

    # If puzzle_type and difficulty are provided, use them directly
    if puzzle_type and difficulty:
        # Lookup puzzle from dataset
        import json
        with open("dataset/bert_dataset.json", "r", encoding="utf-8") as f:
            dataset = json.load(f)
        # Find a matching puzzle
        filtered = [item for item in dataset if item["puzzle_type"] == puzzle_type and item["difficulty"] == difficulty]
        if filtered:
            puzzle = filtered[0]["puzzle"]
            answer = filtered[0]["answer"]
        else:
            puzzle = "No puzzle found for this type and difficulty."
            answer = "N/A"
        return jsonify({
            "puzzle_type": puzzle_type,
            "difficulty": difficulty,
            "puzzle": puzzle,
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
        # Lookup puzzle from dataset
        import json
        with open("dataset/bert_dataset.json", "r", encoding="utf-8") as f:
            dataset = json.load(f)
        filtered = [item for item in dataset if item["puzzle_type"] == puzzle_type and item["difficulty"] == difficulty]
        if filtered:
            puzzle = filtered[0]["puzzle"]
            answer = filtered[0]["answer"]
        else:
            puzzle = "No puzzle found for this type and difficulty."
            answer = "N/A"
        return jsonify({
            "puzzle_type": puzzle_type,
            "difficulty": difficulty,
            "puzzle": puzzle,
            "answer": answer
        })

if __name__ == "__main__":
    app.run(debug=True)
