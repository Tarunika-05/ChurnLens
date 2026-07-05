"""Health check endpoints."""
from fastapi import APIRouter

from api.dependencies import get_model
from api.schemas import HealthResponse
from src.exceptions import ModelLoadError

router = APIRouter()

@router.get("/health", response_model=HealthResponse)
async def health_check() -> HealthResponse:
    model_loaded = False
    try:
        get_model()
        model_loaded = True
        status = "healthy"
    except ModelLoadError:
        status = "degraded (model not loaded)"

    return HealthResponse(
        status=status,
        model_loaded=model_loaded,
        version="1.0.0"
    )
