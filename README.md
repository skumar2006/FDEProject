# Load Checker & MC Verification API

A REST API for verifying MC numbers against the FMCSA database and checking load availability.

## Features

- MC Number Verification using FMCSA API
  - Checks if MC number exists in FMCSA database
  - Verifies DBA name against approved company list
  - Stores verification results for future reference
- Load Availability Checker from CSV data
- FastAPI-based REST API with automatic documentation
- Persistent storage of verification results

## Setup

1. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run the API:
```bash
python main.py
```

The API will be available at `http://localhost:8000`

## API Documentation

Once the server is running, visit:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`


### MC Verification

1. Verify MC Number
```
POST /verify_mc
Request:
{
    "mc_number": "123456"
}

Response:
{
    "mc_number": "123456",
    "verified": true/false,
    "message": "Detailed status message"
}
```

2. Check Verification Status
```
GET /status/{mc_number}

Response:
{
    "mc_number": "123456",
    "verified": true/false,
    "message": "Previously verified" or "Previously rejected"
}
```

3. List All Verified MCs
```
GET /verified_mcs

Response:
{
    "verified_mcs": {
        "123456": true,
        "789012": false
    }
}
```

### Load Checker

1. Get Load by Reference Number
```
GET /loads/{reference_number}

Response:
{
    "reference_number": "REF09460",
    "origin": "Denver CO",
    "destination": "Detroit MI",
    "equipment_type": "Dry Van",
    "rate": 868,
    "commodity": "Automotive Parts"
}
```

## Data Files

The API uses the following data files in the `data` directory:
- `approved_companies.json`: List of approved company names
- `load_data.csv`: Available loads data
- `verified_mcs.json`: Storage for MC verification results

## Error Handling

The API returns appropriate HTTP status codes:
- 200: Success
- 400: Bad Request
- 404: Not Found
- 500: Internal Server Error

## Example Usage

```bash
# Verify an MC number
curl -X POST http://localhost:8000/verify_mc \
     -H "Content-Type: application/json" \
     -d '{"mc_number": "551149"}'

# Check verification status
curl http://localhost:8000/status/551149

# Get load details
curl http://localhost:8000/loads/REF09460
```