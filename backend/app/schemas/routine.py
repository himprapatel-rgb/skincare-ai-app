"""Pydantic schemas for skincare routine management."""

from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, Field


class RoutineStep(BaseModel):
    """Individual step in a skincare routine."""
    name: str = Field(..., min_length=1, max_length=200)
    description: str = Field(..., max_length=500)
    duration_minutes: int = Field(default=5, ge=1, le=60)
    product_type: str  # cleanser, toner, serum, moisturizer, sunscreen, mask
    frequency: str = Field(
        default="daily",
        description="Frequency: daily, morning_only, evening_only, 2x_week, 3x_week"
    )


class RoutineCreate(BaseModel):
    """Schema for creating a new routine."""
    name: str = Field(..., min_length=1, max_length=100)
    description: Optional[str] = Field(None, max_length=500)
    routine_type: str  # morning, evening, weekly_treatment
    is_active: bool = True
    steps: List[RoutineStep]


class RoutineUpdate(BaseModel):
    """Schema for updating a routine."""
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    description: Optional[str] = Field(None, max_length=500)
    is_active: Optional[bool] = None
    steps: Optional[List[RoutineStep]] = None


class RoutineResponse(BaseModel):
    """Routine response schema."""
    id: int
    user_id: int
    name: str
    description: Optional[str]
    routine_type: str
    is_active: bool
    steps: List[RoutineStep]
    adherence_rate: float = Field(default=0.0, ge=0, le=100)
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class RoutineListResponse(BaseModel):
    """Paginated list of routines."""
    total: int
    page: int
    page_size: int
    items: List[RoutineResponse]