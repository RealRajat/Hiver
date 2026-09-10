# Failure Analysis

## 1. Evaluation Context
The following failure analysis is based on the **Deterministic Baseline Pipeline** running on the 200-example golden evaluation set. 
> [!WARNING]
> **Real LLM Evaluation is PENDING PROVIDER CREDENTIALS.** No real LLM evaluation or generated responses exist. The analysis of intent, retrieval, and escalation relies entirely on the deterministic baseline, as explicitly requested, to prevent data fabrication.

## 2. Intent Failures
The deterministic zero-shot classifier achieved **47.50% accuracy** (Macro F1: 42.23%). The most common failure patterns are over-classifying specific issues into the generic fallback category.

### Most Confused Intent Pairs
1. **True:** `Software Bug / Glitch` | **Pred:** `General Complaint / Venting (Other)` (31 occurrences)
2. **True:** `Device Performance / Hardware` | **Pred:** `General Complaint / Venting (Other)` (15 occurrences)
3. **True:** `General Complaint / Venting (Other)` | **Pred:** `Software Bug / Glitch` (12 occurrences)

### Analysis
- **Observed Fact**: The classifier heavily over-indexes on `General Complaint / Venting` when faced with vocabulary it does not explicitly recognize.
- **Inference**: The deterministic baseline lacks the semantic understanding to map specific technical complaints (e.g., "my keyboard autocorrect is broken") to "Software Bug" without explicit keyword matches, thus defaulting to generic venting.

## 3. Retrieval Failures
The lexical TF-IDF retriever achieved **100% coverage** but only a **69.0% Proxy Same-Intent Hit Rate**.

### Analysis
- **Observed Fact**: 31% of the time, the top retrieved historical conversation does not even share the same intent as the customer's query.
- **Inference**: TF-IDF relies purely on exact lexical overlap. A customer asking "how to wipe my phone" and a historical resolution for "factory resetting a device" share very few words, causing the retriever to fail to find the semantically correct evidence.

## 4. Response Failures
> [!IMPORTANT]
> **RESPONSE FAILURE ANALYSIS PENDING.** 
> Because real LLM API credentials are not available, we have not genuinely generated draft replies. Consequently, we cannot systematically analyze hallucinations, unsupported claims, or excessive verbosity yet.

## 5. Escalation Failures
The pipeline currently enforces a strict deterministic escalation policy, resulting in a **49.0% Escalation Rate**.

### Breakdown by Predicted Intent
- **General Complaint / Venting (Other)**: 76 cases escalated.
- **Purchase & Store Operations**: 11 cases escalated.
- **Services & Account**: 11 cases escalated.

### Analysis
- **Observed Fact**: All 98 escalations were triggered perfectly in accordance with the hardcoded policy (which escalates these three intents unconditionally to protect sensitive accounts and avoid aggravating angry customers).
- **Inference**: While safe, escalating 100% of "General Complaint" interactions prevents the agent from handling easily resolvable issues simply because the customer sounded frustrated.

## 6. Misleading Headline Number
**"100% Retrieval Coverage"**

1. **Why the number looks good**: It suggests the agent has perfect knowledge and always successfully finds historical precedent to answer the customer's question.
2. **What it actually measures**: It merely measures that the TF-IDF search function did not crash and successfully returned the top-scoring document from the corpus, regardless of how low the similarity score was.
3. **What it fails to measure**: It completely fails to measure *relevance*.
4. **Why it is misleading**: A reviewer might interpret this as end-to-end retrieval success, but the Proxy Hit Rate (69%) proves that nearly a third of these "successfully retrieved" documents are completely irrelevant to the customer's actual intent. Grounding an LLM on irrelevant evidence guarantees hallucinations or useless replies.

## 7. Key Lessons
1. **Lexical matching is insufficient**: TF-IDF cannot bridge the vocabulary gap between customer phrasing and support phrasing.
2. **Deterministic intent fails gracefully but inaccurately**: Keyword-based classification defaults to "Venting" too often, severely limiting auto-handle opportunities.
3. **Escalation policy is too blunt**: Blanket-escalating entire intents is safe but scales poorly.

## 8. Next-Week Plan
1. **(High Priority) Integrate Real LLM Provider**: Supply API credentials to unblock the `LLMIntentClassifier` and `LLMResponseGenerator` to establish the true LLM baseline.
2. **(High Priority) Implement Semantic/Embedding Retrieval**: Replace the TF-IDF retriever with a dense embedding model (e.g., `all-MiniLM-L6-v2`) to capture semantic meaning rather than exact word matches, directly addressing the 31% proxy miss rate.
3. **(Medium Priority) Calibrate Escalation Thresholds**: Instead of blanket-escalating "General Complaints", use the LLM to assess if the venting contains a resolvable technical question, allowing us to safely auto-handle more cases.
4. **(Medium Priority) Collect Genuine Human Judgments**: Source human annotators to grade the 30 sampled examples using the schema defined in Phase 6, unlocking our LLM-as-Judge agreement metrics.
5. **(Low Priority) Adversarial Edge-Case Testing**: Once the real LLM is wired, inject adversarial customer messages to test the bounds of the "Groundedness" prompt instructions.
