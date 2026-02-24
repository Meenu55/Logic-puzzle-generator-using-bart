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

# TEMPORARY generator (BART will replace this)
def generate_puzzle(prompt):
    return {
        "puzzle": "Five people A, B, C, D, E are sitting in a row. C is in the middle.",
        "answer": "C"
    }

@app.route("/generate", methods=["POST"])
def generate():
    data = request.json
    user_input = data.get("input", "")

    inputs = tokenizer(user_input, return_tensors="pt", truncation=True, padding=True)

    with torch.no_grad():
        outputs = model(**inputs)
        prediction = torch.argmax(outputs.logits, dim=1)

    label = label_encoder.inverse_transform(prediction.numpy())[0]
    puzzle_type, difficulty = label.split("_")

    prompt = build_prompt(puzzle_type, difficulty)
    result = generate_puzzle(prompt)

    return jsonify({
        "puzzle_type": puzzle_type,
        "difficulty": difficulty,
        "puzzle": result["puzzle"],
        "answer": result["answer"]
    })

if __name__ == "__main__":
    app.run(debug=True)
