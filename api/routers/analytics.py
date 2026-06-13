"""Analytics summary endpoints."""
from fastapi import APIRouter, HTTPException
import json
from src.config import REPORTS_DIR

router = APIRouter()

@router.get("/analytics/summary")
async def get_summary() -> dict:
    summary_path = REPORTS_DIR / "business_summary.json"
    if not summary_path.exists():
        raise HTTPException(status_code=404, detail="Business summary not found. Pipeline may not have been run.")
        
    try:
        with open(summary_path, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error loading summary: {str(e)}")
