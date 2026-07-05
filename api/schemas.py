"""Pydantic request/response models."""
from enum import Enum

from pydantic import BaseModel, Field


class ContractType(str, Enum):
    MONTH_TO_MONTH = "Month-to-month"
    ONE_YEAR = "One year"
    TWO_YEAR = "Two year"

class InternetServiceType(str, Enum):
    DSL = "DSL"
    FIBER = "Fiber optic"
    NO = "No"

class PaymentMethodType(str, Enum):
    E_CHECK = "Electronic check"
    MAILED_CHECK = "Mailed check"
    BANK_TRANSFER = "Bank transfer (automatic)"
    CREDIT_CARD = "Credit card (automatic)"

class PredictionRequest(BaseModel):
    customerID: str = Field(default="NEW")
    gender: str = Field(..., pattern="^(Male|Female)$")
    SeniorCitizen: int = Field(..., ge=0, le=1)
    Partner: str = Field(..., pattern="^(Yes|No)$")
    Dependents: str = Field(..., pattern="^(Yes|No)$")
    tenure: int = Field(..., ge=0, le=100)
    PhoneService: str = Field(..., pattern="^(Yes|No)$")
    MultipleLines: str = Field(..., pattern="^(Yes|No|No phone service)$")
    InternetService: InternetServiceType
    OnlineSecurity: str = Field(..., pattern="^(Yes|No|No internet service)$")
    OnlineBackup: str = Field(..., pattern="^(Yes|No|No internet service)$")
    DeviceProtection: str = Field(..., pattern="^(Yes|No|No internet service)$")
    TechSupport: str = Field(..., pattern="^(Yes|No|No internet service)$")
    StreamingTV: str = Field(..., pattern="^(Yes|No|No internet service)$")
    StreamingMovies: str = Field(..., pattern="^(Yes|No|No internet service)$")
    Contract: ContractType
    PaperlessBilling: str = Field(..., pattern="^(Yes|No)$")
    PaymentMethod: PaymentMethodType
    MonthlyCharges: float = Field(..., gt=0, le=500)
    TotalCharges: float = Field(..., ge=0)

class PredictionResponse(BaseModel):
    customer_id: str
    churn_probability: float
    risk_tier: str
    predicted_churn: int
    top_drivers: list[str] | None = None

class HealthResponse(BaseModel):
    status: str
    model_loaded: bool
    version: str
