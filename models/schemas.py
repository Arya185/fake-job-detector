from datetime import datetime
from pydantic import BaseModel, Field, field_validator
from typing import Optional

class JobPosting(BaseModel):
    text: str = Field(
        default=...,
        min_length=20,
        max_length=10000,
        description="Full job description"
    )
    
    @field_validator('text')
    @classmethod
    def validate_text(cls, v: str) -> str:
        if not v or not v.strip():
            raise ValueError('Job description cannot be empty')
        return v.strip()

class PredictionResponse(BaseModel):
    prediction: str = Field(..., description="Prediction result")
    confidence: str = Field(..., description="Confidence level")
    fraud_probability: float = Field(
        ...,
        ge=0.0,
        le=1.0,
        description="Probability of fraud between 0 and 1"
    )

class HistoryItem(BaseModel):
    prediction: str = Field(..., description="Prediction result")
    fraud_probability: float = Field(
        ...,
        ge=0.0,
        le=1.0,
        description="Probability of fraud between 0 and 1"
    )
    created_at: datetime = Field(
        default_factory=datetime.now,
        description="Timestamp when the prediction was created"
    )
    
    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }

class HistoryResponse(BaseModel):
    history: list[HistoryItem] = Field(
        default_factory=list,
        description="List of historical predictions"
    )
    message: Optional[str] = Field(
        default=None,
        description="Success message"
    )
    error: Optional[str] = Field(
        default=None,
        description="Error message if any"
    )
    
    class Config:
        json_schema_extra = {
            "example": {
                "history": [
                    {
                        "prediction": "Legitimate",
                        "fraud_probability": 0.05,
                        "created_at": "2024-01-01T12:00:00"
                    }
                ],
                "message": "History retrieved successfully",
                "error": None
            }
        }
