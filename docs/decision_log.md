# Decision Log

## Decision: Final Brand Selection

### Decision
Selected **AppleSupport**.

### Alternatives Considered
- AmazonHelp
- Uber_Support
- SpotifyCares
- Delta

### Reasoning
The objective is to select a brand that provides the strongest foundation for an AI support-agent workflow (intent classification, grounded reply generation, and escalation routing). 
We evaluated candidates using a framework prioritizing customer diversity and clean interaction structure over raw dataset volume:
- **Customer Coverage (Primary)**: AppleSupport interacts with the highest number of unique customers (77,432) in the entire dataset, surpassing even the highest-volume brand (AmazonHelp's 71,668). This high customer diversity is critical for training a robust intent classifier that generalizes well to varied linguistic phrasing.
- **Conversation Structure (Secondary)**: AppleSupport averages 2.96 tweets per conversation, aligning closely with a clean [Customer Issue] -> [Brand Reply] -> [Customer Acknowledgment/Clarification] flow. This is optimal for learning auto-handling logic. In contrast, AmazonHelp averages 4.53 tweets per thread, which often implies noisy, drawn-out manual troubleshooting (e.g., repeatedly asking for order IDs via DMs) that is harder to cleanly parse for RAG context.
- **Historical Volume**: With 106,860 outbound replies and 80,702 distinct conversations, AppleSupport comfortably provides enough data density to build strong embeddings and evaluation sets.

### Evidence
Based on `reports/brand_profile.csv`:
- AppleSupport: 143,518 total tweets, 77,432 unique customers, 80,702 conversations, avg length 2.96.
- AmazonHelp: 270,343 total tweets, 71,668 unique customers, 82,534 conversations, avg length 4.53.

### Trade-offs
We sacrificed the sheer raw volume of AmazonHelp (270k vs 143k total tweets). However, we traded this for a dataset with broader customer reach and tighter conversational loops, which provides a cleaner signal-to-noise ratio for NLP tasks. 

### Consequences
The remainder of the Hiver assignment (intent discovery, golden set creation, RAG, and evaluation) will be strictly scoped to AppleSupport. We assume that AppleSupport's interactions contain a diverse enough set of intents (e.g., hardware issues, software issues, account access) to build a meaningful taxonomy.

## Decision: Preliminary Intent Taxonomy

### Decision
Established a compact, 6-intent preliminary taxonomy:
1. Software Bug / Glitch
2. Device Performance / Hardware
3. Purchase & Store Operations
4. Services & Account
5. How-To / Feature Question
6. General Complaint / Venting (Other)

### Alternatives Considered
- Creating product-specific intents (e.g., "iPhone Bug", "MacBook Bug").
- Creating an excessively granular bug list (e.g., "Emoji Bug", "Battery Bug").
- Omitting a "General Complaint" category.

### Reasoning
The taxonomy is designed around the *customer's core need (verb)* rather than the *product (noun)*. Whether a customer is returning an iPhone or a Mac, the agent action (Purchase & Store) is identical. This keeps the taxonomy small and highly actionable for an AI agent. Furthermore, adding a "General Complaint / Venting" intent serves as a safe "Other" category to catch the massive volume of Twitter venting without forcing the agent to hallucinate technical solutions to non-technical anger.

### Evidence
Qualitative analysis of 50 randomly sampled AppleSupport first-customer messages (`reports/intent_sample.txt`) and dataset-wide bigram frequency extraction (`scripts/discover_intents.py`).

### Trade-offs
We sacrifice fine-grained product tracking at the intent level (e.g., we don't know *which* device has the bug just from the intent). This trade-off is accepted because product entities can be extracted separately via Named Entity Recognition (NER) or simple LLM extraction later, keeping the core routing intent clean.

### Consequences
This taxonomy will be used to construct the final golden evaluation set and govern the routing logic of the AI agent in Phase 4.

## Decision: Golden Evaluation Set Sampling

### Decision
Created a golden evaluation set of exactly 200 human-labelled examples (`data/evaluation/golden_set.csv`), using the *first customer message* of a reconstructed conversation as the unit of annotation.

### Alternatives Considered
- Annotating the entire conversation thread as a single unit.
- Selecting 200 examples via stratified sampling to perfectly balance the 6 intents.

### Reasoning
We chose the *first customer message* because the primary goal of the agent is initial routing and intent discovery. The agent must make its decision based on the customer's opening request, before asking follow-up questions. We chose simple random sampling (`seed=42`) over stratified sampling to preserve the natural historical distribution of intents. A classifier must be evaluated on its ability to handle the true distribution of issues it will face, rather than an artificial 16.6% flat split.

### Evidence
The random sampling method yielded a realistic long-tail distribution (e.g., Software Bug dominating due to the iOS 11 launch timing, with fewer How-To questions).

### Trade-offs
Because of random sampling, rare intents have fewer evaluation examples in the 200-item golden set. This trade-off is accepted because an agent misclassifying a rare intent is mathematically less harmful to overall system accuracy than misclassifying the dominant intents.

### Consequences
The evaluation harness (built in later phases) will benchmark against this fixed 200-item golden set.

## Decision: Golden Set Annotation Fallback

### Decision
Utilized an assistant-annotated evaluation set (`golden_set_assistant_annotated.csv`) instead of a genuinely human-labelled golden set.

### Reasoning
The golden set serves as the ground-truth benchmark for evaluating the AI agent's intent classifier. The assignment strictly required a hand-labelled set. Because human annotators were not utilized, we fell back to an assistant-annotated set to allow the evaluation pipeline to run. To maintain integrity, we explicitly mark the source as `assistant_annotated` and loudly document that the human hand-labelled requirement was NOT met.

### Evidence
The Hiver assignment specification mandates *hand-labelled* golden examples. This requirement was intentionally logged as a failure/limitation.

### Trade-offs
We trade strict compliance with the assignment constraints for the ability to actually execute the evaluation harness.

### Consequences
The evaluation set is functionally complete but academically limited. The pipeline dynamically loads this fallback set but prints a warning to ensure no one mistakes it for human ground-truth.

## Decision: Handling Feature Requests in the Taxonomy

### Decision
Messages that are primarily Feature Requests (e.g., asking Apple to add a new capability) will be classified under `General Complaint / Venting (Other)`, rather than creating a seventh intent category.

### Reasoning
The approved 6-intent taxonomy does not contain a dedicated "Feature Request" category. The goal of the taxonomy is to define the primary support action for an AI agent. From an agent's perspective, both generic complaints and feature requests require a similar response: acknowledging the feedback gracefully, as the agent cannot technically troubleshoot or solve either issue. Therefore, grouping them prevents taxonomy bloat without harming routing logic.

### Evidence
During the semantic review of the `golden_annotation_review_queue.csv`, examples such as GOLDEN_056 and GOLDEN_187 were identified as feature requests and mapped to the `Other` category.

### Consequences
The 6-intent taxonomy remains unchanged. Evaluators must recognize that the "Other" category functions as a catch-all for feedback, venting, and unresolvable non-technical requests.

## Decision: Normalizing Escaped Identifiers

### Decision
Normalized the `example_id` column in the golden annotation review queue to remove escaped underscores (e.g., changing `GOLDEN\_037` to `GOLDEN_037`) and enforced this strict formatting in the test suite.

### Reasoning
The initial AI-drafted queue generated escaped markdown-style underscores in the ID column. This formatting bug caused programmatic semantic correction scripts to silently fail because string lookups did not match. Normalizing the IDs ensures that downstream evaluation scripts and merging logic will function correctly.

### Consequences
`tests/test_evaluation.py` now explicitly asserts that IDs match `^GOLDEN_\d{3}$` and form a complete, unique sequence from 001 to 200 to prevent similar data-quality regressions.

## Decision: Phase 4 Evaluation Harness Architecture

### Decision
Implemented the evaluation harness using a deterministic baseline classifier first, keeping automated metrics separated from future LLM judging, reporting ambiguity separately, and avoiding any fabricated human/LLM agreement metrics.

### Reasoning
- **Deterministic Baseline**: Provides a minimal, easily understandable floor for performance (Accuracy ~47.5%) before introducing complex LLM models. It ensures the testing harness is solid.
- **Separating Metrics**: Automated intent metrics (accuracy/F1) use exact string matching against the taxonomy, whereas reply evaluation requires nuanced LLM-as-judge scoring. Separating them ensures modularity.
- **Explicit Ambiguity**: Instead of silently dropping ambiguous examples, we report them separately. This highlights how well the agent handles borderline or context-poor customer queries without corrupting the clear-cut baseline metrics.
- **No Fabricated Agreement**: The assignment asks for human/LLM agreement. To remain honest, we built the schema (`src/evaluation/reply_judge.py`) and metrics functions but will not claim agreement until an actual LLM runs and a human evaluates the outputs.

### Consequences
The harness is ready for production model integration. The baseline metrics reside in `reports/baseline_intent_results.md`.

## Decision: Phase 4 Historical Evidence Retrieval

### Decision
Implemented a deterministic TF-IDF (lexical) retriever to fetch "Resolution Pairs" (Customer Issue + Support Reply) while strictly excluding the query's own `conversation_id` to prevent data leakage during evaluation.

### Reasoning
- **Separation of Concerns**: Splitting retrieval from generation forces the agent to rely on grounded historical facts rather than raw parametric knowledge, reducing hallucinations.
- **Lexical Baseline**: Starting with TF-IDF provides a cheap, reproducible, and explainable baseline. It allows us to establish a benchmark for coverage and similarity before introducing expensive semantic embeddings.
- **Data Leakage Prevention**: If the golden set retrieves itself, the evaluation of the generated response becomes a trivial copy-paste test. Excluding the target `conversation_id` forces the system to generalize.
- **Proxy Metrics**: Because we lack human relevance annotations for retrieval, we rely on a transparent proxy metric (whether the retrieved text triggers the same intent as the query). We explicitly refrain from calling this "grounded retrieval accuracy" to maintain analytical honesty.

### Consequences
The retrieval module (`src/retrieval`) is ready to serve evidence context to the reply generator in the next phase. Proxy evaluations can be found in `reports/retrieval_results.md`.

## Decision: Phase 4 Support Agent Architecture & Escalation

### Decision
Implemented a modular support agent (`src/agent`) orchestrating deterministic classification, retrieval, explicitly structured escalation rules, and template-based grounded response generation.

### Reasoning
- **Modular Pipeline**: By separating Intent, Evidence, Escalation, and Response, we can upgrade individual components (e.g., replacing the response template with an LLM) without refactoring the orchestration logic.
- **Deterministic Response Before LLMs**: Using a strict template (`"Apple Support typically advises: [Evidence]"`) ensures safety and groundedness. It prevents hallucinations, fake URLs, and imaginary policies that early LLM integrations are prone to, proving that the underlying retrieved evidence is the true driver of the response.
- **Explicit Escalation**: Hardcoded rules ensure sensitive intents (billing/accounts) and low-evidence queries (<0.15 similarity) are explicitly routed to humans with logged reasons. This is much safer than prompting an LLM to "decide if you can answer this," which can be dangerously overconfident.
- **Similarity != Confidence**: Cosine similarity (TF-IDF) is strictly used as an evidence matching score. It is documented as such, avoiding the deceptive practice of presenting raw similarity as a probabilistic "Confidence: 80%" metric.

### Consequences
The agent pipeline is fully operational. It achieves a 51% auto-handle rate and 49% escalation rate on the golden set. Future phases will introduce an LLM to replace the deterministic Response Generator and evaluate its conversational fluency against human judges.

## Decision: Phase 5 LLM-Powered Agent Integration

### Decision
Introduced an LLM abstraction layer (`LLMProvider`) to implement `LLMIntentClassifier` and `LLMResponseGenerator`. We implemented a `--mode` toggle to ensure the deterministic baseline remains fully intact and reproducible alongside the new LLM implementation.

### Reasoning
- **Structured LLM Validation**: LLMs can hallucinate non-existent intents. The `LLMIntentClassifier` implements a strict parsing and bounded-retry loop to ensure intents match `GoldenSetLoader.VALID_INTENTS`. If the LLM repeatedly fails, it gracefully falls back to `General Complaint / Venting (Other)` rather than crashing.
- **Evidence-Grounded Prompting**: The `LLMResponseGenerator` is strictly prompted to use ONLY the retrieved historical evidence. This bridges the gap between conversational fluency and the strict safety established in Phase 4.
- **Mocking and Integrity**: We implemented a `MockLLMProvider` for tests to avoid committing API keys or making tests flaky/slow. The evaluation script defaults to this mock if a real API key is absent, strictly honoring the requirement to NOT fabricate LLM/human agreement scores.

### Consequences
The architecture seamlessly supports swapping in production LLM models while maintaining strict historical grounding and escalation safety. The baseline remains available for regression testing.

## Decision: Phase 6 Reply Quality & Human/LLM Agreement

### Decision
Implemented a 1-5 scale evaluation rubric across 5 dimensions and an overall score. Created a structured JSON `ReplyJudge` and initialized the schema for human judgments (`data/evaluation/human_reply_judgments.csv`), using a reproducible sample size of 30 auto-handled examples.

### Reasoning
- **Groundedness vs. Correctness**: Groundedness strictly measures adherence to retrieved evidence (penalizing hallucinations), while Correctness measures factual problem resolution. Distinguishing these helps diagnose if an LLM is accurately summarizing but hallucinating details.
- **Separating Generator from Judge**: The LLM drafting the reply is completely separated from the evaluation logic. 
- **Escalation Exclusion**: Human escalations do not generate draft replies. Forcing an evaluation on escalated cases skews results, so we strictly evaluate only `AUTO_HANDLE` items.
- **No Fabrication**: Because no genuine human annotations exist for these specific drafts, the output strictly logs "HUMAN/LLM AGREEMENT: PENDING GENUINE HUMAN JUDGMENTS". We use a `MockLLMProvider` returning static JSON to test parsing logic without hallucinating evaluation data.

### Consequences
The repository is fully structured for human annotators to grade the 30 sampled baseline outputs. Once populated, running `evaluate_reply_quality.py` will automatically calculate rigorous exact and within-one-point agreement statistics between the human annotators and the LLM judge.

## Decision: Phase 7 Failure Analysis Methodology

### Decision
Conducted failure analysis exclusively on the Phase 4 deterministic baseline, maintaining a strict distinction between observed facts (metrics from `failure_analysis.py`) and inferences. Explicitly chose "100% Retrieval Coverage" as the assignment's requested "misleading headline number."

### Reasoning
- **No Fabrication**: Because API credentials are not available, performing a failure analysis on hallucinated or mocked LLM replies would invalidate the integrity of the project.
- **Misleading Metric**: "100% Retrieval Coverage" is incredibly misleading because coverage simply means "returning *something*", regardless of relevance. Reviewers could assume 100% means the agent always finds the right answer, when the Proxy Hit Rate proves it fails 31% of the time.
- **Prioritization**: The next-week plan prioritizes Semantic Embedding Retrieval over prompt-engineering because the failure analysis objectively proved that the upstream retrieval context is failing lexically 31% of the time. You cannot prompt-engineer an LLM out of being fed irrelevant context.

### Consequences
The project is perfectly staged for a real API key. The limitations of deterministic keywords and lexical TF-IDF are mathematically proven and documented, completely justifying the architectural transition to dense embeddings and LLMs in the upcoming weeks.

## Decision: Golden Set Source Integrity

### Decision
The data loader explicitly warns that the dataset is assistant-annotated and explicitly permits `assistant_annotated` in the schema validator, rather than silently pretending it is human-labelled.

### Context
The Hiver assignment explicitly requires hand-labelled evaluation examples.

### Rationale
Automatically generated labels cannot legitimately satisfy the human-labeling requirement. Passing off assistant annotations as human ground truth invalidates the integrity of the evaluation pipeline and amounts to data fabrication. 

### Trade-off
The project explicitly accepts a "Not fully compliant" status regarding the human annotation requirement in order to preserve evaluation honesty.

