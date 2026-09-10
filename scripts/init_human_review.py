import pandas as pd
from pathlib import Path
import shutil

def main():
    eval_dir = Path("data/evaluation")
    draft_path = eval_dir / "golden_set_annotated.csv"
    ai_draft_backup = eval_dir / "golden_annotation_ai_draft.csv"
    human_queue_path = eval_dir / "golden_set_human_review.csv"
    
    if not draft_path.exists():
        if ai_draft_backup.exists():
            draft_path = ai_draft_backup
        else:
            print(f"Error: {draft_path} not found.")
            return

    df = pd.read_csv(draft_path)
    
    # Preserve the AI draft by simply overwriting the backup path safely
    shutil.copy(draft_path, ai_draft_backup)
    
    # Initialize the human review queue
    review_df = pd.DataFrame()
    review_df['example_id'] = df['example_id']
    review_df['conversation_id'] = df['conversation_id']
    review_df['tweet_id'] = df['tweet_id']
    review_df['customer_message'] = df['customer_message']
    review_df['optional_context'] = df['optional_context']
    review_df['ai_draft_intent'] = df['intent']
    review_df['human_intent'] = ""
    review_df['ambiguity_flag'] = ""
    review_df['human_annotation_notes'] = ""
    review_df['annotation_status'] = "pending_human_review"
    review_df['annotator_id'] = ""
    review_df['annotation_timestamp'] = ""
    
    review_df.to_csv(human_queue_path, index=False)
    print(f"Initialized {human_queue_path} with {len(review_df)} rows.")
    
    # We remove the improperly named golden_set_annotated.csv to enforce using the human set or explicitly the ai draft
    if draft_path.name == "golden_set_annotated.csv":
        draft_path.unlink()
        print(f"Removed {draft_path} to enforce clean data separation.")

if __name__ == "__main__":
    main()
