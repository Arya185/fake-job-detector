from datetime import datetime
from pydantic import BaseModel, Field

class JobPosting(BaseModel):
    text: str = Field(
        ...,
        min_length=20,
        max_length=10000,
        description="Full job description"
    )

class PredictionResponse(BaseModel):
    prediction: str
    confidence: str
    fraud_probability: float

    risk_score: int
    matched_rules: list[str]
    matched_keywords: list[str]

class HistoryItem(BaseModel):
    prediction: str
    fraud_probability: float
    created_at: datetime

class HistoryResponse(BaseModel):
    history: list[HistoryItem]
    message: str | None = None
    error: str | None = None
