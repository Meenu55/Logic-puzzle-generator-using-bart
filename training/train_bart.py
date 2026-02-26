import json
from datasets import Dataset
from transformers import BartTokenizer, BartForConditionalGeneration, Trainer, TrainingArguments

# Load BART dataset (converted from bert_dataset.json)
with open("training/bart_dataset.json", encoding='utf-8') as f:
    data = json.load(f)

dataset = Dataset.from_list(data)

tokenizer = BartTokenizer.from_pretrained("facebook/bart-base")

def tokenize_function(example):
    inputs = tokenizer(
        example["input_text"],
        padding="max_length",
        truncation=True,
        max_length=256
    )
    with tokenizer.as_target_tokenizer():
        labels = tokenizer(
            example["target_text"],
            padding="max_length",
            truncation=True,
            max_length=256
        )
    inputs["labels"] = labels["input_ids"]
    return inputs

tokenized_dataset = dataset.map(tokenize_function, batched=False)

model = BartForConditionalGeneration.from_pretrained("facebook/bart-base")

training_args = TrainingArguments(
    output_dir="./bart_model",
    per_device_train_batch_size=4,
    num_train_epochs=3,
    logging_steps=50,
    save_strategy="epoch",
    evaluation_strategy="no",
    fp16=False,
    report_to="none"
)

trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=tokenized_dataset
)

trainer.train()

model.save_pretrained("./bart_model")
tokenizer.save_pretrained("./bart_model")

print("✅ BART training completed and model saved to ./bart_model")
