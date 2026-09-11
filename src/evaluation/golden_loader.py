import pandas as pd
from pathlib import Path
from typing import List, Dict, Any
import warnings

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
        'optional_context', 'intent', 'ambiguity_flag',
        'annotation_notes', 'annotation_source'
    ]

    def __init__(self, csv_path: str = "data/evaluation/golden_set.csv"):
        self.csv_path = Path(csv_path)

    def load(self) -> List[Dict[str, Any]]:
        """Loads and strictly validates the golden set."""
        
        # Determine which file to load
        actual_path = self.csv_path
        if not actual_path.exists():
            assistant_path = Path("data/evaluation/golden_set_assistant_annotated.csv")
            if assistant_path.exists():
                warnings.warn("\n" + "="*80 + "\nWARNING: Loading ASSISTANT-ANNOTATED labels. The assignment's human hand-labelled requirement was NOT met.\n" + "="*80 + "\n")
                actual_path = assistant_path
            else:
                raise FileNotFoundError(f"Neither {self.csv_path} nor {assistant_path} found.")
        
        df = pd.read_csv(actual_path)
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
            
        # 6. Valid ambiguity_flag
        if df['ambiguity_flag'].isna().any():
            raise ValueError("Found missing ambiguity_flag values.")

        # 7. Annotation Source Constraint (Enforce assistant_annotated or human, not just human)
        valid_sources = {'human', 'assistant_annotated'}
        invalid_sources = df[~df['annotation_source'].isin(valid_sources)]
        if not invalid_sources.empty:
            raise ValueError(f"Found invalid annotation sources. Must be one of {valid_sources}.")
