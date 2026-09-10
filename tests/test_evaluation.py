import pytest
import pandas as pd
from pathlib import Path

def test_annotation_queue_schema_and_size():
    golden_set_path = Path("data/evaluation/golden_annotation_queue.csv")
    assert golden_set_path.exists(), "Annotation queue CSV missing"
    
    df = pd.read_csv(golden_set_path)
    
    # Check size
    assert len(df) == 200, f"Expected 200 rows, found {len(df)}"
    
    # Check schema
    expected_cols = [
        'example_id', 'conversation_id', 'tweet_id', 'customer_message', 
        'optional_context', 'annotation_status', 'intent', 'ambiguity_flag', 'annotation_notes'
    ]
    for col in expected_cols:
        assert col in df.columns, f"Missing column: {col}"
        
    # Check that it is an unreviewed queue without automated labels
    assert (df['annotation_status'] == 'unreviewed').all(), "Queue must be unreviewed"
    assert df['intent'].isna().all() or (df['intent'] == '').all(), "Automated intent labels are strictly prohibited"
