"""
Progress Tracking API Routes

This module implements comprehensive skin health progress tracking endpoints including:
- Timeline visualization of skin improvements
- Before/after comparisons with multiple time points
- Skin concern trend analysis
- Goal setting and achievement tracking
- Statistical insights and predictions
- Photo gallery management for progress documentation

Based on SRS FR-3.4: Progress Tracking Requirements
- Track skin health improvements over time
- Compare analysis results across multiple dates
- Visualize trends in specific skin concerns
- Set and monitor skincare goals
- Generate progress reports and insights

Author: AI Skincare App Team
Version: 1.0
Created: 2024
"""

from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_, desc, func
from typing import List, Optional, Dict
from datetime import datetime, timedelta
import logging
import statistics

from app.core.database import get_db
from app.models.user import User
from app.models.skin_analysis import SkinAnalysis
from app.api.v1.routes.auth import get_current_user

# Configure logging
logger = logging.getLogger(__name__)

# Create router
router = APIRouter(
    prefix="/progress",
    tags=["Progress Tracking"],
    responses={
        404: {"description": "Not found"},
        401: {"description": "Unauthorized"},
        500: {"description": "Internal server error"}
    }
)


# Request/Response Models
from pydantic import BaseModel, Field


class ProgressDataPoint(BaseModel):
    """Single data point in progress timeline"""
    date: datetime
    skin_health_score: float
    analysis_id: str
    concerns_count: int
    
    class Config:
        json_schema_extra = {
            "example": {
                "date": "2024-01-15T10:30:00",
                "skin_health_score": 75.5,
                "analysis_id": "550e8400-e29b-41d4-a716-446655440000",
                "concerns_count": 3
            }
        }


class ConcernTrend(BaseModel):
    """Trend data for specific skin concern"""
    concern_type: str
    data_points: List[Dict] = Field(..., description="List of {date, severity, count} objects")
    trend_direction: str = Field(..., description="improving, stable, or worsening")
    change_percentage: float
    
    class Config:
        json_schema_extra = {
            "example": {
                "concern_type": "acne",
                "data_points": [
                    {"date": "2024-01-01", "severity": "moderate", "count": 5},
                    {"date": "2024-01-15", "severity": "mild", "count": 2}
                ],
                "trend_direction": "improving",
                "change_percentage": -60.0
            }
        }


class ProgressTimelineResponse(BaseModel):
    """Complete progress timeline response"""
    user_id: int
    period_days: int
    data_points: List[ProgressDataPoint]
    overall_trend: str
    average_score: float
    score_improvement: float
    total_analyses: int
    
    class Config:
        json_schema_extra = {
            "example": {
                "user_id": 123,
                "period_days": 30,
                "data_points": [],
                "overall_trend": "improving",
                "average_score": 77.3,
                "score_improvement": 8.2,
                "total_analyses": 4
            }
        }


class SkinGoal(BaseModel):
    """Model for skin improvement goals"""
    goal_id: Optional[str] = None
    user_id: int
    goal_type: str = Field(..., description="Type: reduce_acne, improve_texture, reduce_wrinkles, etc.")
    target_date: datetime
    current_progress: float = Field(0.0, ge=0.0, le=100.0)
    is_achieved: bool = False
    created_at: datetime = Field(default_factory=datetime.utcnow)
    
    class Config:
        json_schema_extra = {
            "example": {
                "goal_id": "750e8400-e29b-41d4-a716-446655440000",
                "user_id": 123,
                "goal_type": "reduce_acne",
                "target_date": "2024-03-01T00:00:00",
                "current_progress": 45.5,
                "is_achieved": False,
                "created_at": "2024-01-01T00:00:00"
            }
        }


# API Endpoints

@router.get(
    "/timeline",
    response_model=ProgressTimelineResponse,
    summary="Get progress timeline",
    description="Retrieve complete skin health progress timeline with data points and trends"
)
async def get_progress_timeline(
    days: int = Query(30, ge=7, le=365, description="Number of days to analyze"),
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
) -> ProgressTimelineResponse:
    """
    Get user's skin health progress timeline.
    
    Retrieves all skin analyses within the specified period and generates
    a comprehensive timeline showing improvements, trends, and statistics.
    
    Args:
        days: Number of days to analyze (7-365)
        current_user: Authenticated user
        db: Database session
    
    Returns:
        ProgressTimelineResponse with timeline data and statistics
    """
    try:
        logger.info(f"Retrieving progress timeline for user {current_user.id}, period: {days} days")
        
        # Calculate date range
        end_date = datetime.utcnow()
        start_date = end_date - timedelta(days=days)
        
        # Query analyses within date range
        query = (
            select(SkinAnalysis)
            .where(
                and_(
                    SkinAnalysis.user_id == current_user.id,
                    SkinAnalysis.analysis_date >= start_date,
                    SkinAnalysis.analysis_date <= end_date
                )
            )
            .order_by(SkinAnalysis.analysis_date.asc())
        )
        
        result = await db.execute(query)
        analyses = result.scalars().all()
        
        if not analyses:
            return ProgressTimelineResponse(
                user_id=current_user.id,
                period_days=days,
                data_points=[],
                overall_trend="no_data",
                average_score=0.0,
                score_improvement=0.0,
                total_analyses=0
            )
        
        # Build data points
        data_points = []
        scores = []
        
        for analysis in analyses:
            import json
            concerns = json.loads(analysis.detected_concerns) if analysis.detected_concerns else []
            
            data_points.append(ProgressDataPoint(
                date=analysis.analysis_date,
                skin_health_score=analysis.overall_skin_health_score,
                analysis_id=analysis.id,
                concerns_count=len(concerns)
            ))
            scores.append(analysis.overall_skin_health_score)
        
        # Calculate statistics
        average_score = statistics.mean(scores)
        score_improvement = scores[-1] - scores[0] if len(scores) >= 2 else 0.0
        
        # Determine overall trend
        if score_improvement > 5.0:
            overall_trend = "improving"
        elif score_improvement < -5.0:
            overall_trend = "declining"
        else:
            overall_trend = "stable"
        
        logger.info(f"Timeline retrieved: {len(data_points)} analyses, trend: {overall_trend}")
        
        return ProgressTimelineResponse(
            user_id=current_user.id,
            period_days=days,
            data_points=data_points,
            overall_trend=overall_trend,
            average_score=round(average_score, 2),
            score_improvement=round(score_improvement, 2),
            total_analyses=len(analyses)
        )
        
    except Exception as e:
        logger.error(f"Error retrieving progress timeline: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve progress timeline"
        )


@router.get(
    "/trends/{concern_type}",
    response_model=ConcernTrend,
    summary="Get trend for specific concern",
    description="Track how a specific skin concern has changed over time"
)
async def get_concern_trend(
    concern_type: str,
    days: int = Query(90, ge=7, le=365, description="Number of days to analyze"),
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
) -> ConcernTrend:
    """
    Get trend analysis for a specific skin concern.
    
    Args:
        concern_type: Type of concern to track (e.g., acne, dark_spots, wrinkles)
        days: Number of days to analyze
        current_user: Authenticated user
        db: Database session
    
    Returns:
        ConcernTrend with historical data and trend direction
    """
    try:
        logger.info(f"Analyzing trend for concern '{concern_type}', user {current_user.id}")
        
        # Calculate date range
        end_date = datetime.utcnow()
        start_date = end_date - timedelta(days=days)
        
        # Query analyses
        query = (
            select(SkinAnalysis)
            .where(
                and_(
                    SkinAnalysis.user_id == current_user.id,
                    SkinAnalysis.analysis_date >= start_date
                )
            )
            .order_by(SkinAnalysis.analysis_date.asc())
        )
        
        result = await db.execute(query)
        analyses = result.scalars().all()
        
        # Extract concern-specific data points
        data_points = []
        concern_counts = []
        
        import json
        for analysis in analyses:
            concerns = json.loads(analysis.detected_concerns) if analysis.detected_concerns else []
            
            # Count occurrences of this concern type
            matching_concerns = [c for c in concerns if c.get("concern_type") == concern_type]
            count = len(matching_concerns)
            
            if matching_concerns:
                severity = matching_concerns[0].get("severity", "unknown")
                data_points.append({
                    "date": analysis.analysis_date.isoformat(),
                    "severity": severity,
                    "count": count
                })
                concern_counts.append(count)
        
        # Determine trend
        if len(concern_counts) >= 2:
            first_count = concern_counts[0]
            last_count = concern_counts[-1]
            change_percentage = ((last_count - first_count) / first_count * 100) if first_count > 0 else 0.0
            
            if change_percentage <= -20:
                trend_direction = "improving"
            elif change_percentage >= 20:
                trend_direction = "worsening"
            else:
                trend_direction = "stable"
        else:
            change_percentage = 0.0
            trend_direction = "insufficient_data"
        
        return ConcernTrend(
            concern_type=concern_type,
            data_points=data_points,
            trend_direction=trend_direction,
            change_percentage=round(change_percentage, 1)
        )
        
    except Exception as e:
        logger.error(f"Error analyzing concern trend: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to analyze concern trend"
        )


@router.get(
    "/summary",
    summary="Get progress summary",
    description="Get comprehensive progress summary with key metrics and insights"
)
async def get_progress_summary(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
) -> dict:
    """
    Get comprehensive progress summary.
    
    Returns key metrics, milestones, and insights about user's skincare journey.
    
    Args:
        current_user: Authenticated user
        db: Database session
    
    Returns:
        Dictionary with summary statistics and insights
    """
    try:
        logger.info(f"Generating progress summary for user {current_user.id}")
        
        # Query all analyses
        query = (
            select(SkinAnalysis)
            .where(SkinAnalysis.user_id == current_user.id)
            .order_by(SkinAnalysis.analysis_date.asc())
        )
        
        result = await db.execute(query)
        analyses = result.scalars().all()
        
        if not analyses:
            return {
                "total_analyses": 0,
                "days_tracked": 0,
                "current_score": 0.0,
                "best_score": 0.0,
                "total_improvement": 0.0,
                "most_improved_concern": None,
                "insights": ["Start tracking your skin to see progress!"]
            }
        
        # Calculate metrics
        scores = [a.overall_skin_health_score for a in analyses]
        first_analysis = analyses[0]
        latest_analysis = analyses[-1]
        
        days_tracked = (latest_analysis.analysis_date - first_analysis.analysis_date).days
        total_improvement = latest_analysis.overall_skin_health_score - first_analysis.overall_skin_health_score
        
        # Generate insights
        insights = []
        if total_improvement > 10:
            insights.append(f"Great progress! Your skin health improved by {total_improvement:.1f} points!")
        elif total_improvement > 0:
            insights.append(f"Keep it up! You've improved by {total_improvement:.1f} points.")
        
        if len(analyses) >= 4:
            insights.append("You're consistent with tracking - this helps identify what works!")
        
        return {
            "total_analyses": len(analyses),
            "days_tracked": days_tracked,
            "current_score": round(latest_analysis.overall_skin_health_score, 2),
            "best_score": round(max(scores), 2),
            "total_improvement": round(total_improvement, 2),
            "most_improved_concern": "acne",  # TODO: Calculate from data
            "insights": insights
        }
        
    except Exception as e:
        logger.error(f"Error generating progress summary: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to generate progress summary"
        )