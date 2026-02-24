import json
import random

with open("dataset/logic_puzzle_dataset_1000.json") as f:
    data = json.load(f)

random.shuffle(data)

split = int(0.8 * len(data))
train_data = data[:split]
test_data = data[split:]

with open("dataset/train.json", "w") as f:
    json.dump(train_data, f, indent=2)

with open("dataset/test.json", "w") as f:
    json.dump(test_data, f, indent=2)

print("Train size:", len(train_data))
print("Test size:", len(test_data))
