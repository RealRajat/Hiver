import pytest
import pandas as pd
from pathlib import Path
import tempfile
import os
import sys

# Add project root to the path to import the src module
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from src.data.validation import validate_schema, ValidationError
from src.data.loader import load_twitter_support_data

@pytest.fixture
def valid_data():
    return pd.DataFrame({
        'tweet_id': [1, 2],
        'author_id': ['A', 'B'],
        'inbound': [True, False],
        'created_at': ['2023-01-01', '2023-01-02'],
        'text': ['Hello', 'World'],
        'response_tweet_id': ['3', None],
        'in_response_to_tweet_id': [None, '1']
    })

def test_valid_schema(valid_data):
    metrics = validate_schema(valid_data)
    assert metrics['rows'] == 2
    assert metrics['columns'] == 7
    assert metrics['duplicate_tweet_ids'] == 0
    assert metrics['invalid_inbound_count'] == 0
    assert metrics['missing_text_count'] == 0

def test_missing_required_column(valid_data):
    invalid_data = valid_data.drop(columns=['text'])
    with pytest.raises(ValidationError, match="Dataset is missing required columns"):
        validate_schema(invalid_data)

def test_duplicate_tweet_ids(valid_data):
    # Create duplicate tweet_id
    duplicate_data = pd.concat([valid_data, valid_data.iloc[[0]]], ignore_index=True)
    metrics = validate_schema(duplicate_data)
    assert metrics['duplicate_tweet_ids'] == 1

def test_invalid_inbound(valid_data):
    invalid_data = valid_data.copy()
    invalid_data['inbound'] = invalid_data['inbound'].astype(object)
    invalid_data.loc[0, 'inbound'] = 'InvalidValue'
    metrics = validate_schema(invalid_data)
    assert metrics['invalid_inbound_count'] == 1

def test_missing_file():
    with pytest.raises(FileNotFoundError):
        load_twitter_support_data("non_existent_file.csv")

def test_limited_loading(valid_data):
    # Save to a temporary CSV
    with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.csv') as tmp:
        valid_data.to_csv(tmp.name, index=False)
        tmp_path = tmp.name

    try:
        # Load with nrows=1
        df = load_twitter_support_data(tmp_path, nrows=1)
        assert len(df) == 1
        assert df['tweet_id'].iloc[0] == 1
    finally:
        os.remove(tmp_path)
