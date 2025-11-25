"""
Skincare Routine Database Model

This module defines the SkincareRoutine and RoutineAdherence database models for
storing user skincare routines and tracking adherence.

Based on SRS FR-3.3: Personalized Routine Builder Requirements
- Store customized AM/PM routines
- Track product steps in correct order
- Enable routine modification and updates
- Log adherence and completion history

Author: AI Skincare App Team
Version: 1.0
Created: 2024
"""

from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Boolean, Text, Index
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()


class SkincareRoutine(Base):
    """
    Model for skincare routines.
    
    Stores user-created or AI-generated skincare routines with product steps.
    Supports morning/evening routines with customizable product orders.
    """
    __tablename__ = "skincare_routines"
    
    # Primary Key
    id = Column(String(36), primary_key=True, index=True)
    
    # Foreign Keys
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    based_on_analysis_id = Column(String(36), ForeignKey("skin_analyses.id"), nullable=True)
    
    # Routine Details
    routine_name = Column(String(100), nullable=False)
    routine_time = Column(String(20), nullable=False)  # "morning", "evening", "both"
    steps_json = Column(Text, nullable=False)  # JSON array of product steps
    is_active = Column(Boolean, default=True, nullable=False)
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    # Relationships
    # user = relationship("User", back_populates="routines")
    # analysis = relationship("SkinAnalysis", back_populates="routines")
    adherence_logs = relationship(
        "RoutineAdherence",
        back_populates="routine",
        cascade="all, delete-orphan"
    )
    
    # Indexes for efficient querying
    __table_args__ = (
        Index('idx_user_routine_time', 'user_id', 'routine_time'),
        Index('idx_user_active', 'user_id', 'is_active'),
        Index('idx_analysis', 'based_on_analysis_id'),
    )
    
    def __repr__(self) -> str:
        return f"<SkincareRoutine(id={self.id}, name='{self.routine_name}', time='{self.routine_time}', user_id={self.user_id})>"


class RoutineAdherence(Base):
    """
    Model for tracking routine adherence and completion.
    
    Logs when users complete their routines to track adherence over time
    and identify patterns in skincare habits.
    """
    __tablename__ = "routine_adherence"
    
    # Primary Key
    id = Column(String(36), primary_key=True, index=True)
    
    # Foreign Keys
    routine_id = Column(String(36), ForeignKey("skincare_routines.id"), nullable=False, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    
    # Adherence Details
    completed_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    steps_completed_json = Column(Text, nullable=False)  # JSON array of completed step orders
    completion_percentage = Column(Integer, nullable=False, default=100)  # 0-100
    notes = Column(Text, nullable=True)
    
    # Relationships
    routine = relationship("SkincareRoutine", back_populates="adherence_logs")
    # user = relationship("User", back_populates="adherence_logs")
    
    # Indexes for efficient querying
    __table_args__ = (
        Index('idx_routine_completed', 'routine_id', 'completed_at'),
        Index('idx_user_completed', 'user_id', 'completed_at'),
    )
    
    def __repr__(self) -> str:
        return f"<RoutineAdherence(id={self.id}, routine_id={self.routine_id}, completed_at={self.completed_at}, completion={self.completion_percentage}%)>"


class ProductRecommendation(Base):
    """
    Model for AI-generated product recommendations.
    
    Stores personalized product recommendations based on skin analysis
    and user preferences.
    """
    __tablename__ = "product_recommendations"
    
    # Primary Key
    id = Column(String(36), primary_key=True, index=True)
    
    # Foreign Keys
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    based_on_analysis_id = Column(String(36), ForeignKey("skin_analyses.id"), nullable=True)
    
    # Recommendation Details
    product_name = Column(String(200), nullable=False)
    product_category = Column(String(50), nullable=False)  # cleanser, serum, moisturizer, etc.
    brand_name = Column(String(100), nullable=True)
    recommended_for_concerns = Column(Text, nullable=False)  # JSON array of concerns
    confidence_score = Column(Integer, nullable=False)  # 0-100
    usage_instructions = Column(Text, nullable=True)
    price_range = Column(String(20), nullable=True)  # "budget", "mid-range", "luxury"
    
    # Recommendation Metadata
    recommendation_reason = Column(Text, nullable=True)
    ai_model_version = Column(String(20), nullable=True)
    
    # User Feedback
    user_rating = Column(Integer, nullable=True)  # 1-5 stars
    is_purchased = Column(Boolean, default=False)
    is_favorite = Column(Boolean, default=False)
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    # Relationships
    # user = relationship("User", back_populates="recommendations")
    # analysis = relationship("SkinAnalysis", back_populates="recommendations")
    
    # Indexes
    __table_args__ = (
        Index('idx_user_category', 'user_id', 'product_category'),
        Index('idx_user_favorite', 'user_id', 'is_favorite'),
        Index('idx_analysis', 'based_on_analysis_id'),
    )
    
    def __repr__(self) -> str:
        return f"<ProductRecommendation(id={self.id}, product='{self.product_name}', category='{self.product_category}', confidence={self.confidence_score})>"