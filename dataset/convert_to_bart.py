import json

# Load original dataset
with open("logic_puzzle_dataset_1000.json","r") as f:
    data = json.load(f)

bart_data = []

for item in data:

    input_text = item["instruction"]

    target_text = (
        "Puzzle: " + item["puzzle"] +
        " Question: " + item["question"] +
        " Answer: " + item["answer"]
    )

    bart_data.append({

        "input_text": input_text,
        "target_text": target_text

    })


# Save BART dataset
with open("../training/bart_dataset.json","w") as f:

    json.dump(bart_data,f,indent=2)


print("✅ BART dataset created successfully")