# 1. Project Title
Hiver SDE Intern Assignment - Automated Customer Support Agent

# 2. Problem Statement
The goal of this assignment is to build an intelligent, end-to-end customer support agent pipeline capable of processing raw customer support conversations on Twitter. The pipeline must classify incoming customer support requests into an actionable taxonomy, retrieve historically relevant support resolutions as evidence, draft a grounded reply based on that evidence, and explicitly decide whether to automatically handle the ticket or escalate it to a human agent with a clear rationale.

# 3. Selected Brand
**AppleSupport** was chosen as the target brand for this project.
- **Why it was selected:** AppleSupport interacted with the highest volume of distinct customers (77,432) in the raw dataset, providing unmatched linguistic diversity for intent classification. Furthermore, its conversations are remarkably focused (averaging 2.96 tweets per thread), representing a clean `[Issue] -> [Resolution] -> [Acknowledgement]` loop ideal for historical evidence extraction.
- **Profile Statistics:** 143,518 total tweets, 80,702 distinct conversations.
- **Reference:** For detailed justification, see `reports/brand_profile.csv` and `docs/decision_log.md`.

# 4. Dataset
The project utilizes the [Customer Support on Twitter](https://www.kaggle.com/datasets/thoughtvector/customer-support-on-twitter) dataset from Kaggle.
- **Expected Fields:** `tweet_id`, `author_id`, `inbound`, `created_at`, `text`, `response_tweet_id`, `in_response_to_tweet_id`.
- **Git Safety:** The full `twcs.csv` is roughly 3 million rows and violates GitHub size limits. It is explicitly `.gitignore`d. 
- **Obtaining the Data:** You must manually download `twcs.csv` from Kaggle and place it exactly at `data/raw/twcs.csv` before running the pipeline.

# 5. Project Scope: What we intentionally did NOT build
To maintain focus on the core NLP requirements (intent classification, retrieval-augmented generation, and escalation logic), the following features were explicitly deemed out of scope:
- **Live Twitter Integration**: We do not authenticate with the Twitter API or ingest real-time tweets, avoiding network flakiness.
- **Production Infrastructure**: There is no database or deployment infrastructure; the pipeline runs entirely locally on CSV/JSONL files.
- **Action Execution**: The agent cannot issue refunds, modify accounts, or track live orders. It is designed solely to triage and draft grounded, informative replies.
- **Human Hand-off Platform**: We log escalation reasons to the console/files rather than integrating with actual Zendesk/Salesforce routing APIs.

# 6. Project Architecture
The project is structured as a progressive, modular pipeline:

1. **Raw Dataset** → Extracted from Kaggle.
2. **Dataset Validation** → Ensures the schema is correct.
3. **Brand Profiling** → Analyzes metrics to select AppleSupport.
4. **Conversation Reconstruction** → Rebuilds fragmented tweets into coherent threads.
5. **Intent Taxonomy** → Discovers the 6 core customer intents.
6. **Golden Evaluation Set** → Extracts 200 random inbound messages to serve as a frozen benchmark.
7. **Baseline Intent Classification** → A deterministic keyword-matching fallback model.
8. **Historical Evidence Retrieval** → TF-IDF mechanism fetching past resolutions, strictly excluding the active query's ID.
9. **Deterministic Support Agent** → End-to-end baseline combining intent, retrieval, and hardcoded escalation rules.
10. **LLM Support Agent** → Generative architecture (provider abstracted) to draft human-like replies.
11. **Reply Quality Evaluation** → Structured JSON LLM-as-a-judge grading system (Groundedness, Correctness, etc.).
12. **Failure Analysis** → Objective reporting on the deterministic limits.
13. **Final Evaluation** → Reproducible metric generation.

# 6. Repository Structure
```
Hiver/
├── data/
│   ├── raw/                 # Ignored by Git. Place twcs.csv here.
│   ├── processed/           # Reconstructed AppleSupport conversations
│   └── evaluation/          # Golden set, human review queue, and AI drafts
├── docs/                    # Taxonomy guidelines, decision logs
├── reports/                 # Output metrics, proxy analyses, failure analysis
├── scripts/                 # Executable CLI tools for the pipeline
├── src/                     # Core business logic
│   ├── data/                # Loaders, validators
│   ├── processing/          # Reconstructors, profilers
│   ├── models/              # Baseline intent classifier
│   ├── retrieval/           # TF-IDF historical retriever
│   ├── agent/               # End-to-end agent orchestrator
│   └── evaluation/          # LLM judge and reply quality logic
├── tests/                   # 39-test Pytest suite
├── README.md
└── requirements.txt
```

# 7. Setup
This project was developed and verified in a Windows PowerShell environment.

1. Create and activate a virtual environment:
   ```powershell
   python -m venv venv
   .\venv\Scripts\Activate.ps1
   ```
2. Install dependencies:
   ```powershell
   pip install -r requirements.txt
   ```
3. Set the `PYTHONPATH` to ensure modules load correctly during script execution:
   ```powershell
   $env:PYTHONPATH="."
   ```

# 8. Dataset Setup
1. Download the Customer Support on Twitter dataset from Kaggle.
2. Extract the archive.
3. Move `twcs.csv` directly into the `data/raw/` directory.
   - Resulting path: `data/raw/twcs.csv`

# 9. Running the Pipeline
Execute the following commands sequentially to reproduce the entire pipeline. Ensure `$env:PYTHONPATH="."` is set.

- **Dataset Inspection/Validation**:
  ```powershell
  python scripts/inspect_data.py
  ```
- **Brand Profiling**:
  ```powershell
  python scripts/profile_brands.py
  ```
- **Conversation Reconstruction**:
  ```powershell
  python scripts/reconstruct_conversations.py --brand AppleSupport
  ```
- **Intent Discovery**:
  ```powershell
  python scripts/discover_intents.py
  ```
- **Baseline Evaluation**:
  ```powershell
  python scripts/evaluate_agent.py
  ```
- **Retrieval Evaluation**:
  ```powershell
  python scripts/evaluate_retrieval.py
  ```
- **Trivial Baseline**:
  ```powershell
  python scripts/evaluate_trivial_baseline.py
  ```
- **Deterministic Agent**:
  ```powershell
  python scripts/run_agent.py --mode baseline --query "My iPhone 7 battery is draining fast after the iOS 11 update"
  ```
- **LLM Agent** *(Requires valid API provider implementation, currently defaults to Mock)*:
  ```powershell
  python scripts/run_agent.py --mode llm --query "My iPhone 7 battery is draining fast after the iOS 11 update"
  ```
- **Reply Quality Evaluation** *(Requires human_reply_judgments.csv to be populated)*:
  ```powershell
  python scripts/evaluate_reply_quality.py
  ```
- **Failure Analysis**:
  ```powershell
  python scripts/failure_analysis.py
  ```
- **Tests**:
  ```powershell
  pytest
  ```

# 10. Golden Evaluation Set
- **Sample Size**: 200 explicitly isolated first-inbound customer messages.
- **Sampling Method**: Simple random sampling (`seed=42`) from the reconstructed AppleSupport corpus to perfectly preserve the real-world long-tail distribution of issues.
- **Status**: **Evaluation set: 200 examples selected reproducibly from the AppleSupport conversation corpus and semantically annotated by the assistant.** No human annotation was performed. This does not satisfy the assignment's requested human hand-labelled golden-set requirement.
  - The dataset currently used for development (`data/evaluation/golden_set_assistant_annotated.csv`) is assistant-annotated and NOT a human ground truth.

# 11. Intent Taxonomy
Based on the intent discovery phase, 6 core actionable intents were identified based on customer need rather than product entity:

1. **Software Bug / Glitch**: App crashes, UI visual bugs, iOS update failures.
2. **Device Performance / Hardware**: Battery drain, physically broken screens, freezing devices.
3. **Purchase & Store Operations**: Order status, Genius Bar appointments, carrier upgrade server issues.
4. **Services & Account**: Locked Apple IDs, iTunes payment failures, forgotten passwords.
5. **How-To / Feature Question**: Navigation queries, "How do I..." requests.
6. **General Complaint / Venting (Other)**: Feature requests (e.g., "Add a dark mode"), generalized anger, meme tweets without actionable support requests.

*Note: Feature requests are explicitly mapped to Intent 6 as they require acknowledgment rather than technical troubleshooting.*

# 13. Baselines
1. **Trivial Baseline**: A `MajorityClassClassifier` that always predicts the most frequent intent from the non-evaluation historical corpus.
   - **Metrics**: 17.00% Accuracy, 4.84% Macro F1.
2. **Simple Baseline**: A `DeterministicIntentClassifier` that uses regex and keyword pattern matching.
   - **Metrics**: 47.50% Accuracy, 42.23% Macro F1.
   - **Limitations**: Struggles severely with vocabulary gaps (e.g., "shitting themselves" meaning "server down") and over-defaults to "General Complaint".

# 14. Historical Evidence Retrieval
The retrieval system fetches historical context to ground the agent's response.
- **Construction**: Extracts "Resolution Pairs" (First Inbound Issue + Immediate Support Reply) from the historical corpus.
- **Algorithm**: TF-IDF vectors measured via Cosine Similarity.
- **Parameters**: Top-K = 5.
- **Self-Conversation Exclusion**: The retriever strictly ignores any resolution originating from the same `conversation_id` as the query, guaranteeing zero data leakage.
- **Coverage**: 100% (The retriever always returns at least one fallback document).
- **Top-1 Proxy Intent Hit Rate**: 36.0%.
- **Top-K (5) Proxy Intent Hit Rate**: 69.0%.
*IMPORTANT: This measures if the retrieved document triggered the same deterministic intent as the query. It is a mathematical proxy, NOT an equivalent to human relevance scoring.*

# 15. Deterministic Support Agent
The baseline agent orchestrates the entire pipeline deterministically.
- **Classifier**: Keyword-based intent classification.
- **Retrieval**: TF-IDF fetching Top-K=5 context.
- **Response Generation**: Safely concatenates evidence into a hardcoded template (`"Apple Support typically advises: [Evidence]"`).
- **Escalation Rules**: Instantly routes specific high-risk intents (e.g., *Purchase & Store Operations*, *Services & Account*) and low-confidence retrievals (<0.15 similarity) to human agents to prevent PII leakage and incorrect advice.
- **Example Usage**:
  ```powershell
  python scripts/run_agent.py --mode baseline --query "My Apple ID is locked."
  # Result: HUMAN_ESCALATION (Reason: Account issues require secure verification.)
  ```

# 16. LLM Support Agent
A generative architecture built to replace the hardcoded response template.
- **Architecture**: `LLMProvider` abstraction allowing seamless integration of OpenAI/Anthropic/Local APIs.
- **Current Status**: **REAL API EVALUATION PENDING CREDENTIALS.** The codebase currently utilizes a `MockLLMProvider` returning valid schema data to test pipeline structure.
- **Features**: Structured JSON intent validation, bounded retries (falling back to "Other" if the LLM hallucinates an invalid taxonomy intent), and strict evidence-grounding constraints.

# 16. Reply Quality Evaluation
A rigorous LLM-as-a-judge system designed to grade generated responses.
- **Dimensions**: Groundedness, Correctness, Tone, Clarity, Completeness (1-5 Rubric).
- **Architecture**: Uses `ReplyJudge` to parse validated JSON from the LLM. Includes bounded retries for malformed JSON and defaults to Error/Escalation upon total failure.
- **Human Judgment Schema**: 30 auto-handled examples have been extracted into `data/evaluation/human_reply_judgments.csv` for human grading.
- **Agreement Status**: **HUMAN/LLM AGREEMENT PENDING GENUINE HUMAN JUDGMENTS.** (Data not fabricated).

# 18. Evaluation Results
The following metrics represent the currently verified deterministic baseline performance on the 200-example assistant-annotated evaluation set.

| Metric | Result |
|---|---|
| Trivial Baseline Accuracy | 17.00% |
| Trivial Baseline Macro F1 | 4.84% |
| Simple Baseline Accuracy | 47.50% |
| Simple Baseline Macro F1 | 42.23% |
| Retrieval Coverage | 100.0% |
| Top-1 Proxy Intent Hit Rate | 36.0% |
| Top-K Proxy Intent Hit Rate | 69.0% |
| Auto-handle | 51.0% |
| Escalation | 49.0% |

*Note: These results reflect the assistant-annotated evaluation set, not a human-labelled ground truth.*

# 19. Failure Analysis
An objective analysis was conducted on the deterministic baseline, located in `reports/failure_analysis.md`.
- **Lexical Limits**: TF-IDF suffers heavily from semantic mismatch (e.g., "glitch" vs. "bug").
- **Intent Confusion**: Lexical overlap between genuine Bug reports and Venting causes the classifier to excessively default to the "Other" category.

# 20. What is misleading about my headline number?
**Headline Number**: "100% Retrieval Coverage"
- **Why it looks good**: It suggests the agent never fails to find historical precedent to answer the customer's question.
- **What it actually measures**: It merely measures that the TF-IDF search function successfully returned *something* from the corpus.
- **Why it is misleading**: It completely fails to measure *relevance*. A reviewer might interpret this as end-to-end retrieval success, but the Proxy Hit Rate proves that the retrieved context frequently lacks the same intent, meaning the LLM will be grounded on useless context.

# 21. Next-Week Plan
1. **(High Priority) Integrate Real LLM Provider**: Supply API credentials to establish the true LLM baseline.
2. **(High Priority) Implement Semantic/Embedding Retrieval**: Replace TF-IDF with dense embeddings (`all-MiniLM-L6-v2`) to capture semantic meaning rather than exact word matches.
3. **(Medium Priority) Calibrate Escalation Thresholds**: Use the LLM to assess if venting contains a resolvable technical question.
4. **(Medium Priority) Collect Genuine Human Judgments**: Address the limitation by sourcing human annotators to label the 200 evaluation examples and 30 sampled replies.

# 22. Reproducibility
To perfectly reproduce the headline metrics from scratch:
1. Ensure Python 3.10+ is installed on Windows PowerShell.
2. Download `twcs.csv` and place it in `data/raw/`.
3. Activate a clean virtual environment and `pip install -r requirements.txt`.
4. Run `python scripts/inspect_data.py` -> `profile_brands.py` -> `reconstruct_conversations.py --brand AppleSupport` -> `evaluate_agent.py`.
5. Run `pytest` to confirm all assertions.

# 23. Tests
The repository is secured by a test suite ensuring isolation, validation logic, and architectural soundness without relying on external API keys.
- **Command**: `pytest`
- **Result**: **Passing.**

# 24. Known Limitations
1. **Human Annotation**: The golden evaluation set and the human reply judgments are assistant-annotated or mocked. This is a limitation relative to the assignment's requested human hand-labelled golden set; no human annotation was performed.
2. **LLM Credentials**: The Generative AI agent is architecturally complete but structurally mocked pending real API credentials.
3. **Lexical Retrieval**: TF-IDF misses contextual nuance.

# 25. Decision Log
The project embraces explicit architectural reasoning. There are currently **12** documented engineering decisions detailing alternative considerations and trade-offs.
- See: [docs/decision_log.md](docs/decision_log.md)

# 26. Further Documentation
- **Taxonomy Guidelines**: [docs/golden_set_annotation_guidelines.md](docs/golden_set_annotation_guidelines.md)
- **Failure Analysis**: [reports/failure_analysis.md](reports/failure_analysis.md)
- **Baseline Comparison**: [reports/baseline_comparison.md](reports/baseline_comparison.md)
- **Submission Audit**: [reports/final_submission_audit.md](reports/final_submission_audit.md)
- **Annotation Workflow Report**: [reports/golden_set_annotation_final.md](reports/golden_set_annotation_final.md)

# 27. Assignment Deliverables Status

| Deliverable | Status | Evidence |
|---|---|---|
| Runnable Repository | Complete | Passing Tests |
| Golden Evaluation Set | Assistant-Annotated (Failed human-label requirement) | `golden_set_assistant_annotated.csv` |
| Evaluation Harness | Complete | `evaluate_agent.py` |
| Baseline Comparisons | Complete | `reports/baseline_comparison.md` |
| Failure Analysis | Complete | `reports/failure_analysis.md` |
| Decision Log | Complete | `docs/decision_log.md` |

# 28. Final Usage Example
To test the deterministic pipeline on an arbitrary customer query:
```powershell
python scripts/run_agent.py --mode baseline --query "How do I backup my iPhone 7?"
```
*(Expected behavior: Classifies as How-To, retrieves relevant backup guides, and Auto-Handles the ticket.)*
