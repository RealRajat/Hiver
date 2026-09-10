# Hiver SDE Intern Assignment

## Project Overview
This repository implements the Hiver SDE Intern take-home assignment. It will eventually build and evaluate an AI customer-support agent using the **Customer Support on Twitter** dataset.

## Current Status
`Phase 4 — Evaluation Harness: COMPLETE`

An evaluation harness has been built to benchmark the intent classifier using `data/evaluation/golden_set_annotated.csv`. A simple deterministic baseline classifier has been implemented. (Note: Human/LLM judge agreement for generated replies is not yet implemented).

## Phase 4 — Evaluation Harness
The evaluation harness (`scripts/evaluate_baseline.py`) measures the performance of a minimal keyword-based deterministic baseline classifier against the golden 200-example dataset.
- **Metrics**: Accuracy, Macro P/R/F1, Per-intent P/R/F1, and Confusion Matrix.
- **Ambiguity Handling**: Performance is explicitly reported separately for ambiguous and non-ambiguous examples to provide clarity on model robustness.
- **Commands**: Run `$env:PYTHONPATH="."; python scripts/evaluate_baseline.py` to reproduce the evaluation and view the reports in the `reports/` directory.
- **Limitations**: The current baseline is not production-ready. The golden dataset is assumed to be manually annotated, and LLM-as-judge logic for replies remains an interface stub awaiting future implementation. No fabricated human/LLM agreement scores exist.

## Phase 4 — Historical Evidence Retrieval
A historical evidence retrieval component is built to ground future LLM-drafted responses in actual AppleSupport resolutions, separating retrieval from generation.
- **Corpus**: `data/processed/applesupport_conversations.jsonl`
- **Retrieval Unit**: "Resolution Pairs" consisting of the first customer message and the immediate subsequent support response.
- **Methodology**: Deterministic TF-IDF with Cosine Similarity (Lexical Baseline).
- **Leakage Prevention**: When querying for an evaluation example, its own `conversation_id` is passed to the `exclude_conversation_ids` parameter, strictly preventing self-retrieval.
- **Evaluation**: The baseline retrieval is evaluated using the 200 golden examples. A proxy relevance score is calculated based on whether the retrieved evidence yields the same baseline intent as the query. Note: This proxy is *not* a substitute for human relevance judgments.
- **Reproducibility Command**: Run `$env:PYTHONPATH="."; python scripts/evaluate_retrieval.py` to inspect the retrieval results and metrics in the `reports/` directory.

## Phase 4 — Support Agent Pipeline
The first end-to-end support agent pipeline is implemented in `src/agent/`.
- **Architecture**: Orchestrates `BaselineIntentClassifier`, `LexicalRetriever`, `EscalationPolicy`, and `ResponseGenerator`.
- **Response Strategy**: Deterministic framing of historically retrieved resolutions to ensure grounded, safe answers.
- **Escalation Policy**: Explicit rules route interactions to `HUMAN_ESCALATION` if evidence similarity is low (<0.15), the intent is ambiguous/unactionable, or if the intent involves sensitive account/billing matters.
- **Evaluation**: The agent auto-handles ~51.0% of cases and safely escalates ~49.0% on the golden evaluation set.
- **Commands**:
  - **Demo**: Run `$env:PYTHONPATH="."; python scripts/run_agent.py --message "My iPhone battery is draining very quickly"`
  - **Evaluate**: Run `$env:PYTHONPATH="."; python scripts/evaluate_agent.py`
- **Limitations**: The agent currently uses a deterministic response template rather than an LLM, making responses structurally rigid. Similarity scores are proxies for semantic relevance, and do not represent probabilistic confidence. No genuine LLM or human response evaluations exist yet.

**Selected Support Account**: `AppleSupport`

## Dataset
- **Name:** Customer Support on Twitter
- **Source/Identifier:** `thoughtvector/customer-support-on-twitter` (available on Kaggle)
- **Expected Placement:** The dataset should be placed in `data/raw/`. For example, `data/raw/twcs.csv`.
- **Git Exclusion:** The raw dataset is excluded from version control via `.gitignore` to prevent committing massive multi-million-row CSV files and to keep the source data immutable.

## Setup
Supported Python version: Python 3.10+ recommended.

To install dependencies, run:
```bash
python -m pip install -r requirements.txt
```

## Run Task 1
To inspect the dataset and generate a quality report, run the inspection script:
```bash
python scripts/inspect_dataset.py --data-path data/raw/twcs.csv
```
*(If you are testing with a smaller sample file, update the path accordingly, e.g., `--data-path tests/fixtures/sample.csv`)*

## Validation
The ingestion layer implements explicit schema validation. It currently checks for:
- The existence of required columns (`tweet_id`, `author_id`, `inbound`, `created_at`, `text`, `response_tweet_id`, `in_response_to_tweet_id`).
- Unique `tweet_id`s (measures duplicate tweet IDs).
- Valid boolean-like values for the `inbound` field.
- The availability of text (counts missing texts).
- Missing `author_id`s.
- The presence of response references (`in_response_to_tweet_id` and `response_tweet_id`).

## Development Sampling
The dataset contains millions of rows. To load a limited number of rows during development for faster engineering smoke tests, you can use the `--limit` argument:
```bash
python scripts/inspect_dataset.py --data-path data/raw/twcs.csv --limit 100000
```
**Important:** The simple first-N-row limit is acceptable for engineering smoke tests, but it is NOT the final evaluation sampling methodology, as it is not guaranteed to be statistically representative of conversations or brands.

## Current Findings
Findings produced by running the inspection script on a 2-row synthetic sample dataset (`tests/fixtures/sample.csv`):

- **Dataset Overview**: 2 rows, 7 columns, 0.00 MB memory usage.
- **Direction**: 1 inbound, 1 outbound.
- **Quality**: 0 missing text, 0 duplicate tweet IDs, 0 missing author IDs, 0 invalid inbound values.
- **Conversation References**: 1 row with `in_response_to_tweet_id`, 1 row with `response_tweet_id`.
- **Authors**: 2 unique author IDs.

*(Note: Run the inspection script on the full dataset to view the actual Kaggle dataset statistics)*

## Run Phase 2: Brand Profiling
To generate profiling metrics and candidate comparisons for all support accounts in the dataset:
```bash
python scripts/profile_brands.py --data-path data/raw/twcs.csv --output-dir reports
```

## Run Phase 3: Conversation Reconstruction
To extract all chronological conversations for the selected brand into a JSONL corpus:
```bash
python scripts/reconstruct_conversations.py --brand AppleSupport
```
*(The generated corpus `data/processed/applesupport_conversations.jsonl` is excluded from Git due to its size.)*

## Limitations / Next Phase
The project does not yet:
- define intents;
- train models;
- generate replies;
- implement escalation;
- evaluate the final agent.

The next phase will involve intent discovery based on the reconstructed conversations.
