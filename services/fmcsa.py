import requests
from typing import Optional, Dict, Any
from config import FMCSA_API_KEY, FMCSA_API_URL

class FMCSAService:
    def __init__(self):
        self.api_key = FMCSA_API_KEY
        self.base_url = FMCSA_API_URL

    def verify_mc_number(self, mc_number: str) -> Optional[Dict[str, Any]]:
        """Verify an MC number with FMCSA API."""
        url = f"{self.base_url}/{mc_number}"
        params = {"webKey": self.api_key}
        
        try:
            response = requests.get(url, params=params)
            response.raise_for_status()
            data = response.json()
            
            if not data.get('content'):
                return None
                
            return data['content'][0].get('carrier')
        except (requests.exceptions.RequestException, KeyError, IndexError) as e:
            print(f"Error verifying MC number {mc_number}: {e}")
            return None 