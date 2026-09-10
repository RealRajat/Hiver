import pandas as pd
from pathlib import Path

def main():
    csv_path = Path("data/evaluation/golden_annotation_review_queue.csv")
    df = pd.read_csv(csv_path)
    
    print("1. Count of each intent value:")
    print(df['intent'].value_counts(dropna=False))
    
    print("\n2. Current intent for exact IDs:")
    ids_to_check = [
        'GOLDEN_037', 'GOLDEN_039', 'GOLDEN_046', 'GOLDEN_056', 'GOLDEN_057', 
        'GOLDEN_081', 'GOLDEN_117', 'GOLDEN_120', 'GOLDEN_137', 'GOLDEN_148', 
        'GOLDEN_154', 'GOLDEN_156', 'GOLDEN_157', 'GOLDEN_177', 'GOLDEN_187', 'GOLDEN_191'
    ]
    for ex_id in ids_to_check:
        intent = df.loc[df['example_id'] == ex_id, 'intent'].values
        if len(intent) > 0:
            print(f"{ex_id} -> {intent[0]}")
        else:
            print(f"{ex_id} -> NOT FOUND")
            
    print("\n4. Confirmations:")
    print(f"Total rows: {len(df)}")
    print(f"Ambiguity flags: {df['ambiguity_flag'].sum()}")
    print(f"All annotation_source == ai_draft: {(df['annotation_source'] == 'ai_draft').all()}")
    print(f"Any human_reviewed rows: {(df['annotation_source'] == 'human_reviewed').any()}")

if __name__ == '__main__':
    main()
