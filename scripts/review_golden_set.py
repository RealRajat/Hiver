import pandas as pd
import argparse
from pathlib import Path
from datetime import datetime
import os

TAXONOMY = {
    "1": "Software Bug / Glitch",
    "2": "Device Performance / Hardware",
    "3": "Purchase & Store Operations",
    "4": "Services & Account",
    "5": "How-To / Feature Question",
    "6": "General Complaint / Venting (Other)"
}

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def main():
    parser = argparse.ArgumentParser(description="Human Review CLI for Golden Set")
    parser.add_argument("--hide-ai-label", action="store_true", help="Hide AI draft labels for blind annotation")
    parser.add_argument("--resume", action="store_true", help="Resume from the first pending example")
    parser.add_argument("--annotator", type=str, default="human_reviewer_1", help="Annotator ID")
    args = parser.parse_args()

    queue_path = Path("data/evaluation/golden_set_human_review.csv")
    if not queue_path.exists():
        print(f"Error: {queue_path} does not exist. Please initialize the queue first.")
        return

    df = pd.read_csv(queue_path)
    
    # Fill NAs
    df.fillna("", inplace=True)
    
    pending_idx = df.index[df['annotation_status'] == 'pending_human_review'].tolist()
    
    if not pending_idx:
        print("All 200 examples have been human-annotated!")
        return
        
    print(f"Found {len(pending_idx)} pending examples. Starting review...\n")
    
    for idx in pending_idx:
        row = df.loc[idx]
        clear_screen()
        print("="*60)
        print(f"EXAMPLE ID: {row['example_id']}")
        print(f"PROGRESS:   {200 - len(pending_idx)}/200 completed")
        print("="*60)
        print(f"\nCUSTOMER MESSAGE:\n{row['customer_message']}\n")
        
        if row['optional_context']:
            print(f"CONTEXT:\n{row['optional_context']}\n")
            
        if not args.hide_ai_label:
            print(f"[DRAFT] AI Proposed Intent: {row['ai_draft_intent']}")
            print("WARNING: Treat the AI draft as a suggestion only. Do not accept it automatically.\n")
            
        print("TAXONOMY:")
        for k, v in TAXONOMY.items():
            print(f"  {k}. {v}")
            
        print("\nSelect an intent (1-6) or 'q' to quit and save progress:")
        while True:
            choice = input("> ").strip().lower()
            if choice == 'q':
                print("Saving progress and exiting...")
                df.to_csv(queue_path, index=False)
                return
            if choice in TAXONOMY:
                selected_intent = TAXONOMY[choice]
                break
            print("Invalid choice. Please enter 1-6 or 'q'.")
            
        print("\nIs this example genuinely ambiguous? (y/n/q):")
        while True:
            ambig = input("> ").strip().lower()
            if ambig == 'q':
                print("Saving progress and exiting...")
                df.to_csv(queue_path, index=False)
                return
            if ambig in ['y', 'n']:
                is_ambiguous = "true" if ambig == 'y' else "false"
                break
            print("Invalid choice. Please enter 'y' or 'n'.")
            
        notes = ""
        if is_ambiguous == "true":
            print("\nPlease provide brief notes explaining the ambiguity:")
            notes = input("> ").strip()
            
        # Update DataFrame
        df.at[idx, 'human_intent'] = selected_intent
        df.at[idx, 'ambiguity_flag'] = is_ambiguous
        df.at[idx, 'human_annotation_notes'] = notes
        df.at[idx, 'annotation_status'] = "completed"
        df.at[idx, 'annotator_id'] = args.annotator
        df.at[idx, 'annotation_timestamp'] = datetime.utcnow().isoformat()
        
        # Save after every interaction
        df.to_csv(queue_path, index=False)
        pending_idx.remove(idx)
        
    print("\nAll 200 examples have been annotated! You can now compile the final golden set.")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nReview interrupted. Progress is automatically saved.")
