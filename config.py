import os
from pathlib import Path

# API Configuration
FMCSA_API_KEY = "cdc33e44d693a3a58451898d4ec9df862c65b954"
FMCSA_API_URL = "https://mobile.fmcsa.dot.gov/qc/services/carriers/docket-number"

# File paths
BASE_DIR = Path(__file__).parent
DATA_DIR = BASE_DIR / "data"
VERIFIED_MCS_FILE = DATA_DIR / "verified_mcs.json"
APPROVED_COMPANIES_FILE = DATA_DIR / "approved_companies.json"
LOAD_DATA_FILE = DATA_DIR / "load_data.csv"

# Create data directory if it doesn't exist
DATA_DIR.mkdir(exist_ok=True)

# Default approved companies if file doesn't exist
DEFAULT_APPROVED_COMPANIES = [
    "ABC Trucking Inc",
    "XYZ Logistics LLC",
    "Best Haulers Ltd",
    "GREYHOUND AUTO TRANSPORT"  # Added based on your example
] 