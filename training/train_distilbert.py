import json
import torch
from torch.utils.data import Dataset
from transformers import DistilBertTokenizerFast, DistilBertForSequenceClassification, Trainer, TrainingArguments
from sklearn.preprocessing import LabelEncoder

# Load training data (single BERT dataset)
with open("dataset/bert_dataset.json", encoding="utf-8") as f:
    data = json.load(f)

texts = [item["instruction"] for item in data]
labels = [f'{item["puzzle_type"]}_{item["difficulty"]}' for item in data]

# Encode labels
label_encoder = LabelEncoder()
encoded_labels = label_encoder.fit_transform(labels)

# Save label mapping
import pickle
with open("training/label_encoder.pkl", "wb") as f:
    pickle.dump(label_encoder, f)

# Dataset class
class PuzzleDataset(Dataset):
    def __init__(self, texts, labels, tokenizer):
        self.encodings = tokenizer(texts, truncation=True, padding=True)
        self.labels = labels

    def __getitem__(self, idx):
        item = {key: torch.tensor(val[idx]) for key, val in self.encodings.items()}
        item["labels"] = torch.tensor(self.labels[idx])
        return item

    def __len__(self):
        return len(self.labels)

# Tokenizer
tokenizer = DistilBertTokenizerFast.from_pretrained("distilbert-base-uncased")

dataset = PuzzleDataset(texts, encoded_labels, tokenizer)

# Model
model = DistilBertForSequenceClassification.from_pretrained(
    "distilbert-base-uncased",
    num_labels=len(label_encoder.classes_)
)

# Training arguments
training_args = TrainingArguments(
    output_dir="models/distilbert",
    num_train_epochs=3,
    per_device_train_batch_size=8,
    logging_steps=10,
    save_steps=500,
    save_total_limit=2,
    report_to="none"
)


# Trainer
trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=dataset
)

# Train
trainer.train()

# Save model
trainer.save_model("models/distilbert")
tokenizer.save_pretrained("models/distilbert")

print("✅ DistilBERT training completed and model saved.")
