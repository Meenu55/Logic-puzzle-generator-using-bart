import json

with open("logic_puzzle_dataset_1000.json") as f:
    data = json.load(f)


for item in data:

    ptype = item["puzzle_type"].lower()


    if "alphabet" in ptype:

        item["question"] = "Find the next letter in the series."

    elif "number" in ptype:

        item["question"] = "Find the missing number."

    elif "coding" in ptype:

        item["question"] = "Decode the pattern and find the answer."

    elif "clock" in ptype:

        item["question"] = "Find the correct time."

    elif "direction" in ptype:

        item["question"] = "Find the final position."

    elif "age" in ptype:

        item["question"] = "Find the age."

    elif "blood" in ptype:

        item["question"] = "Find the relationship."

    elif "seating" in ptype:

        item["question"] = "Determine the correct arrangement."

    else:

        item["question"] = "Solve the puzzle."


with open("logic_puzzle_dataset_1000_fixed.json","w") as f:

    json.dump(data,f,indent=2)


print("✅ Questions improved")