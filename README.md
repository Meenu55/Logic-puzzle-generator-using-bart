
# Logic Puzzle Generator

This project is a logic-puzzle generator that uses a small classifier to pick a puzzle type and difficulty, and a generator model (BART) to produce puzzle statements and solutions. The repository contains: a Flask backend, a simple frontend, dataset utilities, and training scripts.

Core idea
- Users provide a short instruction (for example: "Generate a medium seating arrangement puzzle"), the system classifies the request (puzzle type + difficulty), builds a generation prompt, and produces a puzzle and answer.

What is included
- `frontend/` — static UI (HTML/CSS/JS) to input instructions and view puzzles.
- `backend/` — Flask API (`/generate`) that classifies input and returns a puzzle from the dataset or (after you train BART on HPC) can call the generator.
- `dataset/bert_dataset.json` — single cleaned dataset used for BERT training and conversion to BART format.
- `dataset/convert_to_bart.py` — converts `bert_dataset.json` to `training/bart_dataset.json` for BART training (run on HPC).
- `training/train_distilbert.py` — train the DistilBERT classifier (local or HPC).
- `training/train_bart.py` — BART training script (for HPC only).
- `requirements.txt` — base Python deps for running the app and BERT training.
- `requirements-bart.txt` — minimal deps for BART training on HPC.

Quick start (local development)
1. Create and activate a Python environment, install dependencies:

	```bash
	python -m venv venv
	source venv/bin/activate        # Linux / macOS
	venv\Scripts\activate         # Windows PowerShell
	pip install -r requirements.txt
	```

2. Start the Flask backend (runs on port 5000):

	```bash
	python backend/app.py
	```

3. Serve the frontend (recommended) and open it in a browser:

	```bash
	cd frontend
	python -m http.server 8000
	# then open http://127.0.0.1:8000
	```

4. Use the UI to send an instruction. If you don't select puzzle type/difficulty, the DistilBERT classifier will infer them.

Training notes
- DistilBERT classifier (local or HPC):
  - Script: `training/train_distilbert.py` — reads `dataset/bert_dataset.json`, trains, and saves the model to `models/distilbert` and `training/label_encoder.pkl`.

- BART generator (HPC recommended):
  - Convert dataset on the HPC node: `python dataset/convert_to_bart.py` (writes `training/bart_dataset.json`).
  - Install `requirements-bart.txt` on HPC and run `python training/train_bart.py`.
  - Adjust `training/train_bart.py` hyperparameters (`per_device_train_batch_size`, `num_train_epochs`, `fp16`) to match available GPUs.

Repository hygiene
- Large or generated artifacts are not committed. On the HPC clone, run `python dataset/convert_to_bart.py` to generate `training/bart_dataset.json` before training BART.

If you want, I can create a small SLURM submission script tuned to your cluster or commit these changes to a branch for you.

