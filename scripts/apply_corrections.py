import pandas as pd
from pathlib import Path

def main():
    csv_path = Path("data/evaluation/golden_annotation_review_queue.csv")
    df = pd.read_csv(csv_path)
    
    corrections = {
        'GOLDEN_037': 'Software Bug / Glitch',
        'GOLDEN_039': 'Software Bug / Glitch',
        'GOLDEN_046': 'Software Bug / Glitch',
        'GOLDEN_056': 'General Complaint / Venting (Other)',
        'GOLDEN_057': 'Software Bug / Glitch',
        'GOLDEN_081': 'Software Bug / Glitch',
        'GOLDEN_091': 'General Complaint / Venting (Other)',
        'GOLDEN_117': 'Purchase & Store Operations',
        'GOLDEN_120': 'General Complaint / Venting (Other)',
        'GOLDEN_137': 'Services & Account',
        'GOLDEN_148': 'General Complaint / Venting (Other)',
        'GOLDEN_154': 'General Complaint / Venting (Other)',
        'GOLDEN_156': 'Device Performance / Hardware',
        'GOLDEN_157': 'General Complaint / Venting (Other)',
        'GOLDEN_177': 'Software Bug / Glitch',
        'GOLDEN_187': 'General Complaint / Venting (Other)',
        'GOLDEN_191': 'General Complaint / Venting (Other)'
    }
    
    for ex_id, new_intent in corrections.items():
        df.loc[df['example_id'] == ex_id, 'intent'] = new_intent
        
    # Ensure no human_reviewed flag is set
    assert (df['annotation_source'] != 'human_reviewed').all(), "Found human_reviewed flag!"
    
    df.to_csv(csv_path, index=False)
    
    # Print metrics for the report
    print("\n--- Intent Distribution ---")
    print(df['intent'].value_counts(dropna=False))
    print("\nAmbiguous Count:", df['ambiguity_flag'].sum())
    
if __name__ == '__main__':
    main()
