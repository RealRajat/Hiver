import pandas as pd
from pathlib import Path
from typing import Optional, Union

from .validation import validate_schema, ValidationError

def load_twitter_support_data(path: Union[str, Path], nrows: Optional[int] = None) -> pd.DataFrame:
    """
    Loads the Customer Support on Twitter dataset.
    
    Args:
        path: Path to the dataset CSV file.
        nrows: Optional limit on the number of rows to load.
        
    Returns:
        A pandas DataFrame containing the loaded data.
        
    Raises:
        FileNotFoundError: If the specified file does not exist.
        ValidationError: If the loaded dataset fails schema validation.
    """
    filepath = Path(path)
    if not filepath.exists():
        raise FileNotFoundError(f"Dataset not found at {filepath}")
        
    try:
        # Load the CSV, specifying low_memory=False to avoid mixed type warnings on large files
        df = pd.read_csv(filepath, nrows=nrows, low_memory=False)
    except Exception as e:
        raise RuntimeError(f"Failed to read CSV at {filepath}: {e}")
        
    # Validate schema
    # (Note: we just call validate_schema to ensure it doesn't raise an exception on required columns)
    validate_schema(df)
        
    return df
