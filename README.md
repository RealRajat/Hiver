# Hiver SDE Intern Assignment

## 1. Problem Framing
This repository implements the foundation for an AI customer-support agent. The objective is to intelligently classify incoming customer queries, retrieve historically grounded resolutions to avoid hallucinations, draft accurate responses, and deterministically escalate sensitive or low-confidence interactions to a human support layer.

## 2. Dataset
The project uses the "Customer Support on Twitter" dataset.
**Source/Citation:** [Kaggle — Customer Support on Twitter](https://www.kaggle.com/thoughtvector/customer-support-on-twitter)

## 3. Brand Selection
**Selected Support Account**: `AppleSupport`
Chosen due to its massive unique customer footprint (77k+ distinct customers) and ideal conversational structure (averaging ~3 tweets per thread), optimizing signal-to-noise ratio for agent intent classification.

## 4. Conversation Reconstruction
Chronological resolution threads were constructed from isolated tweets. The corpus is stored at `data/processed/applesupport_conversations.jsonl` (excluded from git).

## 5. Intent Taxonomy
A highly actionable, 6-intent taxonomy was formulated:
1. Software Bug / Glitch
2. Device Performance / Hardware
3. Purchase & Store Operations
4. Services & Account
5. How-To / Feature Question
6. General Complaint / Venting (Other)

## 6. Golden Evaluation Set
A fixed benchmark of 200 examples (`data/evaluation/golden_set_annotated.csv`) was generated to evaluate the pipeline. *Provenance: Initial annotations were AI-drafted and subsequently programmatically corrected; it is not fully human-labelled.*

## 7. Baseline
A minimal deterministic intent classifier achieves 47.50% accuracy on the golden set. It struggles with vocabulary gap and over-defaults to "General Complaint".

## 8. Historical Retrieval
A TF-IDF lexical retriever extracts historical resolution pairs to ground the generated response. It enforces strict query-time exclusion of the target query's `conversation_id` to prevent data leakage.

## 9. Support-Agent Architecture
Orchestrates Intent Classification, Retrieval, Escalation, and Generation. Hardcoded escalation rules protect sensitive topics (Billing/Accounts) and low-evidence queries (<0.15 TF-IDF similarity).

## 10. LLM Architecture
Abstracted via `LLMProvider` and `MockLLMProvider` to cleanly decouple logic from external APIs. It implements bounded retries to enforce structured JSON validation against hallucinated intents or scores.

## 11. Reply-Quality Evaluation
An `LLM-as-judge` module utilizes a strict 1-5 rubric assessing Helpfulness, Correctness, Relevance, Groundedness, Tone, and Overall Score for generated replies.

## 12. Results

| Component | Metric | Result |
|---|---|---:|
| Intent Baseline | Accuracy | 47.50% |
| Intent Baseline | Macro F1 | 42.23% |
| Retrieval | Coverage | 100% |
| Retrieval | Same-intent proxy hit rate | 69% |
| Agent | Auto-handle rate | 51% |
| Agent | Escalation rate | 49% |
| LLM | Real evaluation | Pending |
| Human/LLM Agreement | Genuine judgments | Pending |

## 13. Failure Analysis
The deterministic baseline suffers heavily from lexical mismatch (e.g., retrieving a factory reset document for a software keyboard bug) because TF-IDF relies on exact word overlap rather than semantic meaning. The classifier misidentifies 31 explicit technical bugs as "General Venting".

## 14. Misleading Headline Number
**"100% Retrieval Coverage"**
This headline sounds impressive, suggesting perfect knowledge recall. However, it only measures that the retriever successfully returned at least one document from the corpus without crashing. The *same-intent proxy hit rate* (69%) mathematically proves that 31% of the time, the top retrieved document didn't even match the intent of the query. 100% coverage does not equal 100% relevance.

## 15. Limitations
- **REAL LLM EVALUATION: PENDING PROVIDER CREDENTIALS.** No fabricated mock metrics are claimed as real LLM performance.
- **HUMAN/LLM AGREEMENT: PENDING GENUINE HUMAN JUDGMENTS.** The human annotation schema exists but contains no fabricated scores.
- Retrieval proxy hit rate is merely a proxy for relevance; it does not explicitly guarantee the retrieved text actually solves the specific issue.

## 16. Next-Week Plan
1. Integrate actual LLM credentials to unlock the true generative baseline.
2. Implement semantic/dense embedding retrieval to fix the 31% TF-IDF proxy miss rate.
3. Calibrate escalation thresholds rather than indiscriminately escalating entire intents.

## 17. Reproduction Instructions
Ensure `data/raw/twcs.csv` is present. Run the following commands from the project root:
- Evaluate Baseline: `python scripts/evaluate_agent.py --mode baseline`
- Failure Analysis: `python scripts/failure_analysis.py`
- Mock LLM Judge Evaluation: `python scripts/evaluate_reply_quality.py --mode mock`
- Agent Pipeline Demo: `python scripts/run_agent.py --message "My iPhone battery is draining very quickly" --mode baseline`

*(Note: Depending on your environment, you may need to prefix commands with `$env:PYTHONPATH="."` (Windows PowerShell) or `PYTHONPATH="."` (Unix/Linux).)*

## 18. Project Structure
- `data/`: Raw and processed dataset files, including the golden set.
- `docs/`: Decision logs and annotation guidelines.
- `reports/`: Markdown and JSON reports for evaluation metrics.
- `scripts/`: Executable entry points for the pipeline.
- `src/`: Core logic (Agent, Data, Evaluation, Retrieval).
- `tests/`: `pytest` test suite.
