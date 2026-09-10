import pandas as pd
from pathlib import Path

def main():
    eval_dir = Path("data/evaluation")
    review_queue_path = eval_dir / "golden_set_human_review.csv"
    final_golden_path = eval_dir / "golden_set.csv"
    
    if not review_queue_path.exists():
        print(f"Error: {review_queue_path} does not exist.")
        return
        
    df = pd.read_csv(review_queue_path)
    
    # Validation 1: Exactly 200 examples
    if len(df) != 200:
        print(f"Validation Failed: Expected 200 examples, found {len(df)}.")
        return
        
    # Validation 2: Unique IDs
    if df['example_id'].nunique() != 200:
        print("Validation Failed: Duplicate example_ids found.")
        return
        
    # Validation 3: All must be completed
    pending = df[df['annotation_status'] != 'completed']
    if len(pending) > 0:
        print(f"Validation Failed: There are {len(pending)} examples still pending human review.")
        print("Run `python scripts/review_golden_set.py` to complete them.")
        return
        
    # Validation 4: Valid taxonomy labels
    valid_intents = {
        "Software Bug / Glitch",
        "Device Performance / Hardware",
        "Purchase & Store Operations",
        "Services & Account",
        "How-To / Feature Question",
        "General Complaint / Venting (Other)"
    }
    
    invalid_intents = df[~df['human_intent'].isin(valid_intents)]
    if len(invalid_intents) > 0:
        print(f"Validation Failed: Found {len(invalid_intents)} rows with invalid human_intent.")
        return
        
    # Validation 5: No missing customer messages
    missing_msgs = df[df['customer_message'].isna() | (df['customer_message'] == "")]
    if len(missing_msgs) > 0:
        print("Validation Failed: Found missing customer messages.")
        return
        
    # If valid, compile final set
    final_df = pd.DataFrame()
    final_df['example_id'] = df['example_id']
    final_df['conversation_id'] = df['conversation_id']
    final_df['tweet_id'] = df['tweet_id']
    final_df['customer_message'] = df['customer_message']
    final_df['optional_context'] = df['optional_context']
    final_df['intent'] = df['human_intent']
    final_df['ambiguity_flag'] = df['ambiguity_flag']
    final_df['annotation_notes'] = df['human_annotation_notes']
    final_df['annotation_source'] = "human"
    
    final_df.to_csv(final_golden_path, index=False)
    print(f"SUCCESS: Compiled fully validated human-labelled golden set to {final_golden_path}")

if __name__ == "__main__":
    main()
