import json
from typing import Dict, List, Optional, Tuple
from pathlib import Path
from config import VERIFIED_MCS_FILE, APPROVED_COMPANIES_FILE, DEFAULT_APPROVED_COMPANIES

class VerificationService:
    def __init__(self):
        self.verified_mcs = self._load_verified_mcs()
        self.approved_companies = self._load_approved_companies()

    def _load_verified_mcs(self) -> Dict[str, bool]:
        """Load verified MCs from file."""
        try:
            with open(VERIFIED_MCS_FILE, 'r') as f:
                data = json.load(f)
                return data.get('verified_mcs', {})
        except (FileNotFoundError, json.JSONDecodeError):
            return {}

    def _load_approved_companies(self) -> List[str]:
        try:
            with open(APPROVED_COMPANIES_FILE, 'r') as f:
                data = json.load(f)
                return data.get('approved_companies', DEFAULT_APPROVED_COMPANIES)
        except (FileNotFoundError, json.JSONDecodeError):
            return DEFAULT_APPROVED_COMPANIES

    def _save_verified_mcs(self):
        """Save verified MCs to file."""
        with open(VERIFIED_MCS_FILE, 'w') as f:
            json.dump({'verified_mcs': self.verified_mcs}, f)

    def verify_mc(self, mc_number: str, dba_name: Optional[str] = None) -> Tuple[bool, str]:
        """Verify if an MC number exists in FMCSA and its DBA name is in the approved list."""
        # Check if MC exists in FMCSA
        if not dba_name:
            return False, "MC number not found in FMCSA database"
            
        # Check if DBA name is in approved list
        is_verified = dba_name in self.approved_companies
        self.verified_mcs[mc_number] = is_verified
        self._save_verified_mcs()
        
        if is_verified:
            return True, "MC number verified successfully"
        else:
            return False, "DBA name not in approved list"

    def get_verification_status(self, mc_number: str) -> Optional[bool]:
        """Get verification status for an MC number."""
        return self.verified_mcs.get(mc_number)

    def get_all_verified_mcs(self) -> Dict[str, bool]:
        """Get all verified MC numbers and their status."""
        return self.verified_mcs 