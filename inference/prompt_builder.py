def build_prompt(puzzle_type, difficulty):
    prompt = f"""
Generate a {difficulty.lower()} level {puzzle_type.lower()} logic puzzle.

Rules:
- Puzzle must be logically solvable
- Difficulty must strictly match the level
- Provide a clear puzzle statement
- Provide exactly one correct answer

Output format:
Puzzle:
<problem>

Answer:
<solution>
"""
    return prompt
