import torch
import pickle
from transformers import DistilBertTokenizerFast, DistilBertForSequenceClassification
from prompt_builder import build_prompt

# Load DistilBERT
tokenizer = DistilBertTokenizerFast.from_pretrained("models/distilbert")
model = DistilBertForSequenceClassification.from_pretrained(
    "models/distilbert/checkpoint-300"
)

with open("training/label_encoder.pkl", "rb") as f:
    label_encoder = pickle.load(f)

model.eval()

# User input
user_input = "I want a medium seating arrangement puzzle"

# Classify input
inputs = tokenizer(user_input, return_tensors="pt", truncation=True, padding=True)

with torch.no_grad():
    outputs = model(**inputs)
    prediction = torch.argmax(outputs.logits, dim=1)

label = label_encoder.inverse_transform(prediction.numpy())[0]
puzzle_type, difficulty = label.split("_")

# Build prompt
prompt = build_prompt(puzzle_type, difficulty)

print("=== GENERATED PROMPT SENT TO LLM ===")
print(prompt)

# LLM generation placeholder
print("\n=== LLM OUTPUT ===")
print("Puzzle:\nFive people A, B, C, D, E are sitting in a row...\n\nAnswer:\nC")
