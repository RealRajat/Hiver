import pandas as pd
from pathlib import Path
from typing import List, Dict, Any

class GoldenSetLoader:
    """
    Loads and validates the 200-example golden evaluation dataset.
    """
    
    VALID_INTENTS = {
        'Software Bug / Glitch',
        'Device Performance / Hardware',
        'Purchase & Store Operations',
        'Services & Account',
        'How-To / Feature Question',
        'General Complaint / Venting (Other)'
    }
    
    REQUIRED_COLUMNS = [
        'example_id', 'conversation_id', 'tweet_id', 'customer_message',
        'optional_context', 'annotation_status', 'intent', 'ambiguity_flag',
        'annotation_notes', 'annotation_source'
    ]

    def __init__(self, csv_path: str = "data/evaluation/golden_set_annotated.csv"):
        self.csv_path = Path(csv_path)

    def load(self) -> List[Dict[str, Any]]:
        """Loads and strictly validates the golden set."""
        if not self.csv_path.exists():
            raise FileNotFoundError(f"Golden set not found at {self.csv_path}")
            
        df = pd.read_csv(self.csv_path)
        self._validate_schema(df)
        
        return df.to_dict(orient='records')

    def _validate_schema(self, df: pd.DataFrame):
        # 1. Row count
        if len(df) != 200:
            raise ValueError(f"Golden set must contain exactly 200 examples, found {len(df)}")
            
        # 2. Required columns
        missing_cols = set(self.REQUIRED_COLUMNS) - set(df.columns)
        if missing_cols:
            raise ValueError(f"Missing required columns: {missing_cols}")
            
        # 3. Unique IDs
        if not df['example_id'].is_unique:
            raise ValueError("example_id column contains duplicates.")
            
        # 4. Valid intent labels
        invalid_intents = df[~df['intent'].isin(self.VALID_INTENTS)]
        if not invalid_intents.empty:
            raise ValueError(f"Found invalid intent labels: {invalid_intents['intent'].unique()}")
            
        # 5. Missing customer_message
        if df['customer_message'].isna().any() or (df['customer_message'] == "").any():
            raise ValueError("Found missing customer_message values.")
            
        # 6. Valid ambiguity_flag (must be bool-like)
        if df['ambiguity_flag'].isna().any():
            raise ValueError("Found missing ambiguity_flag values.")
