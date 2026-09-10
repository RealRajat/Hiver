# Golden Set Annotation

## Overview
This document outlines the state of the `golden_set.csv` evaluation dataset.

## Current Status
**HUMAN ANNOTATION: PENDING — 0/200 completed.**

- **Total examples**: 200
- **Number human-labelled**: 0
- **Number ambiguous**: 0 (Pending)

## Sampling Methodology
The 200 examples were drawn via simple random sampling (`seed=42`) from the reconstructed AppleSupport conversation corpus.

## Annotation Guidelines
Reviewers strictly utilize the 6-intent taxonomy defined in `docs/golden_set_annotation_guidelines.md`. Ambiguous examples are explicitly flagged rather than discarded or forcibly shoehorned into an inaccurate category.

## Annotation Workflow
1. Run `python scripts/review_golden_set.py` to enter the interactive CLI.
2. Provide a taxonomy intent (1-6) and ambiguity status (y/n) for each pending row.
3. Once 200 rows are annotated, run `python scripts/compile_golden_set.py` to compile the final `golden_set.csv`.

## Provenance
The current dataset retains AI-generated draft labels (`data/evaluation/golden_annotation_ai_draft.csv`). The final compiled file will have `annotation_source = human` to explicitly guarantee human ground-truth.

## Limitations
Single-annotator labeling; inter-annotator agreement was not measured. The current baseline evaluations operate on the AI draft, serving as an engineering placeholder until genuine annotations are completed.
