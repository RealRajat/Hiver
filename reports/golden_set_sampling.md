# Golden Set Sampling Report

## Sampling Method
- **Source Corpus**: `data/processed/applesupport_conversations.jsonl`
- **Sampling Strategy**: Random sample of the first customer message using a fixed random seed (`seed=42`).
- **Exclusions**: Messages shorter than 10 characters were excluded to filter out tiny noise (e.g., "hi").
- **Candidate Population**: 80670 valid first-customer messages.
- **Final Sample Size**: 200 examples placed in the queue.

## Annotation Workflow
The 200 examples have been exported to `data/evaluation/golden_annotation_queue.csv` for manual human review.
- **Automated Labels**: Discarded. No LLM or heuristic was used to generate intent labels.
- **Status**: Currently pending human annotation.

## Intent Distribution
*(Pending human annotation)*

## Ambiguity
*(Pending human annotation)*
