import pytest
import pandas as pd
from pathlib import Path

def test_annotation_queue_schema_and_size():
    golden_set_path = Path("data/evaluation/golden_annotation_review_queue.csv")
    assert golden_set_path.exists(), "Annotation review queue CSV missing"
    
    df = pd.read_csv(golden_set_path)
    
    # Check size and ID validation
    assert len(df) == 200, f"Expected 200 rows, found {len(df)}"
    assert df['example_id'].is_unique, "example_ids are not unique"
    
    # Assert IDs match the exact pattern GOLDEN_\d{3} (no backslashes)
    assert df['example_id'].str.match(r'^GOLDEN_\d{3}$').all(), "example_id contains invalid formatting (e.g., escaped backslashes)"
    
    expected_ids = {f"GOLDEN_{i:03d}" for i in range(1, 201)}
    actual_ids = set(df['example_id'])
    assert expected_ids == actual_ids, "example_id values do not exactly match GOLDEN_001 through GOLDEN_200"
    
    # Check schema
    expected_cols = [
        'example_id', 'conversation_id', 'tweet_id', 'customer_message', 
        'optional_context', 'annotation_status', 'intent', 'ambiguity_flag', 'annotation_notes', 'annotation_source'
    ]
    for col in expected_cols:
        assert col in df.columns, f"Missing column: {col}"
        
    # Check that labels are from the valid taxonomy
    valid_intents = [
        'Software Bug / Glitch',
        'Device Performance / Hardware',
        'Purchase & Store Operations',
        'Services & Account',
        'How-To / Feature Question',
        'General Complaint / Venting (Other)'
    ]
    
    invalid_labels = df[~df['intent'].isin(valid_intents) & df['intent'].notna()]
    assert len(invalid_labels) == 0, f"Found invalid intent labels: {invalid_labels['intent'].unique()}"
    
    # Check annotation source is NOT human
    assert (df['annotation_source'] != 'human_reviewed').all(), "Queue claims to be human_reviewed but it is not."
    assert (df['annotation_source'] == 'ai_draft').all(), "Queue must be marked as ai_draft."
