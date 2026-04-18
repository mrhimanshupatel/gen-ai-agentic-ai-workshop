# Example Comparison Notebook - Concepts Covered

## 1) Notebook Goal
This notebook demonstrates interactive experimentation with utility functions from `text_utils.py` and compares notebook workflows with regular Python scripts.

## 2) Reusable Module Pattern
The notebook imports functions from a separate module:
- `clean_text`
- `count_words`
- `get_text_stats`

Concept covered:
- Keep logic in `.py` files for reuse and maintainability.
- Use `.ipynb` for exploration and demonstration.

## 3) Text Processing Concepts Demonstrated
Using multiple examples, the notebook shows:
- basic normalization/cleaning of text
- word counting
- descriptive text statistics (through `get_text_stats`)
- comparison across different sample inputs

## 4) Interactive Exploration Workflow
The notebook highlights iterative analysis:
1. Define sample text.
2. Run utility functions.
3. Inspect output immediately.
4. Try another example with changed input.

This supports fast hypothesis testing in NLP experiments.

## 5) Formatted Output for Readability
The notebook prints structured outputs (key-value stats) using loop-based formatting.

Concept covered:
- presenting exploratory results clearly matters for interpretation and debugging.

## 6) Multi-Example Comparison
A list of sample texts is processed in a loop to compare:
- word count differences
- average word length behavior

Concept covered:
- lightweight batch-style comparison without building a full pipeline.

## 7) Notebook vs Script Tradeoff (Explicitly Covered)
The notebook includes a direct comparison:

For `.py` (`text_utils.py`):
- reusable and importable code
- better for testing and version control
- no persisted rich output

For `.ipynb`:
- inline outputs and documentation
- interactive and visual exploration
- useful for demos, learning, and experimentation

## 8) Practical Learning Outcome
By the end, the learner understands how to combine:
- production-style reusable functions in modules
- experimentation-style analysis in notebooks

This is a common and effective workflow in NLP/GenAI projects.
