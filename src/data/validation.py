import pandas as pd
from typing import Dict, Any

REQUIRED_COLUMNS = {
    'tweet_id',
    'author_id',
    'inbound',
    'created_at',
    'text',
    'response_tweet_id',
    'in_response_to_tweet_id'
}

class ValidationError(Exception):
    """Exception raised when the dataset fails schema validation."""
    pass

def validate_schema(df: pd.DataFrame) -> Dict[str, Any]:
    """
    Validates the dataset schema and returns a dictionary of data quality metrics.
    
    Args:
        df: The pandas DataFrame containing the dataset.
        
    Returns:
        A dictionary containing various data quality metrics.
        
    Raises:
        ValidationError: If required columns are missing.
    """
    missing_cols = REQUIRED_COLUMNS - set(df.columns)
    if missing_cols:
        raise ValidationError(f"Dataset is missing required columns: {missing_cols}")
    
    # Check duplicate tweet IDs
    duplicate_tweet_ids = int(df['tweet_id'].duplicated().sum())
    
    # Check inbound values (expected boolean-like: True, False, 'True', 'False')
    valid_inbound_values = {True, False, 'True', 'False', 1, 0}
    invalid_inbound_mask = ~df['inbound'].isin(valid_inbound_values)
    invalid_inbound_count = int(invalid_inbound_mask.sum())
    
    # Measure text availability
    missing_text_count = int(df['text'].isna().sum())
    
    # Measure response-reference fields availability
    rows_with_in_response_to = int(df['in_response_to_tweet_id'].notna().sum())
    rows_with_response_to = int(df['response_tweet_id'].notna().sum())
    
    # Memory usage
    memory_usage_mb = float(df.memory_usage(deep=True).sum() / (1024 * 1024))
    
    # Inbound and outbound counts
    inbound_count = int(df['inbound'].isin({True, 'True', 1}).sum())
    outbound_count = int(df['inbound'].isin({False, 'False', 0}).sum())
    
    return {
        "rows": len(df),
        "columns": len(df.columns),
        "memory_usage_mb": memory_usage_mb,
        "inbound_count": inbound_count,
        "outbound_count": outbound_count,
        "missing_text_count": missing_text_count,
        "duplicate_tweet_ids": duplicate_tweet_ids,
        "missing_author_ids": int(df['author_id'].isna().sum()),
        "invalid_inbound_count": invalid_inbound_count,
        "rows_with_in_response_to_tweet_id": rows_with_in_response_to,
        "rows_with_response_tweet_id": rows_with_response_to,
        "unique_author_ids": int(df['author_id'].nunique())
    }
