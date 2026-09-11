# Failure Analysis

## 1. Evaluation Context
The following failure analysis is based on the **Deterministic Baseline Pipeline** running on the 200-example golden evaluation set. 

> [!WARNING]
> **Real LLM Evaluation is PENDING PROVIDER CREDENTIALS.** No real LLM evaluation or generated responses exist. The analysis relies entirely on the deterministic baseline, as explicitly requested, to prevent data fabrication.

## 2. Top 5 Failure Modes

### Failure Mode 1: Vocabulary Gap & Emotional Intent Confusion
- **Real Example**: `GOLDEN_003` - "Bruhhhh I’m so fuckin tired @AppleSupport @115858 fixed these damn glitches ! Keep cutting my phone off"
- **Expected Behavior**: Classify as `Device Performance / Hardware` or `Software Bug`.
- **Actual Behavior**: Classified as `General Complaint / Venting (Other)`.
- **Why the System Failed**: The keyword classifier heavily penalizes emotional language and lacks the semantic depth to map "cutting my phone off" to a device performance issue, defaulting to generic venting.
- **Hypothesis for Improvement**: An LLM classifier can look past the expletives and identify the underlying technical issue ("cutting off" = power/performance failure).

### Failure Mode 2: Lexical Retrieval Mismatch (The Proxy Hit Rate Gap)
- **Real Example**: `GOLDEN_007` - "@AppleSupport trying to setup HomeKit automation for when multiple people leave home but it says to upgrade my hub -an Apple TV w tvOS 11.1"
- **Expected Behavior**: Retrieve a historical "How-To" resolution regarding HomeKit hub requirements.
- **Actual Behavior**: Retrieved an irrelevant bug report regarding tvOS beta versions (Proxy intent: `Software Bug / Glitch`).
- **Why the System Failed**: TF-IDF (lexical matching) overly indexed on "tvOS 11.1" and "upgrade", pulling documents with those exact tokens regardless of the semantic intent (HomeKit setup).
- **Hypothesis for Improvement**: Transitioning to dense semantic embeddings (`all-MiniLM-L6-v2`) will allow the retriever to match the *meaning* of the query rather than raw token overlap.

### Failure Mode 3: Overly Blunt Escalation Policy
- **Real Example**: `GOLDEN_004` - "What is this “A” and  QUESTION MARK THAT MY PHONE KEEPS DOING!! @115858 @AppleSupport"
- **Expected Behavior**: Auto-handle with the known iOS 11.1 autocorrect bug workaround.
- **Actual Behavior**: Escalated to a human agent unconditionally.
- **Why the System Failed**: Because the query was misclassified as `General Complaint / Venting` (due to all-caps and lack of the word "bug"), it triggered a hardcoded safety rule that escalates all venting to human agents.
- **Hypothesis for Improvement**: Calibrate the escalation logic to use LLM assessment rather than hardcoded intent-blocks. If an LLM detects a resolvable question within the venting, it should draft a reply.

### Failure Mode 4: Context-Dependent Keyword Ambiguity
- **Real Example**: `GOLDEN_002` - "@AppleSupport you seem to be skipping the step that allows to select which carrier phone to get for iPhone X upgrade head start. Why?"
- **Expected Behavior**: Classify as `Purchase & Store Operations`.
- **Actual Behavior**: Classified as `General Complaint / Venting (Other)`.
- **Why the System Failed**: The word "upgrade" is highly ambiguous. It frequently refers to "iOS software upgrade" (Bug/Glitch) but here refers to the "iPhone Upgrade Program" (Purchase). The keyword system cannot contextualize the noun phrase.
- **Hypothesis for Improvement**: Generative LLMs inherently process attention across the entire sentence, easily disambiguating "carrier phone to get" as a purchase operation.

### Failure Mode 5: Blind Evidence Concatenation (Template Brittleness)
- **Real Example**: When retrieval similarity is marginally above the escalation threshold (e.g., 0.20) but the proxy intent is wrong.
- **Expected Behavior**: The agent recognizes the retrieved evidence does not actually answer the question and escalates.
- **Actual Behavior**: The deterministic response generator blindly pastes the irrelevant resolution into the hardcoded template (`"Apple Support typically advises: [Irrelevant Evidence]"`).
- **Why the System Failed**: The deterministic agent lacks a "reading comprehension" step. It assumes retrieval success implies relevance.
- **Hypothesis for Improvement**: The `LLMResponseGenerator` prompts the model to read the evidence first. If the evidence cannot answer the question, the LLM is instructed to output an escalation request rather than hallucinate a connection.

## 3. Misleading Headline Number
**"100% Retrieval Coverage"**

- **Why it looks good**: It suggests the agent never fails to find historical precedent to answer the customer's question.
- **What it actually measures**: It merely measures that the TF-IDF search function did not crash and successfully returned the top-scoring document from the corpus, regardless of similarity.
- **Why it is misleading**: A reviewer might interpret this as end-to-end retrieval success. However, the Proxy Hit Rate proves that the retrieved context fails to even match the customer's intent 64% of the time (Top-1 Proxy = 36%). Grounding an LLM on irrelevant evidence guarantees hallucinations. 

## 4. Next-Week Plan
1. **(High Priority) Integrate Real LLM Provider**: Supply API credentials to unblock the `LLMIntentClassifier` and `LLMResponseGenerator`.
2. **(High Priority) Implement Semantic/Embedding Retrieval**: Replace the TF-IDF retriever with dense embeddings to directly address Failure Mode 2.
3. **(Medium Priority) Calibrate Escalation Thresholds**: Address Failure Mode 3 by replacing rigid blocks with LLM routing.
4. **(Medium Priority) Collect Genuine Human Judgments**: Address the human-label limitation by sourcing human annotators to label the 200 evaluation examples and 30 sampled replies.
