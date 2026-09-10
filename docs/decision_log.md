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
