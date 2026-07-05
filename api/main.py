"""FastAPI application for churn prediction service."""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from api.routers import analytics, health, predictions

app = FastAPI(
    title="Churn Prediction API",
    description="REST API for customer churn prediction and analytics",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Tighten in production
    allow_methods=["*"],
    allow_headers=["*"],
)

from fastapi.responses import RedirectResponse


@app.get("/", include_in_schema=False)
async def root():
    return RedirectResponse(url="/docs")


app.include_router(health.router, tags=["Health"])
app.include_router(predictions.router, prefix="/api/v1", tags=["Predictions"])
app.include_router(analytics.router, prefix="/api/v1", tags=["Analytics"])
