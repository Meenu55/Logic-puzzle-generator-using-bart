import json
import random

puzzle_templates = {
    "Seating Arrangement": [
        "Five people A, B, C, D, E are sitting in a row. A sits to the left of B. C is in the middle.",
        "Six people are sitting in a circle. A sits opposite D. B is between A and C."
    ],
    "Logical Reasoning": [
        "If all cats are animals and some animals are pets, can we conclude all cats are pets?",
        "If today is Monday, what day will it be after 61 days?"
    ],
    "Number Logic": [
        "Find the next number in the series: 2, 6, 12, 20, ?",
        "Find the missing number: 3, 7, 15, 31, ?"
    ],
    "Direction Sense": [
        "A man walks 5 km north, then turns right and walks 3 km.",
        "Ravi walks east, then turns left and walks north."
    ],
    "Blood Relation": [
        "Pointing to a man, Rita said, 'He is the son of my grandfather.'",
        "John is the brother of Mary's father."
    ],
    "Coding-Decoding": [
        "If CAT is coded as DBU, how is DOG coded?",
        "If APPLE is coded as ELPPA, how is MANGO coded?"
    ],
    "Syllogism": [
        "All pens are books. Some books are papers.",
        "No car is bike. Some bikes are cycles."
    ],
    "Alphabet Series": [
        "A, C, F, J, ?",
        "Z, X, U, Q, ?"
    ],
    "Clock": [
        "At what time between 2 and 3 will the hands of a clock overlap?",
        "Find the angle between clock hands at 3:30."
    ],
    "Logical Deduction": [
        "A is taller than B. B is taller than C.",
        "D is older than A but younger than B."
    ]
}

difficulties = ["Easy", "Medium", "Hard"]

dataset = []

for i in range(1000):
    puzzle_type = random.choice(list(puzzle_templates.keys()))
    difficulty = random.choice(difficulties)
    puzzle = random.choice(puzzle_templates[puzzle_type])

    record = {
        "instruction": f"Generate a {difficulty.lower()} {puzzle_type.lower()} puzzle",
        "puzzle_type": puzzle_type,
        "difficulty": difficulty,
        "puzzle": puzzle,
        "question": "Solve the puzzle logically.",
        "answer": "Answer derived logically"
    }

    dataset.append(record)

with open("dataset/logic_puzzle_dataset_1000.json", "w") as f:
    json.dump(dataset, f, indent=2)

print("✅ Dataset with 1000 records created successfully!")
