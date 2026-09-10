import argparse
import sys
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from src.profiling.brand_profiler import profile_brands

def generate_markdown_report(df, output_path: Path):
    top_candidates = df.head(10)
    
    md_content = f"""# Brand Profiling Report

## Methodology
Candidate support accounts were identified heuristically by locating all `author_id`s that authored at least one outbound tweet (`inbound == False`). 

## Dataset Scope
The profiling used the full provided dataset, loaded memory-consciously by extracting only the relational and identification columns (`tweet_id`, `author_id`, `inbound`, `in_response_to_tweet_id`).

## Conversation Methodology
An identifiable conversation/thread is determined deterministically by resolving the `in_response_to_tweet_id` graph. Every tweet's parent path is traversed to find its root tweet. All tweets sharing the same root are grouped into a single conversation.

## Metrics
- **total_tweets**: Sum of inbound customer tweets directed at the brand and outbound replies from the brand.
- **inbound_tweets**: Number of customer tweets (`inbound == True`) that replied directly to the brand's tweets.
- **outbound_tweets**: Number of support tweets (`inbound == False`) authored by the brand.
- **unique_customers**: Number of distinct customer `author_id`s that either replied to the brand or were replied to by the brand.
- **conversation_count**: Number of identifiable conversation threads involving the support account.
- **multi_turn_conversations**: Threads containing more than one interaction/message.
- **multi_turn_rate**: Ratio of multi-turn conversations to total conversations.
- **avg_conversation_length**: Average number of messages per identifiable conversation.
- **cust_support_participating_convs**: Conversations containing both a customer message (`inbound == True`) and a support message (`inbound == False`).

## Candidate Comparison (Top 10 by Volume)

{top_candidates.to_markdown(index=False)}

## Limitations
- **Lack of explicit brand labels**: Brands are inferred strictly from outbound behavior.
- **Incomplete conversation references**: Tweets that lack a valid `in_response_to_tweet_id` cannot be reliably linked to a customer/brand interaction.
- **Identifiable vs Real-World**: These metrics reflect *identifiable dataset threads*, not guaranteed real-world support cases. The dataset contains deleted parent tweets, unthreaded mentions, and missing context that naturally break conversations into smaller disjoint fragments.

## Reproducibility
```bash
python scripts/profile_brands.py --data-path data/raw/twcs.csv --output-dir reports
```
"""
    output_path.write_text(md_content, encoding='utf-8')


def main():
    parser = argparse.ArgumentParser(description="Profile brands in the TWCS dataset.")
    parser.add_argument("--data-path", type=str, required=True, help="Path to the dataset CSV file.")
    parser.add_argument("--output-dir", type=str, default="reports", help="Directory to save the reports.")
    args = parser.parse_args()
    
    data_path = Path(args.data_path)
    if not data_path.exists():
        print(f"Error: Dataset not found at {data_path}")
        sys.exit(1)
        
    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    
    print("Profiling brands... This may take a moment for large datasets.")
    try:
        profile_df = profile_brands(data_path)
    except Exception as e:
        print(f"Failed to profile dataset: {e}")
        sys.exit(1)
        
    csv_path = output_dir / "brand_profile.csv"
    md_path = output_dir / "brand_profiling.md"
    
    profile_df.to_csv(csv_path, index=False)
    generate_markdown_report(profile_df, md_path)
    
    print(f"Profiling complete. Found {len(profile_df)} candidate brands.")
    print(f"CSV saved to: {csv_path}")
    print(f"Markdown report saved to: {md_path}")

if __name__ == "__main__":
    main()
