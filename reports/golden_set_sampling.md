# Golden Set Sampling Report

## Sampling Method
- **Source Corpus**: `data/processed/applesupport_conversations.jsonl`
- **Sampling Strategy**: Random sample of the first customer message using a fixed random seed (`seed=42`).
- **Exclusions**: Messages shorter than 10 characters were excluded to filter out tiny noise (e.g., "hi").
- **Candidate Population**: 80670 valid first-customer messages.
- **Final Sample Size**: 200 examples placed in the queue.

## Annotation Workflow
The 200 examples were initially labeled using an AI drafting process (`golden_annotation_ai_draft.csv`). Because the dataset must be human-labelled ground truth, the AI-generated labels were programmatically reviewed and placed into `data/evaluation/golden_annotation_review_queue.csv` with the explicit `annotation_source = ai_draft` marker.
- **Automated Labels**: Pre-populated by an AI tool for review.
- **Status**: Currently pending human approval. The labels cannot be considered ground truth until explicitly reviewed and marked `human_reviewed`.

## Intent Distribution
*(Pending human annotation)*

## Ambiguity
*(Pending human annotation)*
