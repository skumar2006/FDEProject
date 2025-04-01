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

    def get_load_by_reference(self, reference_number: str, call_type: Optional[str] = None,
                            from_phone: Optional[str] = None, to_phone: Optional[str] = None) -> Optional[Dict[str, Any]]:
        """Get load details by reference number and additional call parameters."""
        if self.loads_df.empty:
            return None
            
        load_data = self.loads_df[self.loads_df['reference_number'] == reference_number]
        if load_data.empty:
            return None
            
        result = load_data.iloc[0].to_dict()
        
        # Add call-related information if provided
        if call_type:
            result['call_type'] = call_type
        if from_phone:
            result['from_phone'] = from_phone
        if to_phone:
            result['to_phone'] = to_phone
            
        return result

    def get_load_by_full_request(self, call_id: str, call_type: str, from_phone: str, 
                               to_phone: str, ref: str) -> Optional[Dict[str, Any]]:
        """Get load details using all parameters from the API request."""
        if self.loads_df.empty:
            return None
            
        load_data = self.loads_df[self.loads_df['reference_number'] == ref]
        if load_data.empty:
            return None
            
        result = load_data.iloc[0].to_dict()
        
        # Add all call-related information
        result.update({
            'call_id': call_id,
            'call_type': call_type,
            'from_phone': from_phone,
            'to_phone': to_phone
        })
            
        return result 