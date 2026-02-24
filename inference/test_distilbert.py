import torch
import pickle
from transformers import DistilBertTokenizerFast, DistilBertForSequenceClassification

# Load tokenizer
tokenizer = DistilBertTokenizerFast.from_pretrained("models/distilbert")

# Load trained model (FINAL CHECKPOINT)
model = DistilBertForSequenceClassification.from_pretrained(
    "models/distilbert/checkpoint-300"
)

# Load label encoder
with open("training/label_encoder.pkl", "rb") as f:
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
