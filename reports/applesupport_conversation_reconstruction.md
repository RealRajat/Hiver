# AppleSupport Conversation Reconstruction Report

## Dataset Scope
- **Target Account**: `AppleSupport`
- **Conversations Reconstructed**: 80,702
- **Total Tweets Processed**: 238,907

## Conversation Statistics
- **Average Conversation Length**: 2.96 tweets
- **Median Conversation Length**: 2.0 tweets
- **Total Customer Messages**: 131,764
- **Total Support Messages**: 107,143

## Data Quality
- **Missing Parents / Orphaned Records**: A conversation thread is strictly defined by the unbroken `in_response_to_tweet_id` graph. If a parent tweet was deleted or the dataset scrape missed it, the thread is broken into separate fragments. The dataset contains numerous such fragments, treating them deterministically as independent conversations.
- **Duplicate IDs**: No duplicate resolution was forced; the dataset relies on the raw `tweet_id` index.
- **Malformed References**: Any reference pointing to a non-existent dataset tweet safely results in the reference itself acting as a root.

## Methodology
Conversations were reconstructed deterministically:
1. **Root Resolution**: Every tweet's `in_response_to_tweet_id` was traversed upwards until reaching a root tweet (either no parent, or a parent missing from the dataset).
2. **Grouping**: All tweets resolving to the same root were grouped into a single `conversation_id` equal to the root's `tweet_id`.
3. **Filtering**: Only conversations containing at least one tweet authored by `AppleSupport` were extracted.
4. **Ordering**: Tweets within each conversation were chronologically sorted using `created_at`.

## Limitations
- **Identifiable Threads vs. Support Cases**: These are structurally identifiable Twitter threads. They do not perfectly map 1:1 with real-world support cases (e.g., a customer might start a fresh unthreaded mention).
- **Resolution Guarantee**: Structural reconstruction does NOT guarantee or imply that the customer's issue was resolved. The conversation may end abruptly.

## Output
Corpus generated at: `data/processed/applesupport_conversations.jsonl`
