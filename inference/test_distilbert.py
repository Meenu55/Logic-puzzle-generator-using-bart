import torch
import pickle
from pathlib import Path
from transformers import DistilBertTokenizerFast, DistilBertForSequenceClassification

# Resolve paths relative to this file's location
ROOT = Path(__file__).resolve().parent.parent
MODEL_PATH = ROOT / "models" / "distilbert"
CHECKPOINT_PATH = MODEL_PATH / "checkpoint-300"
LABEL_ENCODER_PATH = ROOT / "training" / "label_encoder.pkl"

# Load tokenizer
tokenizer = DistilBertTokenizerFast.from_pretrained(str(MODEL_PATH))

# Load trained model (FINAL CHECKPOINT)
model = DistilBertForSequenceClassification.from_pretrained(str(CHECKPOINT_PATH))

# Load label encoder
with open(LABEL_ENCODER_PATH, "rb") as f:
    label_encoder = pickle.load(f)

model.eval()

# Test input
text = "Generate a medium seating arrangement puzzle"

inputs = tokenizer(text, return_tensors="pt", truncation=True, padding=True)

with torch.no_grad():
    outputs = model(**inputs)
    prediction = torch.argmax(outputs.logits, dim=1)

label = label_encoder.inverse_transform(prediction.numpy())

print("Input:", text)
print("Predicted label:", label[0])
