"""
Skin Analysis API Routes

This module implements comprehensive skin analysis endpoints including:
- Image upload and preprocessing
- Real-time skin analysis with AI/ML models
- Analysis history and results retrieval
- Confidence scoring and recommendations
- Support for multiple analysis types (acne, wrinkles, dark spots, etc.)

Based on SRS FR-3.2: AI Skin Analysis Requirements
- Upload/capture facial images
- Detect skin concerns (acne, wrinkles, dark spots, etc.)
- Provide confidence scores for each detection  
- Generate personalized product recommendations
- Track analysis history over time

Author: AI Skincare App Team
Version: 1.0
Created: 2024
"""

from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, status, BackgroundTasks
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_, desc
from typing import List, Optional
from datetime import datetime, timedelta
import logging
import uuid
import json

from app.core.database import get_db
from app.models.user import User
from app.models.skin_analysis import SkinAnalysis, AnalysisType, SkinConcernSeverity
from app.api.v1.routes.auth import get_current_user

# Configure logging
logger = logging.getLogger(__name__)

# Create router
router = APIRouter(
    prefix="/analysis",
    tags=["Skin Analysis"],
    responses={
        404: {"description": "Not found"},
        401: {"description": "Unauthorized"},
        500: {"description": "Internal server error"}
    }
)


# Request/Response Models
from pydantic import BaseModel, Field, validator


class SkinConcernDetection(BaseModel):
    """Model for individual skin concern detection"""
    concern_type: str = Field(..., description="Type of skin concern detected")
    severity: str = Field(..., description="Severity level: mild, moderate, severe")
    confidence: float = Field(..., ge=0.0, le=1.0, description="Detection confidence score")
    location: Optional[dict] = Field(None, description="Bounding box coordinates if applicable")
    
    class Config:
        json_schema_extra = {
            "example": {
                "concern_type": "acne",
                "severity": "moderate",
                "confidence": 0.87,
                "location": {"x": 120, "y": 150, "width": 30, "height": 30}
            }
        }


class AnalysisRequest(BaseModel):
    """Request model for initiating skin analysis"""
    analysis_type: str = Field(..., description="Type of analysis: full, acne, aging, pigmentation")
    image_quality_check: bool = Field(True, description="Whether to verify image quality before analysis")
    generate_recommendations: bool = Field(True, description="Whether to generate product recommendations")
    
    @validator('analysis_type')
    def validate_analysis_type(cls, v):
        valid_types = ['full', 'acne', 'aging', 'pigmentation', 'texture']
        if v not in valid_types:
            raise ValueError(f"Analysis type must be one of: {valid_types}")
        return v
    
    class Config:
        json_schema_extra = {
            "example": {
                "analysis_type": "full",
                "image_quality_check": True,
                "generate_recommendations": True
            }
        }


class AnalysisResponse(BaseModel):
    """Response model for analysis results"""
    analysis_id: str = Field(..., description="Unique analysis identifier")
    user_id: int
    analysis_type: str
    detections: List[SkinConcernDetection] = Field(..., description="List of detected skin concerns")
    overall_skin_health_score: float = Field(..., ge=0.0, le=100.0, description="Overall skin health score")
    recommendations: Optional[List[str]] = Field(None, description="Product/routine recommendations")
    analysis_date: datetime
    image_url: Optional[str] = Field(None, description="URL to analyzed image")
    
    class Config:
        json_schema_extra = {
            "example": {
                "analysis_id": "550e8400-e29b-41d4-a716-446655440000",
                "user_id": 123,
                "analysis_type": "full",
                "detections": [
                    {"concern_type": "acne", "severity": "moderate", "confidence": 0.87}
                ],
                "overall_skin_health_score": 75.5,
                "recommendations": ["Use salicylic acid cleanser", "Apply SPF 50 daily"],
                "analysis_date": "2024-01-15T10:30:00",
                "image_url": "/storage/analyses/550e8400.jpg"
            }
        }


class AnalysisHistoryResponse(BaseModel):
    """Response model for analysis history"""
    total_count: int
    analyses: List[AnalysisResponse]
    
    class Config:
        json_schema_extra = {
            "example": {
                "total_count": 5,
                "analyses": []
            }
        }


# Helper Functions
async def process_image_analysis(
    image_data: bytes,
    analysis_type: str,
    user_id: int
) -> dict:
    """
    Process uploaded image and perform AI analysis.
    
    Args:
        image_data: Raw image bytes
        analysis_type: Type of analysis to perform
        user_id: ID of the user requesting analysis
    
    Returns:
        Dictionary containing analysis results
    
    Note:
        This is a placeholder that will integrate with actual ML models.
        In production, this would call PyTorch/TFLite models for inference.
    """
    try:
        # TODO: Integrate with actual ML models (PyTorch/TFLite)
        # For now, returning mock data structure
        
        detections = []
        
        if analysis_type in ['full', 'acne']:
            detections.append({
                "concern_type": "acne",
                "severity": "moderate",
                "confidence": 0.85,
                "location": {"x": 120, "y": 150, "width": 30, "height": 30}
            })
        
        if analysis_type in ['full', 'aging']:
            detections.append({
                "concern_type": "fine_lines",
                "severity": "mild",
                "confidence": 0.72,
                "location": {"x": 200, "y": 180, "width": 50, "height": 20}
            })
        
        if analysis_type in ['full', 'pigmentation']:
            detections.append({
                "concern_type": "dark_spots",
                "severity": "mild",
                "confidence": 0.78,
                "location": {"x": 150, "y": 200, "width": 25, "height": 25}
            })
        
        # Calculate overall skin health score
        overall_score = 85.0
        if detections:
            severity_penalties = {
                "mild": 5,
                "moderate": 10,
                "severe": 20
            }
            for detection in detections:
                overall_score -= severity_penalties.get(detection["severity"], 0)
        
        overall_score = max(0.0, min(100.0, overall_score))
        
        return {
            "detections": detections,
            "overall_skin_health_score": overall_score,
            "processed": True
        }
        
    except Exception as e:
        logger.error(f"Error processing image analysis: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to process image analysis"
        )


async def generate_recommendations(detections: List[dict]) -> List[str]:
    """
    Generate product/routine recommendations based on detected skin concerns.
    
    Args:
        detections: List of detected skin concerns
    
    Returns:
        List of recommendation strings
    """
    recommendations = []
    
    concern_recommendations = {
        "acne": [
            "Use a salicylic acid cleanser twice daily",
            "Apply benzoyl peroxide spot treatment to active breakouts",
            "Consider a lightweight, oil-free moisturizer"
        ],
        "fine_lines": [
            "Incorporate retinol into your evening routine",
            "Use a vitamin C serum in the morning",
            "Always apply SPF 50+ sunscreen during the day"
        ],
        "dark_spots": [
            "Use niacinamide serum to fade hyperpigmentation",
            "Apply vitamin C in the morning for brightening",
            "Ensure consistent SPF protection to prevent darkening"
        ],
        "wrinkles": [
            "Use a peptide-rich anti-aging serum",
            "Consider adding hyaluronic acid for hydration",
            "Apply retinol or retinoid treatments at night"
        ],
        "dryness": [
            "Use a gentle, hydrating cleanser",
            "Apply hyaluronic acid serum on damp skin",
            "Use a rich moisturizer with ceramides"
        ]
    }
    
    for detection in detections:
        concern_type = detection.get("concern_type")
        if concern_type in concern_recommendations:
            recommendations.extend(concern_recommendations[concern_type])
    
    # Remove duplicates while preserving order
    seen = set()
    unique_recommendations = []
    for rec in recommendations:
        if rec not in seen:
            seen.add(rec)
            unique_recommendations.append(rec)
    
    return unique_recommendations[:5]  # Return top 5 recommendations


# API Endpoints

@router.post(
    "/upload",
    response_model=AnalysisResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Upload image for skin analysis",
    description="Upload a facial image and receive AI-powered skin analysis results"
)
async def create_analysis(
    file: UploadFile = File(..., description="Facial image file (JPEG, PNG)"),
    request: AnalysisRequest = Depends(),
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
    background_tasks: BackgroundTasks = None
) -> AnalysisResponse:
    """
    Upload and analyze a facial image.
    
    This endpoint:
    1. Validates the uploaded image
    2. Performs AI skin analysis based on requested type
    3. Saves analysis results to database
    4. Returns detailed analysis with recommendations
    
    Args:
        file: Uploaded image file
        request: Analysis request parameters
        current_user: Authenticated user
        db: Database session
        background_tasks: Background task queue
    
    Returns:
        AnalysisResponse with detected concerns and recommendations
    
    Raises:
        HTTPException: If image is invalid or analysis fails
    """
    try:
        # Validate file type
        if not file.content_type.startswith('image/'):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="File must be an image (JPEG, PNG)"
            )
        
        # Read image data
        image_data = await file.read()
        
        if len(image_data) == 0:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Uploaded file is empty"
            )
        
        # Limit file size to 10MB
        if len(image_data) > 10 * 1024 * 1024:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="File size must be less than 10MB"
            )
        
        logger.info(f"Processing analysis for user {current_user.id}, type: {request.analysis_type}")
        
        # Process image analysis
        analysis_results = await process_image_analysis(
            image_data=image_data,
            analysis_type=request.analysis_type,
            user_id=current_user.id
        )
        
        # Generate recommendations if requested
        recommendations = None
        if request.generate_recommendations:
            recommendations = await generate_recommendations(analysis_results["detections"])
        
        # Create unique analysis ID
        analysis_id = str(uuid.uuid4())
        
        # TODO: Store image file to storage (S3/local) and get URL
        image_url = f"/storage/analyses/{analysis_id}.jpg"
        
        # Create database record
        skin_analysis = SkinAnalysis(
            id=analysis_id,
            user_id=current_user.id,
            analysis_type=request.analysis_type,
            image_url=image_url,
            detected_concerns=json.dumps(analysis_results["detections"]),
            overall_skin_health_score=analysis_results["overall_skin_health_score"],
            recommendations=json.dumps(recommendations) if recommendations else None,
            analysis_date=datetime.utcnow()
        )
        
        db.add(skin_analysis)
        await db.commit()
        await db.refresh(skin_analysis)
        
        logger.info(f"Analysis {analysis_id} created successfully for user {current_user.id}")
        
        # Prepare response
        return AnalysisResponse(
            analysis_id=analysis_id,
            user_id=current_user.id,
            analysis_type=request.analysis_type,
            detections=[
                SkinConcernDetection(**detection)
                for detection in analysis_results["detections"]
            ],
            overall_skin_health_score=analysis_results["overall_skin_health_score"],
            recommendations=recommendations,
            analysis_date=skin_analysis.analysis_date,
            image_url=image_url
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error creating analysis: {str(e)}")
        await db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to create analysis"
        )


@router.get(
    "/{analysis_id}",
    response_model=AnalysisResponse,
    summary="Get analysis by ID",
    description="Retrieve detailed results of a specific skin analysis"
)
async def get_analysis(
    analysis_id: str,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
) -> AnalysisResponse:
    """
    Retrieve a specific analysis by ID.
    
    Args:
        analysis_id: Unique analysis identifier
        current_user: Authenticated user
        db: Database session
    
    Returns:
        AnalysisResponse with full analysis details
    
    Raises:
        HTTPException: If analysis not found or user unauthorized
    """
    try:
        # Query analysis from database
        query = select(SkinAnalysis).where(
            and_(
                SkinAnalysis.id == analysis_id,
                SkinAnalysis.user_id == current_user.id
            )
        )
        result = await db.execute(query)
        analysis = result.scalar_one_or_none()
        
        if not analysis:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Analysis not found"
            )
        
        # Parse JSON fields
        detections = json.loads(analysis.detected_concerns) if analysis.detected_concerns else []
        recommendations = json.loads(analysis.recommendations) if analysis.recommendations else None
        
        return AnalysisResponse(
            analysis_id=analysis.id,
            user_id=analysis.user_id,
            analysis_type=analysis.analysis_type,
            detections=[SkinConcernDetection(**d) for d in detections],
            overall_skin_health_score=analysis.overall_skin_health_score,
            recommendations=recommendations,
            analysis_date=analysis.analysis_date,
            image_url=analysis.image_url
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error retrieving analysis {analysis_id}: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve analysis"
        )


@router.get(
    "/",
    response_model=AnalysisHistoryResponse,
    summary="Get user's analysis history",
    description="Retrieve all skin analyses for the current user with pagination"
)
async def get_analysis_history(
    skip: int = 0,
    limit: int = 20,
    analysis_type: Optional[str] = None,
    start_date: Optional[datetime] = None,
    end_date: Optional[datetime] = None,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
) -> AnalysisHistoryResponse:
    """
    Retrieve user's analysis history with optional filtering.
    
    Args:
        skip: Number of records to skip (pagination)
        limit: Maximum number of records to return
        analysis_type: Filter by analysis type (optional)
        start_date: Filter analyses from this date (optional)
        end_date: Filter analyses until this date (optional)
        current_user: Authenticated user
        db: Database session
    
    Returns:
        AnalysisHistoryResponse with list of analyses and total count
    
    Raises:
        HTTPException: If query fails
    """
    try:
        # Build query with filters
        conditions = [SkinAnalysis.user_id == current_user.id]
        
        if analysis_type:
            conditions.append(SkinAnalysis.analysis_type == analysis_type)
        
        if start_date:
            conditions.append(SkinAnalysis.analysis_date >= start_date)
        
        if end_date:
            conditions.append(SkinAnalysis.analysis_date <= end_date)
        
        # Count total matching records
        count_query = select(SkinAnalysis).where(and_(*conditions))
        count_result = await db.execute(count_query)
        total_count = len(count_result.scalars().all())
        
        # Query analyses with pagination
        query = (
            select(SkinAnalysis)
            .where(and_(*conditions))
            .order_by(desc(SkinAnalysis.analysis_date))
            .offset(skip)
            .limit(limit)
        )
        result = await db.execute(query)
        analyses = result.scalars().all()
        
        # Convert to response models
        analysis_responses = []
        for analysis in analyses:
            detections = json.loads(analysis.detected_concerns) if analysis.detected_concerns else []
            recommendations = json.loads(analysis.recommendations) if analysis.recommendations else None
            
            analysis_responses.append(
                AnalysisResponse(
                    analysis_id=analysis.id,
                    user_id=analysis.user_id,
                    analysis_type=analysis.analysis_type,
                    detections=[SkinConcernDetection(**d) for d in detections],
                    overall_skin_health_score=analysis.overall_skin_health_score,
                    recommendations=recommendations,
                    analysis_date=analysis.analysis_date,
                    image_url=analysis.image_url
                )
            )
        
        logger.info(f"Retrieved {len(analysis_responses)} analyses for user {current_user.id}")
        
        return AnalysisHistoryResponse(
            total_count=total_count,
            analyses=analysis_responses
        )
        
    except Exception as e:
        logger.error(f"Error retrieving analysis history: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve analysis history"
        )


@router.delete(
    "/{analysis_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete analysis",
    description="Delete a specific skin analysis record"
)
async def delete_analysis(
    analysis_id: str,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Delete a specific analysis.
    
    Args:
        analysis_id: Unique analysis identifier
        current_user: Authenticated user
        db: Database session
    
    Raises:
        HTTPException: If analysis not found or user unauthorized
    """
    try:
        # Query analysis from database
        query = select(SkinAnalysis).where(
            and_(
                SkinAnalysis.id == analysis_id,
                SkinAnalysis.user_id == current_user.id
            )
        )
        result = await db.execute(query)
        analysis = result.scalar_one_or_none()
        
        if not analysis:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Analysis not found"
            )
        
        # Delete the analysis
        await db.delete(analysis)
        await db.commit()
        
        logger.info(f"Analysis {analysis_id} deleted by user {current_user.id}")
        
        # TODO: Also delete associated image file from storage
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error deleting analysis {analysis_id}: {str(e)}")
        await db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to delete analysis"
        )


@router.get(
    "/compare/{analysis_id_1}/{analysis_id_2}",
    summary="Compare two analyses",
    description="Compare results between two skin analyses to track progress"
)
async def compare_analyses(
    analysis_id_1: str,
    analysis_id_2: str,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
) -> dict:
    """
    Compare two analyses to track skin health progress.
    
    Args:
        analysis_id_1: First analysis ID (typically older)
        analysis_id_2: Second analysis ID (typically newer)
        current_user: Authenticated user
        db: Database session
    
    Returns:
        Comparison data showing improvements or changes
    
    Raises:
        HTTPException: If either analysis not found
    """
    try:
        # Fetch both analyses
        query = select(SkinAnalysis).where(
            and_(
                SkinAnalysis.id.in_([analysis_id_1, analysis_id_2]),
                SkinAnalysis.user_id == current_user.id
            )
        )
        result = await db.execute(query)
        analyses = result.scalars().all()
        
        if len(analyses) != 2:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="One or both analyses not found"
            )
        
        # Order by date (older first)
        analyses_sorted = sorted(analyses, key=lambda x: x.analysis_date)
        analysis_1, analysis_2 = analyses_sorted
        
        # Parse detections
        detections_1 = json.loads(analysis_1.detected_concerns) if analysis_1.detected_concerns else []
        detections_2 = json.loads(analysis_2.detected_concerns) if analysis_2.detected_concerns else []
        
        # Calculate changes
        score_change = analysis_2.overall_skin_health_score - analysis_1.overall_skin_health_score
        
        # Compare concern counts by type
        def count_concerns(detections):
            concern_counts = {}
            for detection in detections:
                concern_type = detection.get("concern_type")
                concern_counts[concern_type] = concern_counts.get(concern_type, 0) + 1
            return concern_counts
        
        concerns_1 = count_concerns(detections_1)
        concerns_2 = count_concerns(detections_2)
        
        # Identify improvements and new concerns
        improvements = []
        new_concerns = []
        
        for concern_type, count_1 in concerns_1.items():
            count_2 = concerns_2.get(concern_type, 0)
            if count_2 < count_1:
                improvements.append({
                    "concern_type": concern_type,
                    "change": count_1 - count_2,
                    "message": f"{concern_type} reduced by {count_1 - count_2}"
                })
        
        for concern_type, count_2 in concerns_2.items():
            count_1 = concerns_1.get(concern_type, 0)
            if count_2 > count_1:
                new_concerns.append({
                    "concern_type": concern_type,
                    "change": count_2 - count_1,
                    "message": f"New or increased {concern_type}: +{count_2 - count_1}"
                })
        
        # Overall assessment
        if score_change > 10:
            overall_trend = "significant_improvement"
        elif score_change > 0:
            overall_trend = "improvement"
        elif score_change == 0:
            overall_trend = "stable"
        elif score_change > -10:
            overall_trend = "slight_decline"
        else:
            overall_trend = "significant_decline"
        
        comparison_result = {
            "analysis_1": {
                "id": analysis_1.id,
                "date": analysis_1.analysis_date,
                "score": analysis_1.overall_skin_health_score
            },
            "analysis_2": {
                "id": analysis_2.id,
                "date": analysis_2.analysis_date,
                "score": analysis_2.overall_skin_health_score
            },
            "score_change": round(score_change, 2),
            "days_between": (analysis_2.analysis_date - analysis_1.analysis_date).days,
            "overall_trend": overall_trend,
            "improvements": improvements,
            "new_concerns": new_concerns,
            "total_concerns_before": len(detections_1),
            "total_concerns_after": len(detections_2)
        }
        
        logger.info(f"Compared analyses {analysis_id_1} and {analysis_id_2} for user {current_user.id}")
        
        return comparison_result
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error comparing analyses: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to compare analyses"
        )