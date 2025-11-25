"""Skin Analysis Model - SQLAlchemy ORM

Stores AI-powered skin analysis results including detected concerns,
severity scores, and ML model predictions.

Author: AI Engineering Team
Version: 1.0.0
"""

from datetime import datetime
from typing import List, Optional, Dict
from uuid import UUID, uuid4
import enum

from sqlalchemy import (
    Column, DateTime, String, Integer, Float,
    Text, Enum, JSON, ForeignKey, Boolean
)
from sqlalchemy.dialects.postgresql import UUID as PGUUID, ARRAY
from sqlalchemy.orm import relationship, Mapped, mapped_column
from sqlalchemy.sql import func

from app.core.database import Base


class AnalysisStatusEnum(str, enum.Enum):
    """Analysis processing status."""
    PENDING = "pending"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"


class SeverityEnum(str, enum.Enum):
    """Skin concern severity levels."""
    NONE = "none"
    MILD = "mild"
    MODERATE = "moderate"
    SEVERE = "severe"
    VERY_SEVERE = "very_severe"


class ImageAngleEnum(str, enum.Enum):
    """Captured image angle."""
    FRONT = "front"
    LEFT = "left"
    RIGHT = "right"


class SkinAnalysis(Base):
    """Skin analysis results from ML models."""
    
    __tablename__ = "skin_analyses"
    
    # Primary Key
    id: Mapped[UUID] = mapped_column(
        PGUUID(as_uuid=True),
        primary_key=True,
        default=uuid4,
        index=True
    )
    
    # Foreign Keys
    user_id: Mapped[UUID] = mapped_column(
        PGUUID(as_uuid=True),
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True
    )
    
    # Image Information
    image_url: Mapped[str] = mapped_column(Text, nullable=False)
    image_angle: Mapped[ImageAngleEnum] = mapped_column(
        Enum(ImageAngleEnum),
        default=ImageAngleEnum.FRONT,
        nullable=False
    )
    image_width: Mapped[int] = mapped_column(Integer, nullable=False)
    image_height: Mapped[int] = mapped_column(Integer, nullable=False)
    lighting_score: Mapped[float] = mapped_column(Float, nullable=True)  # 0-1
    
    # Analysis Status
    status: Mapped[AnalysisStatusEnum] = mapped_column(
        Enum(AnalysisStatusEnum),
        default=AnalysisStatusEnum.PENDING,
        nullable=False,
        index=True
    )
    
    # Overall Scores
    overall_score: Mapped[Optional[float]] = mapped_column(
        Float,
        nullable=True  # 0-100
    )
    
    # Detected Concerns (JSON array)
    detected_concerns: Mapped[Optional[dict]] = mapped_column(
        JSON,
        nullable=True,
        default=list,
        comment="Array of detected skin concerns with details"
    )
    
    # Skin Metrics (JSON object)
    skin_metrics: Mapped[Optional[dict]] = mapped_column(
        JSON,
        nullable=True,
        default=dict,
        comment="Hydration, oiliness, texture, etc."
    )
    
    # Acne Detection Results
    acne_severity: Mapped[Optional[SeverityEnum]] = mapped_column(
        Enum(SeverityEnum),
        nullable=True
    )
    acne_lesion_count: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    acne_confidence: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    acne_affected_areas: Mapped[Optional[List[str]]] = mapped_column(
        ARRAY(String),
        nullable=True
    )
    
    # Wrinkle Detection Results
    wrinkle_severity: Mapped[Optional[SeverityEnum]] = mapped_column(
        Enum(SeverityEnum),
        nullable=True
    )
    wrinkle_depth_score: Mapped[Optional[float]] = mapped_column(
        Float,
        nullable=True
    )
    wrinkle_confidence: Mapped[Optional[float]] = mapped_column(
        Float,
        nullable=True
    )
    wrinkle_affected_areas: Mapped[Optional[List[str]]] = mapped_column(
        ARRAY(String),
        nullable=True
    )
    
    # Pigmentation Detection Results
    pigmentation_severity: Mapped[Optional[SeverityEnum]] = mapped_column(
        Enum(SeverityEnum),
        nullable=True
    )
    pigmentation_uniformity: Mapped[Optional[float]] = mapped_column(
        Float,
        nullable=True
    )
    pigmentation_confidence: Mapped[Optional[float]] = mapped_column(
        Float,
        nullable=True
    )
    
    # Dark Circles Detection
    dark_circles_severity: Mapped[Optional[SeverityEnum]] = mapped_column(
        Enum(SeverityEnum),
        nullable=True
    )
    dark_circles_confidence: Mapped[Optional[float]] = mapped_column(
        Float,
        nullable=True
    )
    
    # Pore Visibility
    pore_visibility_score: Mapped[Optional[float]] = mapped_column(
        Float,
        nullable=True
    )
    
    # Skin Type Classification
    detected_skin_type: Mapped[Optional[str]] = mapped_column(
        String(50),
        nullable=True
    )
    skin_type_confidence: Mapped[Optional[float]] = mapped_column(
        Float,
        nullable=True
    )
    
    # ML Model Metadata
    model_versions: Mapped[Optional[dict]] = mapped_column(
        JSON,
        nullable=True,
        comment="Versions of ML models used"
    )
    processing_time_ms: Mapped[Optional[int]] = mapped_column(
        Integer,
        nullable=True
    )
    
    # Recommendations
    recommendations: Mapped[Optional[List[str]]] = mapped_column(
        ARRAY(String),
        nullable=True
    )
    
    # Error Handling
    error_message: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    
    # Audit Fields
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
        index=True
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False
    )
    
    # Relationships
    user: Mapped["User"] = relationship(
        "User",
        back_populates="analyses"
    )
    
    progress_entries: Mapped[List["ProgressEntry"]] = relationship(
        "ProgressEntry",
        back_populates="analysis",
        foreign_keys="ProgressEntry.analysis_id"
    )
    
    def __repr__(self) -> str:
        return (
            f"<SkinAnalysis(id={self.id}, user_id={self.user_id}, "
            f"status={self.status}, score={self.overall_score})>"
        )
    
    @property
    def has_concerns(self) -> bool:
        """Check if analysis detected any skin concerns."""
        if not self.detected_concerns:
            return False
        return len(self.detected_concerns) > 0
    
    @property
    def primary_concern(self) -> Optional[Dict]:
        """Get the most severe detected concern."""
        if not self.detected_concerns or len(self.detected_concerns) == 0:
            return None
        
        # Sort by severity and confidence
        severity_order = {
            "very_severe": 4,
            "severe": 3,
            "moderate": 2,
            "mild": 1,
            "none": 0
        }
        
        sorted_concerns = sorted(
            self.detected_concerns,
            key=lambda x: (
                severity_order.get(x.get("severity", "none"), 0),
                x.get("confidence", 0)
            ),
            reverse=True
        )
        
        return sorted_concerns[0] if sorted_concerns else None
    
    def to_dict(self) -> dict:
        """Convert analysis to dictionary for API responses."""
        return {
            "analysis_id": str(self.id),
            "status": self.status.value,
            "overall_score": self.overall_score,
            "detected_concerns": self.detected_concerns or [],
            "skin_metrics": self.skin_metrics or {},
            "recommendations": self.recommendations or [],
            "image_angle": self.image_angle.value,
            "processing_time_ms": self.processing_time_ms,
            "created_at": self.created_at.isoformat() if self.created_at else None
        }
