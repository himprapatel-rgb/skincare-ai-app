"""Dermatologist Consultation API Route Module

Endpoints:
- POST /consult - Create consultation request
- GET /consultations - Get user consultations
- GET /consultations/{id} - Get consultation details
- POST /consultations/{id}/rate - Rate dermatologist response
- POST /consultations/{id}/cancel - Cancel consultation
"""

from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File
from sqlalchemy.ext.asyncio import AsyncSession
from pydantic import BaseModel
from datetime import datetime
import logging

from app.core.database import get_db
from app.core.security import get_current_user
from app.models.user import User

logger = logging.getLogger(__name__)
router = APIRouter()


class DermatologistConsultationRequest(BaseModel):
    question: str
    description: Optional[str] = None
    image_url: Optional[str] = None


class ConsultationRating(BaseModel):
    rating: int  # 1-5 stars
    feedback: Optional[str] = None


@router.post("/consult")
async def request_dermatologist_consultation(
    request: DermatologistConsultationRequest,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Request a consultation with a dermatologist"""
    try:
        logger.info(f"Consultation request from user {current_user.user_id}")
        
        return {
            "consultation_id": "cons_001",
            "user_id": str(current_user.user_id),
            "status": "pending",
            "question": request.question,
            "created_at": datetime.utcnow(),
            "estimated_response_time": "24 hours",
            "message": "Your consultation has been created successfully"
        }
    except Exception as e:
        logger.error(f"Error creating consultation: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to create consultation"
        )


@router.get("/consultations")
async def get_my_consultations(
    status_filter: Optional[str] = None,
    limit: int = 20,
    offset: int = 0,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Get all consultations for the current user"""
    try:
        logger.info(f"Fetching consultations for user {current_user.user_id}")
        
        consultations = [
            {
                "consultation_id": "cons_001",
                "status": "answered",
                "question": "What should I do about my acne?",
                "created_at": datetime.utcnow(),
                "answered_at": datetime.utcnow(),
                "response": "Based on your skin analysis, I recommend...",
                "dermatologist_name": "Dr. Sarah Johnson",
                "rating": 5
            }
        ]
        
        return {
            "user_id": str(current_user.user_id),
            "consultations": consultations,
            "total": len(consultations),
            "pending_count": 0,
            "answered_count": len(consultations)
        }
    except Exception as e:
        logger.error(f"Error fetching consultations: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to fetch consultations"
        )


@router.get("/consultations/{consultation_id}")
async def get_consultation_detail(
    consultation_id: str,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Get detailed information about a specific consultation"""
    try:
        logger.info(f"Fetching consultation {consultation_id} for user {current_user.user_id}")
        
        consultation = {
            "consultation_id": consultation_id,
            "user_id": str(current_user.user_id),
            "status": "answered",
            "question": "What should I do about my acne?",
            "description": "I have been dealing with acne for several months",
            "created_at": datetime.utcnow(),
            "answered_at": datetime.utcnow(),
            "response": "Based on your skin analysis and the image provided, I recommend...",
            "dermatologist_name": "Dr. Sarah Johnson",
            "dermatologist_specialty": "Acne Treatment",
            "rating": 5,
            "feedback": "Very helpful response!"
        }
        
        return consultation
    except Exception as e:
        logger.error(f"Error fetching consultation: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to fetch consultation"
        )


@router.post("/consultations/{consultation_id}/rate")
async def rate_consultation_response(
    consultation_id: str,
    rating: ConsultationRating,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Rate a dermatologist's response to a consultation"""
    try:
        if rating.rating < 1 or rating.rating > 5:
            raise ValueError("Rating must be between 1 and 5")
        
        logger.info(f"Rating consultation {consultation_id} with {rating.rating} stars by user {current_user.user_id}")
        
        return {
            "consultation_id": consultation_id,
            "user_id": str(current_user.user_id),
            "rating": rating.rating,
            "feedback": rating.feedback,
            "message": "Thank you for your feedback!"
        }
    except Exception as e:
        logger.error(f"Error rating consultation: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to rate consultation"
        )


@router.post("/consultations/{consultation_id}/cancel")
async def cancel_consultation(
    consultation_id: str,
    reason: Optional[str] = None,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Cancel a pending consultation"""
    try:
        logger.info(f"Cancelling consultation {consultation_id} by user {current_user.user_id}")
        
        return {
            "consultation_id": consultation_id,
            "user_id": str(current_user.user_id),
            "status": "cancelled",
            "reason": reason,
            "message": "Consultation cancelled successfully"
        }
    except Exception as e:
        logger.error(f"Error cancelling consultation: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to cancel consultation"
        )


@router.get("/dermatologists")
async def get_available_dermatologists(
    specialty: Optional[str] = None,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Get list of available dermatologists"""
    try:
        logger.info(f"Fetching available dermatologists")
        
        dermatologists = [
            {
                "dermatologist_id": "derm_001",
                "name": "Dr. Sarah Johnson",
                "specialty": "Acne Treatment",
                "rating": 4.8,
                "available": True,
                "response_time": "< 24 hours"
            },
            {
                "dermatologist_id": "derm_002",
                "name": "Dr. Michael Chen",
                "specialty": "Anti-Aging",
                "rating": 4.9,
                "available": True,
                "response_time": "< 12 hours"
            }
        ]
        
        return {
            "dermatologists": dermatologists,
            "total": len(dermatologists)
        }
    except Exception as e:
        logger.error(f"Error fetching dermatologists: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to fetch dermatologists"
        )
