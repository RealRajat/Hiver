# Golden Set Sampling Report

## Sampling Method
- **Source Corpus**: `data/processed/applesupport_conversations.jsonl`
- **Sampling Strategy**: Random sample of the first customer message using a fixed random seed (`seed=42`).
- **Exclusions**: Messages shorter than 10 characters were excluded to filter out tiny noise (e.g., "hi").
- **Candidate Population**: 80670 valid first-customer messages.
- **Final Sample Size**: 200 examples placed in the queue.

## Annotation Workflow
Because human annotators were not utilized for this assignment, the 200 examples were semantically evaluated by the assistant (`data/evaluation/golden_set_assistant_annotated.csv`) with the explicit `annotation_source = assistant_annotated` marker.
- **Status**: The dataset is functionally complete for evaluation but explicitly fails the assignment's human hand-labelled requirement.

## Intent Distribution
- Software Bug / Glitch: 68
- Device Performance / Hardware: 57
- General Complaint / Venting (Other): 34
- Services & Account: 15
- How-To / Feature Question: 14
- Purchase & Store Operations: 12

## Ambiguity
- Ambiguous: 32
- Unambiguous: 168
