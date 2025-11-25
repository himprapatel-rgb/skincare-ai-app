"""User Model - SQLAlchemy ORM

Defines the User table schema with relationships to other models.
Includes authentication, profile, and audit fields.

Author: AI Engineering Team
Version: 1.0.0
"""

from datetime import datetime
from typing import List, Optional
from uuid import UUID, uuid4

from sqlalchemy import (
    Boolean, Column, DateTime, String, Integer, 
    Text, Enum, JSON, ForeignKey
)
from sqlalchemy.dialects.postgresql import UUID as PGUUID
from sqlalchemy.orm import relationship, Mapped, mapped_column
from sqlalchemy.sql import func

from app.core.database import Base
import enum


class GenderEnum(str, enum.Enum):
    """User gender options."""
    MALE = "male"
    FEMALE = "female"
    OTHER = "other"
    PREFER_NOT_TO_SAY = "prefer_not_to_say"


class UserRoleEnum(str, enum.Enum):
    """User role for access control."""
    USER = "user"
    PREMIUM = "premium"
    DERMATOLOGIST = "dermatologist"
    ADMIN = "admin"


class User(Base):
    """User account model."""
    
    __tablename__ = "users"
    
    # Primary Key
    id: Mapped[UUID] = mapped_column(
        PGUUID(as_uuid=True),
        primary_key=True,
        default=uuid4,
        index=True
    )
    
    # Authentication
    email: Mapped[str] = mapped_column(
        String(255),
        unique=True,
        index=True,
        nullable=False
    )
    hashed_password: Mapped[str] = mapped_column(String(255), nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    is_verified: Mapped[bool] = mapped_column(Boolean, default=False)
    is_superuser: Mapped[bool] = mapped_column(Boolean, default=False)
    
    # Role & Subscription
    role: Mapped[UserRoleEnum] = mapped_column(
        Enum(UserRoleEnum),
        default=UserRoleEnum.USER,
        nullable=False
    )
    subscription_expires_at: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True),
        nullable=True
    )
    
    # Personal Information
    first_name: Mapped[str] = mapped_column(String(100), nullable=False)
    last_name: Mapped[str] = mapped_column(String(100), nullable=False)
    date_of_birth: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True),
        nullable=True
    )
    gender: Mapped[Optional[GenderEnum]] = mapped_column(
        Enum(GenderEnum),
        nullable=True
    )
    phone: Mapped[Optional[str]] = mapped_column(String(20), nullable=True)
    
    # Profile Photo
    avatar_url: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    
    # OAuth Integration
    google_id: Mapped[Optional[str]] = mapped_column(
        String(255),
        unique=True,
        nullable=True,
        index=True
    )
    apple_id: Mapped[Optional[str]] = mapped_column(
        String(255),
        unique=True,
        nullable=True,
        index=True
    )
    
    # Preferences & Settings (JSON)
    preferences: Mapped[Optional[dict]] = mapped_column(
        JSON,
        nullable=True,
        default={}
    )
    
    # Audit Fields
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False
    )
    last_login_at: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True),
        nullable=True
    )
    deleted_at: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True),
        nullable=True  # Soft delete
    )
    
    # Relationships
    skin_profile: Mapped[Optional["SkinProfile"]] = relationship(
        "SkinProfile",
        back_populates="user",
        uselist=False,
        cascade="all, delete-orphan"
    )
    
    analyses: Mapped[List["SkinAnalysis"]] = relationship(
        "SkinAnalysis",
        back_populates="user",
        cascade="all, delete-orphan"
    )
    
    routines: Mapped[List["SkincareRoutine"]] = relationship(
        "SkincareRoutine",
        back_populates="user",
        cascade="all, delete-orphan"
    )
    
    progress_entries: Mapped[List["ProgressEntry"]] = relationship(
        "ProgressEntry",
        back_populates="user",
        cascade="all, delete-orphan"
    )
    
    notifications: Mapped[List["Notification"]] = relationship(
        "Notification",
        back_populates="user",
        cascade="all, delete-orphan"
    )
    
    def __repr__(self) -> str:
        return f"<User(id={self.id}, email={self.email}, role={self.role})>"
    
    @property
    def full_name(self) -> str:
        """Get user's full name."""
        return f"{self.first_name} {self.last_name}"
    
    @property
    def is_premium(self) -> bool:
        """Check if user has active premium subscription."""
        if not self.subscription_expires_at:
            return False
        return datetime.utcnow() < self.subscription_expires_at
    
    @property
    def age(self) -> Optional[int]:
        """Calculate user's age from date of birth."""
        if not self.date_of_birth:
            return None
        today = datetime.utcnow()
        return today.year - self.date_of_birth.year - (
            (today.month, today.day) < 
            (self.date_of_birth.month, self.date_of_birth.day)
        )
