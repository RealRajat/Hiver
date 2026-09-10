import pandas as pd
from pathlib import Path

def main():
    csv_path = Path("data/evaluation/golden_annotation_review_queue.csv")
    df = pd.read_csv(csv_path)
    
    # 1. Normalize example_id
    df['example_id'] = df['example_id'].astype(str).str.replace(r'\\_', '_', regex=True)
    
    # 2. Verify IDs
    assert len(df) == 200, f"Expected 200 rows, got {len(df)}"
    assert df['example_id'].is_unique, "example_ids are not unique!"
    expected_ids = [f"GOLDEN_{i:03d}" for i in range(1, 201)]
    actual_ids = df['example_id'].tolist()
    assert set(expected_ids) == set(actual_ids), "Missing or extra expected IDs!"
    
    # 3. Apply corrections
    corrections = {
        'GOLDEN_037': 'Software Bug / Glitch',
        'GOLDEN_039': 'Software Bug / Glitch',
        'GOLDEN_046': 'Software Bug / Glitch',
        'GOLDEN_056': 'General Complaint / Venting (Other)',
        'GOLDEN_057': 'Software Bug / Glitch',
        'GOLDEN_081': 'Software Bug / Glitch',
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
        # Quick validation check: ensure the ID actually exists before modifying
        if ex_id in df['example_id'].values:
            df.loc[df['example_id'] == ex_id, 'intent'] = new_intent
        else:
            print(f"WARNING: Could not find {ex_id}")
            
    # Save the repaired queue
    df.to_csv(csv_path, index=False)
    
    # --- Generate Report Data ---
    print("\n--- 2. Final Intent Distribution ---")
    print(df['intent'].value_counts(dropna=False))
    
    print("\n--- 3. Exact labels for 16 corrected IDs ---")
    for ex_id in corrections.keys():
        intent = df.loc[df['example_id'] == ex_id, 'intent'].values[0]
        print(f"{ex_id}: {intent}")
        
    print("\n--- 4. ID Validation Result ---")
    print("200 unique normalized IDs confirmed: GOLDEN_001 through GOLDEN_200.")
    print(f"Ambiguity flags: {df['ambiguity_flag'].sum()}")
    print(f"All annotation_source == ai_draft: {(df['annotation_source'] == 'ai_draft').all()}")
    print(f"Any human_reviewed rows: {(df['annotation_source'] == 'human_reviewed').any()}")

if __name__ == '__main__':
    main()
