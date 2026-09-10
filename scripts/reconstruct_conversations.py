import argparse
import sys
import json
import statistics
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from src.conversations.conversation_reconstructor import reconstruct_brand_conversations

def generate_markdown_report(conversations, output_path: Path, target_brand: str):
    num_convs = len(conversations)
    total_tweets = sum(c['tweet_count'] for c in conversations)
    
    lengths = [c['tweet_count'] for c in conversations]
    avg_len = sum(lengths) / num_convs if num_convs > 0 else 0
    med_len = statistics.median(lengths) if num_convs > 0 else 0
    
    cust_msgs = sum(c['customer_message_count'] for c in conversations)
    supp_msgs = sum(c['support_message_count'] for c in conversations)
    
    # Missing parent anomalies can be loosely inferred if customer messages exist 
    # but the conversation root is the brand's response (meaning the customer's initiating tweet is missing).
    # We won't assert complex missing parents, but we will document the structural reality.
    
    md_content = f"""# {target_brand} Conversation Reconstruction Report

## Dataset Scope
- **Target Account**: `{target_brand}`
- **Conversations Reconstructed**: {num_convs:,}
- **Total Tweets Processed**: {total_tweets:,}

## Conversation Statistics
- **Average Conversation Length**: {avg_len:.2f} tweets
- **Median Conversation Length**: {med_len} tweets
- **Total Customer Messages**: {cust_msgs:,}
- **Total Support Messages**: {supp_msgs:,}

## Data Quality
- **Missing Parents / Orphaned Records**: A conversation thread is strictly defined by the unbroken `in_response_to_tweet_id` graph. If a parent tweet was deleted or the dataset scrape missed it, the thread is broken into separate fragments. The dataset contains numerous such fragments, treating them deterministically as independent conversations.
- **Duplicate IDs**: No duplicate resolution was forced; the dataset relies on the raw `tweet_id` index.
- **Malformed References**: Any reference pointing to a non-existent dataset tweet safely results in the reference itself acting as a root.

## Methodology
Conversations were reconstructed deterministically:
1. **Root Resolution**: Every tweet's `in_response_to_tweet_id` was traversed upwards until reaching a root tweet (either no parent, or a parent missing from the dataset).
2. **Grouping**: All tweets resolving to the same root were grouped into a single `conversation_id` equal to the root's `tweet_id`.
3. **Filtering**: Only conversations containing at least one tweet authored by `{target_brand}` were extracted.
4. **Ordering**: Tweets within each conversation were chronologically sorted using `created_at`.

## Limitations
- **Identifiable Threads vs. Support Cases**: These are structurally identifiable Twitter threads. They do not perfectly map 1:1 with real-world support cases (e.g., a customer might start a fresh unthreaded mention).
- **Resolution Guarantee**: Structural reconstruction does NOT guarantee or imply that the customer's issue was resolved. The conversation may end abruptly.

## Output
Corpus generated at: `data/processed/{target_brand.lower()}_conversations.jsonl`
"""
    output_path.write_text(md_content, encoding='utf-8')


def main():
    parser = argparse.ArgumentParser(description="Reconstruct conversations for a target brand.")
    parser.add_argument("--data-path", type=str, default="data/raw/twcs.csv", help="Path to raw dataset.")
    parser.add_argument("--output-dir", type=str, default="data/processed", help="Directory for JSONL corpus.")
    parser.add_argument("--brand", type=str, default="AppleSupport", help="Support account to extract.")
    args = parser.parse_args()
    
    data_path = Path(args.data_path)
    if not data_path.exists():
        print(f"Error: Dataset not found at {data_path}")
        sys.exit(1)
        
    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    
    print(f"Reconstructing conversations for {args.brand}...")
    try:
        conversations = reconstruct_brand_conversations(data_path, args.brand)
    except Exception as e:
        print(f"Failed to reconstruct conversations: {e}")
        sys.exit(1)
        
    jsonl_path = output_dir / f"{args.brand.lower()}_conversations.jsonl"
    
    print(f"Writing {len(conversations)} conversations to {jsonl_path}...")
    with open(jsonl_path, 'w', encoding='utf-8') as f:
        for conv in conversations:
            f.write(json.dumps(conv) + '\n')
            
    reports_dir = Path("reports")
    reports_dir.mkdir(parents=True, exist_ok=True)
    md_path = reports_dir / f"{args.brand.lower()}_conversation_reconstruction.md"
    
    generate_markdown_report(conversations, md_path, args.brand)
    
    print(f"Reconstruction complete.")
    print(f"Report saved to: {md_path}")

if __name__ == "__main__":
    main()
