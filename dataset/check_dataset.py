import json

with open("dataset/logic_puzzle_dataset_1000.json") as f:
    data = json.load(f)

print("Total records:", len(data))
print("Sample record:\n", data[0])
