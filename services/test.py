from fastapi import APIRouter
from typing import Dict

router = APIRouter()

@router.get("/test")
async def test_endpoint() -> Dict[str, str]:
    """Simple test endpoint that returns a greeting."""
    return {
        "status": "success",
        "message": "Hello from the test endpoint!",
        "version": "1.0.0"
    }
