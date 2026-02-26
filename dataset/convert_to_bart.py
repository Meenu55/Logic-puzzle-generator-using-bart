import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
IN = ROOT / "bert_dataset.json"
OUT = ROOT.parent / "training" / "bart_dataset.json"

def main():
    with open(IN, encoding='utf-8') as f:
        data = json.load(f)

    bart_data = []
    for item in data:
        input_text = item.get("instruction", "")
        target_text = (
            "Puzzle: " + item.get("puzzle", "") + "\n"
            + "Question: " + item.get("question", "") + "\n"
            + "Answer: " + item.get("answer", "")
        )
        bart_data.append({"input_text": input_text, "target_text": target_text})

    OUT.parent.mkdir(parents=True, exist_ok=True)
    with open(OUT, "w", encoding='utf-8') as f:
        json.dump(bart_data, f, indent=2, ensure_ascii=False)

    print(f"Wrote {len(bart_data)} records to {OUT}")

if __name__ == '__main__':
    main()
