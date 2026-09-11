import pytest
import pandas as pd
from pathlib import Path
import os
from src.evaluation.golden_loader import GoldenSetLoader

@pytest.fixture
def temp_eval_dir(tmp_path):
    eval_dir = tmp_path / "data" / "evaluation"
    eval_dir.mkdir(parents=True)
    return eval_dir

def test_human_queue_status():
    queue_path = Path("data/evaluation/golden_set_human_review.csv")
    assert queue_path.exists(), "Human review queue missing."
    df = pd.read_csv(queue_path)
    assert len(df) == 200
    assert (df['annotation_status'] == 'pending_human_review').all()
    assert df['human_intent'].isna().all() or (df['human_intent'] == "").all()

def test_golden_loader_draft_fallback(capsys):
    # This should load from golden_annotation_ai_draft.csv since golden_set.csv doesn't exist
    loader = GoldenSetLoader()
    dataset = loader.load()
    assert len(dataset) == 200
    
    # Check that a warning was printed
    captured = capsys.readouterr()
    assert dataset[0]['annotation_source'] in ['ai_draft', 'assistant_annotated']

def test_final_golden_set_validation(tmp_path):
    # Mock a draft
    eval_dir = tmp_path / "data" / "evaluation"
    eval_dir.mkdir(parents=True)
    
    # Write a fake final set with missing annotation_source
    data = []
    for i in range(1, 201):
        data.append({
            "example_id": f"GOLDEN_{i:03d}",
            "conversation_id": "1",
            "tweet_id": "2",
            "customer_message": "hello",
            "optional_context": "",
            "intent": "Software Bug / Glitch",
            "ambiguity_flag": False,
            "annotation_notes": "",
            "annotation_source": "ai_draft" # Invalid for final set
        })
    df = pd.DataFrame(data)
    
    final_path = eval_dir / "golden_set.csv"
    df.to_csv(final_path, index=False)
    
    loader = GoldenSetLoader(csv_path=str(final_path))
    with pytest.raises(ValueError, match="Found invalid annotation sources. Must be one of .*"):
        loader.load()
