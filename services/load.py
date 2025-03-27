import pandas as pd
from typing import Optional, Dict, Any
from config import LOAD_DATA_FILE

class LoadService:
    def __init__(self):
        self.loads_df = self._load_data()

    def _load_data(self) -> pd.DataFrame:
        """Load and cache the CSV data."""
        try:
            return pd.read_csv(LOAD_DATA_FILE)
        except FileNotFoundError:
            print(f"Warning: Load data file not found at {LOAD_DATA_FILE}")
            return pd.DataFrame()

    def get_load_by_reference(self, reference_number: str) -> Optional[Dict[str, Any]]:
        """Get load details by reference number."""
        if self.loads_df.empty:
            return None
            
        load_data = self.loads_df[self.loads_df['reference_number'] == reference_number]
        if load_data.empty:
            return None
            
        return load_data.iloc[0].to_dict() 