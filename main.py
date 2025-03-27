from fastapi import FastAPI, HTTPException, Query, Path
from pydantic import BaseModel
from typing import Dict, List, Optional
from services.fmcsa import FMCSAService
from services.load import LoadService
from services.verification import VerificationService
import urllib.parse
from starlette.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title="Load Checker & MC Verification API",
    description="API for verifying MC numbers and checking load availability",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize services
fmcsa_service = FMCSAService()
load_service = LoadService()
verification_service = VerificationService()

class MCVerificationRequest(BaseModel):
    mc_number: str

class MCVerificationResponse(BaseModel):
    mc_number: str
    verified: bool
    message: str

class LoadResponse(BaseModel):
    reference_number: str
    origin: str
    destination: str
    equipment_type: str
    rate: float
    commodity: str

@app.post("/verify_mc", response_model=MCVerificationResponse)
async def verify_mc(request: MCVerificationRequest):
    """Verify an MC number with FMCSA and check against approved companies."""
    # Get carrier data from FMCSA
    carrier_data = fmcsa_service.verify_mc_number(request.mc_number)
    dba_name = carrier_data.get('dbaName') if carrier_data else None
    
    # Verify MC and get detailed result
    is_verified, message = verification_service.verify_mc(request.mc_number, dba_name)
    
    return MCVerificationResponse(
        mc_number=request.mc_number,
        verified=is_verified,
        message=message
    )

@app.get("/status/{mc_number}", response_model=MCVerificationResponse)
async def check_status(mc_number: str):
    """Check verification status for an MC number."""
    status = verification_service.get_verification_status(mc_number)
    if status is None:
        raise HTTPException(status_code=404, detail="MC Number not found")
    return MCVerificationResponse(
        mc_number=mc_number,
        verified=status,
        message="Previously verified" if status else "Previously rejected"
    )

@app.get("/verified_mcs")
async def list_verified_mcs():
    """List all verified MC numbers and their status."""
    return {"verified_mcs": verification_service.get_all_verified_mcs()}

@app.get("/loads/{reference_number}", response_model=LoadResponse)
async def get_load_by_path(reference_number: str = Path(..., description="Reference number for the load")):
    """Get load details by reference number using path parameter."""
    try:
        load_data = load_service.get_load_by_reference(reference_number)
        if not load_data:
            raise HTTPException(status_code=404, detail=f"Load with reference number {reference_number} not found")
        return LoadResponse(**load_data)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving load: {str(e)}")

@app.get("/loads", response_model=LoadResponse)
async def get_load_by_query(
    ref: str = Query(..., description="Reference number for the load"),
    call_id: Optional[str] = Query(None, description="Call ID from telephony platform"),
    call_type: Optional[str] = Query(None, description="Type of call (Inbound/Outbound)"),
    from_phone: Optional[str] = Query(None, description="Caller phone number"),
    to_phone: Optional[str] = Query(None, description="Recipient phone number")
):
    """Get load details by reference number using query parameter."""
    try:
        # Decode URL-encoded parameters
        if from_phone:
            from_phone = urllib.parse.unquote(from_phone)
        if to_phone:
            to_phone = urllib.parse.unquote(to_phone)
            
        load_data = load_service.get_load_by_reference(ref)
        if not load_data:
            return JSONResponse(
                status_code=404,
                content={"detail": f"Load with reference number {ref} not found"}
            )
            
        response_data = LoadResponse(**load_data)
        return JSONResponse(
            status_code=200,
            content={
                "reference_number": response_data.reference_number,
                "origin": response_data.origin,
                "destination": response_data.destination,
                "equipment_type": response_data.equipment_type,
                "rate": response_data.rate,
                "commodity": response_data.commodity
            }
        )
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"detail": f"Error retrieving load: {str(e)}"}
        )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000) 