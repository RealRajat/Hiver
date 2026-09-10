# Hiver SDE Intern Assignment

## Project Overview
This repository implements the Hiver SDE Intern take-home assignment. It will eventually build and evaluate an AI customer-support agent using the **Customer Support on Twitter** dataset.

## Current Status
`Phase 2 — Brand Selected`

The initial data ingestion and schema validation layer is implemented, and the brands within the TWCS dataset have been profiled. We have finalized the brand selection for the subsequent AI agent workflow.

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

## Limitations / Next Phase
The project does not yet:
- select the final brand;
- reconstruct complete conversations;
- define intents;
- train models;
- generate replies;
- implement escalation;
- evaluate the final agent.

The next phase is **Phase 2, Step 3: Final Brand Selection**.
