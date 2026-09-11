# Golden Set Annotation

## Overview
This document outlines the state of the `golden_set_assistant_annotated.csv` evaluation dataset.

## Current Status
**ASSISTANT-ANNOTATED (FAILED HUMAN-LABEL REQUIREMENT) — 200/200 completed.**

- **Total examples**: 200
- **Number assistant-labelled**: 200
- **Number ambiguous**: 32

## Sampling Methodology
The 200 examples were drawn via simple random sampling (`seed=42`) from the reconstructed AppleSupport conversation corpus.

## Annotation Guidelines
The assistant strictly utilized the 6-intent taxonomy defined in `docs/golden_set_annotation_guidelines.md`. Ambiguous examples were explicitly flagged rather than discarded or forcibly shoehorned into an inaccurate category.

## Annotation Workflow
Because human annotators were not utilized for this assignment, the assistant autonomously generated the labels. The interactive CLI `review_golden_set.py` is available in the repository but was bypassed. 

## Provenance
The evaluation set has the `annotation_source = assistant_annotated` field to explicitly guarantee its provenance. The dataset explicitly FAILS the assignment's human-ground truth requirement.

## Limitations
The evaluation set was fully semantically annotated by the assistant. No human review or inter-annotator agreement was measured. This is an explicit failure of the Hiver SDE Intern Take-Home assignment requirement.
