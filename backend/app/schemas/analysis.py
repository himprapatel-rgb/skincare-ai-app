"""Pydantic schemas for skin analysis data validation."""

from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, Field


class AnalysisCreate(BaseModel):
    """Schema for creating a new skin analysis."""
    image_url: str = Field(..., description="URL of skin image")
    concerns: Optional[List[str]] = Field(
        None, description="List of skin concerns: acne, dryness, oiliness, sensitivity, wrinkles"
    )
    notes: Optional[str] = Field(None, max_length=500)


class SkinConcernDetail(BaseModel):
    """Details of a detected skin concern."""
    concern_type: str
    severity: float = Field(..., ge=0, le=1, description="Severity score 0-1")
    description: str
    recommendations: List[str]


class AnalysisResponse(BaseModel):
    """Skin analysis response schema."""
    id: int
    user_id: int
    image_url: str
    skin_type_detected: str
    overall_score: float = Field(..., ge=0, le=100, description="Overall skin health score")
    concerns: List[SkinConcernDetail]
    recommendations: List[str]
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class AnalysisListResponse(BaseModel):
    """Paginated list of analyses."""
    total: int
    page: int
    page_size: int
    items: List[AnalysisResponse]