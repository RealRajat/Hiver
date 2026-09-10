import argparse
import sys
from pathlib import Path

# Add project root to the path to import the src module
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from src.data.loader import load_twitter_support_data
from src.data.validation import validate_schema, ValidationError

def main():
    parser = argparse.ArgumentParser(description="Inspect the Customer Support on Twitter dataset.")
    parser.add_argument("--data-path", type=str, required=True, help="Path to the dataset CSV file.")
    parser.add_argument("--limit", type=int, default=None, help="Optional limit on the number of rows to load for fast development.")
    
    args = parser.parse_args()
    
    try:
        df = load_twitter_support_data(args.data_path, nrows=args.limit)
    except FileNotFoundError as e:
        print(f"Error: {e}")
        sys.exit(1)
    except ValidationError as e:
        print(f"Error: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"Unexpected error while loading data: {e}")
        sys.exit(1)
        
    metrics = validate_schema(df)
    
    print("Dataset Overview")
    print("----------------")
    print(f"Rows: {metrics['rows']}")
    print(f"Columns: {metrics['columns']}")
    print(f"Memory usage: {metrics['memory_usage_mb']:.2f} MB\n")
    
    print("Direction")
    print("---------")
    print(f"Inbound: {metrics['inbound_count']}")
    print(f"Outbound: {metrics['outbound_count']}\n")
    
    print("Quality")
    print("-------")
    print(f"Missing text: {metrics['missing_text_count']}")
    print(f"Duplicate tweet IDs: {metrics['duplicate_tweet_ids']}")
    print(f"Missing author IDs: {metrics['missing_author_ids']}")
    print(f"Invalid inbound values: {metrics['invalid_inbound_count']}\n")
    
    print("Conversation References")
    print("-----------------------")
    print(f"Rows with in_response_to_tweet_id: {metrics['rows_with_in_response_to_tweet_id']}")
    print(f"Rows with response_tweet_id: {metrics['rows_with_response_tweet_id']}\n")
    
    print("Authors")
    print("-------")
    print(f"Unique author IDs: {metrics['unique_author_ids']}")

if __name__ == "__main__":
    main()
