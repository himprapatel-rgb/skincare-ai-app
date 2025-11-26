"""Pydantic schemas for user-related data validation."""

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, EmailStr, Field


class UserBase(BaseModel):
    """Base user schema with common fields."""
    email: EmailStr
    first_name: str = Field(..., min_length=1, max_length=100)
    last_name: str = Field(..., min_length=1, max_length=100)
    age: Optional[int] = Field(None, ge=13, le=120)
    skin_type: Optional[str] = Field(
        None,
        description="Skin type: oily, dry, combination, sensitive, normal"
    )


class UserRegister(UserBase):
    """User registration schema with password."""
    password: str = Field(..., min_length=8, max_length=128)
    password_confirm: str = Field(..., min_length=8, max_length=128)

    class Config:
        json_schema_extra = {
            "example": {
                "email": "user@example.com",
                "first_name": "John",
                "last_name": "Doe",
                "password": "SecurePass123!",
                "password_confirm": "SecurePass123!",
            }
        }


class UserLogin(BaseModel):
    """User login schema."""
    email: EmailStr
    password: str = Field(..., min_length=8, max_length=128)

    class Config:
        json_schema_extra = {
            "example": {
                "email": "user@example.com",
                "password": "SecurePass123!",
            }
        }


class UserUpdate(BaseModel):
    """User update schema."""
    first_name: Optional[str] = Field(None, min_length=1, max_length=100)
    last_name: Optional[str] = Field(None, min_length=1, max_length=100)
    age: Optional[int] = Field(None, ge=13, le=120)
    skin_type: Optional[str] = None


class UserResponse(UserBase):
    """User response schema (no password)."""
    id: int
    is_active: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class UserDetailResponse(UserResponse):
    """Detailed user response with additional fields."""
    analysis_count: int = 0
    routine_count: int = 0
    last_analysis: Optional[datetime] = None