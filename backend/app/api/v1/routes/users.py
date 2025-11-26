"""Users API Route Module - User Management and Profile Management

Endpoints:
- GET /me - Get current user profile
- PUT /me - Update user profile
- DELETE /me - Delete user account
- GET /me/statistics - Get user statistics
- GET /me/preferences - Get user preferences
- PUT /me/preferences - Update user preferences
"""

from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import datetime
import logging

from app.core.database import get_db
from app.core.security import get_current_user
from app.models.user import User

logger = logging.getLogger(__name__)
router = APIRouter()


@router.get("/me")
async def get_current_user_profile(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Get current authenticated user's profile"""
    try:
        logger.info(f"Fetching profile for user {current_user.user_id}")
        return {
            "user_id": str(current_user.user_id),
            "email": current_user.email,
            "first_name": current_user.first_name,
            "last_name": current_user.last_name,
            "age": current_user.age,
            "skin_type": current_user.skin_type,
            "created_at": current_user.created_at,
            "updated_at": current_user.updated_at,
        }
    except Exception as e:
        logger.error(f"Error fetching user profile: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to fetch user profile"
        )


@router.put("/me")
async def update_user_profile(
    first_name: Optional[str] = None,
    last_name: Optional[str] = None,
    age: Optional[int] = None,
    skin_type: Optional[str] = None,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Update current user's profile"""
    try:
        logger.info(f"Updating profile for user {current_user.user_id}")
        
        if first_name:
            current_user.first_name = first_name
        if last_name:
            current_user.last_name = last_name
        if age:
            current_user.age = age
        if skin_type:
            current_user.skin_type = skin_type
        
        current_user.updated_at = datetime.utcnow()
        db.add(current_user)
        await db.commit()
        await db.refresh(current_user)
        
        logger.info(f"Profile updated successfully for user {current_user.user_id}")
        
        return {
            "user_id": str(current_user.user_id),
            "email": current_user.email,
            "first_name": current_user.first_name,
            "last_name": current_user.last_name,
            "age": current_user.age,
            "skin_type": current_user.skin_type,
            "updated_at": current_user.updated_at,
            "message": "Profile updated successfully"
        }
    except Exception as e:
        await db.rollback()
        logger.error(f"Error updating user profile: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to update user profile"
        )


@router.delete("/me")
async def delete_user_account(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Delete current user's account (soft delete)"""
    try:
        logger.info(f"Deleting account for user {current_user.user_id}")
        
        current_user.is_active = False
        current_user.updated_at = datetime.utcnow()
        db.add(current_user)
        await db.commit()
        
        logger.info(f"Account deleted successfully for user {current_user.user_id}")
        
        return {"message": "Account deleted successfully", "user_id": str(current_user.user_id)}
    except Exception as e:
        await db.rollback()
        logger.error(f"Error deleting user account: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to delete account"
        )


@router.get("/me/statistics")
async def get_user_statistics(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Get user statistics including analysis history and routine adherence"""
    try:
        logger.info(f"Fetching statistics for user {current_user.user_id}")
        
        stats = {
            "user_id": str(current_user.user_id),
            "total_analyses": 0,
            "avg_skin_score": 0.0,
            "last_analysis_date": None,
            "preferred_products": [],
            "routine_adherence_rate": 0.0,
            "joined_date": current_user.created_at
        }
        
        return stats
    except Exception as e:
        logger.error(f"Error fetching user statistics: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to fetch statistics"
        )


@router.get("/me/preferences")
async def get_user_preferences(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Get user preferences"""
    try:
        logger.info(f"Fetching preferences for user {current_user.user_id}")
        
        preferences = current_user.preferences or {
            "notifications_enabled": True,
            "email_reminders": True,
            "language": "en",
            "theme": "light"
        }
        
        return {"user_id": str(current_user.user_id), "preferences": preferences}
    except Exception as e:
        logger.error(f"Error fetching preferences: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to fetch preferences"
        )


@router.put("/me/preferences")
async def update_user_preferences(
    preferences: dict,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Update user preferences"""
    try:
        logger.info(f"Updating preferences for user {current_user.user_id}")
        
        current_user.preferences = preferences
        current_user.updated_at = datetime.utcnow()
        db.add(current_user)
        await db.commit()
        await db.refresh(current_user)
        
        logger.info(f"Preferences updated successfully for user {current_user.user_id}")
        
        return {"message": "Preferences updated successfully", "preferences": preferences}
    except Exception as e:
        await db.rollback()
        logger.error(f"Error updating preferences: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to update preferences"
        )
