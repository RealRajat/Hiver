import pandas as pd
from pathlib import Path

def semantic_correction(row):
    text = str(row['customer_message']).lower()
    intent = str(row['intent'])
    ambig = row['ambiguity_flag']
    notes = str(row['annotation_notes'])
    
    # 1. Product Name confusion correction
    # AI often thinks "iphone" means Device Performance or Purchase.
    # But if there's no verb, it's just a general complaint or ambiguous.
    
    # 2. Short replies missing context
    if len(text.split()) < 4:
        ambig = True
        notes = "Short message; requires surrounding context for true intent."
        if intent not in ['General Complaint / Venting (Other)', 'How-To / Feature Question']:
            intent = 'General Complaint / Venting (Other)'
            
    # 3. Valid intents check
    valid_intents = [
        'Software Bug / Glitch',
        'Device Performance / Hardware',
        'Purchase & Store Operations',
        'Services & Account',
        'How-To / Feature Question',
        'General Complaint / Venting (Other)'
    ]
    if intent not in valid_intents:
        intent = 'General Complaint / Venting (Other)'
        ambig = True
        notes += " | Originally invalid AI intent."
        
    return pd.Series({'intent': intent, 'ambiguity_flag': ambig, 'annotation_notes': notes})

def main():
    input_path = Path("data/evaluation/golden_annotation_ai_draft.csv")
    output_path = Path("data/evaluation/golden_annotation_review_queue.csv")
    
    if not input_path.exists():
        print(f"File not found: {input_path}")
        return
        
    df = pd.read_csv(input_path)
    print(f"Loaded {len(df)} records from AI draft.")
    
    # Apply semantic corrections
    corrections = df.apply(semantic_correction, axis=1)
    df['intent'] = corrections['intent']
    df['ambiguity_flag'] = corrections['ambiguity_flag']
    df['annotation_notes'] = corrections['annotation_notes']
    
    # Add annotation source column
    df['annotation_source'] = 'ai_draft'
    
    # Save the review queue
    df.to_csv(output_path, index=False)
    print(f"Saved review queue to: {output_path}")

if __name__ == "__main__":
    main()
