"""Skin Scan API Route - Connect to AI Skin Analysis Service.

This module provides a clean API endpoint that uses the
skin_analysis_service for actual AI-powered skin analysis.
"""
from fastapi import APIRouter, UploadFile, File, HTTPException, Depends
from fastapi.responses import JSONResponse
from typing import Optional
import base64
import logging

from app.services.skin_analysis_service import skin_analysis_service

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/skin-scan", tags=["Skin Scan"])


@router.post("/analyze")
async def analyze_skin(
    file: UploadFile = File(...),
    user_id: Optional[str] = None
):
    """
    Analyze skin from uploaded image using AI.
    
    Args:
        file: Image file (JPEG, PNG)
        user_id: Optional user ID for tracking
    
    Returns:
        Complete skin analysis with:
        - Overall health score (0-100)
        - Skin type classification
        - Detected concerns with severity
        - Personalized recommendations
        - Detailed skin metrics
    """
    # Validate file type
    allowed_types = ["image/jpeg", "image/png", "image/jpg"]
    if file.content_type not in allowed_types:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid file type. Allowed: {allowed_types}"
        )
    
    try:
        # Read image data
        image_data = await file.read()
        
        # Convert to base64
        image_base64 = base64.b64encode(image_data).decode("utf-8")
        
        # Call the skin analysis service
        result = await skin_analysis_service.analyze_skin(
            image_base64=image_base64,
            user_id=user_id
        )
        
        return JSONResponse(
            status_code=200,
            content={
                "success": True,
                "data": {
                    "overall_score": result.overall_score,
                    "skin_type": result.skin_type,
                    "skin_age": result.skin_age,
                    "concerns": [
                        {
                            "type": c.concern_type,
                            "severity": c.severity,
                            "confidence": c.confidence,
                            "recommendations": c.recommendations
                        }
                        for c in result.concerns
                    ],
                    "metrics": {
                        "hydration": result.metrics.hydration_score,
                        "oiliness": result.metrics.oiliness_score,
                        "texture": result.metrics.texture_score,
                        "elasticity": result.metrics.elasticity_score,
                        "pore_size": result.metrics.pore_size_score,
                        "skin_tone_evenness": result.metrics.skin_tone_evenness
                    },
                    "recommendations": result.recommendations,
                    "confidence_score": result.confidence_score,
                    "image_quality": result.image_quality_score,
                    "analyzed_at": result.analysis_timestamp.isoformat()
                }
            }
        )
        
    except Exception as e:
        logger.error(f"Skin analysis failed: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Analysis failed: {str(e)}"
        )


@router.post("/analyze-url")
async def analyze_skin_from_url(
    image_url: str,
    user_id: Optional[str] = None
):
    """
    Analyze skin from image URL.
    
    Args:
        image_url: Public URL of the image
        user_id: Optional user ID for tracking
    
    Returns:
        Complete skin analysis results
    """
    try:
        result = await skin_analysis_service.analyze_skin(
            image_url=image_url,
            user_id=user_id
        )
        
        return JSONResponse(
            status_code=200,
            content={
                "success": True,
                "data": {
                    "overall_score": result.overall_score,
                    "skin_type": result.skin_type,
                    "skin_age": result.skin_age,
                    "concerns": [
                        {
                            "type": c.concern_type,
                            "severity": c.severity,
                            "confidence": c.confidence,
                            "recommendations": c.recommendations
                        }
                        for c in result.concerns
                    ],
                    "metrics": {
                        "hydration": result.metrics.hydration_score,
                        "oiliness": result.metrics.oiliness_score,
                        "texture": result.metrics.texture_score,
                        "elasticity": result.metrics.elasticity_score,
                        "pore_size": result.metrics.pore_size_score,
                        "skin_tone_evenness": result.metrics.skin_tone_evenness
                    },
                    "recommendations": result.recommendations,
                    "confidence_score": result.confidence_score,
                    "image_quality": result.image_quality_score,
                    "analyzed_at": result.analysis_timestamp.isoformat()
                }
            }
        )
        
    except Exception as e:
        logger.error(f"Skin analysis from URL failed: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Analysis failed: {str(e)}"
        )


@router.get("/health")
async def health_check():
    """Health check endpoint for the skin scan service."""
    return {"status": "healthy", "service": "skin-scan"}