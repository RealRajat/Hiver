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

## Decision: Golden Evaluation Set Correction (Manual Annotation Required)

### Decision
Rejected the automatically generated keyword labels for the golden evaluation set. Created `data/evaluation/golden_annotation_queue.csv` to serve as a manual annotation queue, preserving the original 200 sampled items.

### Reasoning
The golden set serves as the ground-truth benchmark for evaluating the AI agent's intent classifier. If the golden set itself is generated via automated keyword heuristics, any future classifier that replicates those heuristics will artificially score 100%, while a superior classifier that understands nuance might score poorly. Therefore, genuine human annotation is strictly required.

### Evidence
The Hiver assignment specification mandates *hand-labelled* golden examples.

### Trade-offs
This requires pausing the AI development pipeline to wait for manual human review of the 200 examples.

### Consequences
The evaluation set will remain pending (`Phase 4 — Golden Evaluation Set: Annotation In Progress`) until a human reviewer completes the queue and freezes the final labels.
