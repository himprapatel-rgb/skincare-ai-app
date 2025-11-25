"""
Skincare Routine Builder API Routes

This module implements comprehensive skincare routine management endpoints including:
- Personalized routine creation based on skin analysis
- Morning and evening routine management
- Product step ordering and timing
- Routine modification and customization
- Routine history and adherence tracking

Based on SRS FR-3.3: Personalized Routine Builder Requirements
- Generate customized AM/PM routines based on skin analysis
- Recommend products in correct order (cleanse, treat, moisturize, protect)
- Allow users to modify and save routines
- Track routine adherence and completion
- Provide reminders and notifications

Author: AI Skincare App Team
Version: 1.0
Created: 2024
"""

from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_, desc, update, delete as sql_delete
from typing import List, Optional, Dict
from datetime import datetime, time
from enum import Enum
import logging
import uuid
import json

from app.core.database import get_db
from app.models.user import User
from app.api.v1.routes.auth import get_current_user

# Configure logging
logger = logging.getLogger(__name__)

# Create router
router = APIRouter(
    prefix="/routine",
    tags=["Skincare Routine"],
    responses={
        404: {"description": "Not found"},
        401: {"description": "Unauthorized"},
        500: {"description": "Internal server error"}
    }
)


# Request/Response Models
from pydantic import BaseModel, Field, validator


class RoutineTime(str, Enum):
    """Enum for routine timing"""
    MORNING = "morning"
    EVENING = "evening"
    BOTH = "both"


class ProductStep(BaseModel):
    """Model for individual product step in routine"""
    step_order: int = Field(..., ge=1, description="Order of step in routine")
    product_name: str = Field(..., min_length=1, description="Product name")
    product_category: str = Field(..., description="Category: cleanser, toner, serum, moisturizer, sunscreen")
    instructions: Optional[str] = Field(None, description="Usage instructions")
    wait_time_seconds: Optional[int] = Field(None, description="Wait time after application")
    
    @validator('product_category')
    def validate_category(cls, v):
        valid_categories = [
            'cleanser', 'toner', 'essence', 'serum', 'eye_cream',
            'moisturizer', 'sunscreen', 'spot_treatment', 'mask', 'oil'
        ]
        if v not in valid_categories:
            raise ValueError(f"Product category must be one of: {valid_categories}")
        return v
    
    class Config:
        json_schema_extra = {
            "example": {
                "step_order": 1,
                "product_name": "Gentle Foaming Cleanser",
                "product_category": "cleanser",
                "instructions": "Apply to damp skin, massage gently, rinse with water",
                "wait_time_seconds": 0
            }
        }


class CreateRoutineRequest(BaseModel):
    """Request model for creating a new routine"""
    routine_name: str = Field(..., min_length=1, max_length=100, description="Name for the routine")
    routine_time: RoutineTime = Field(..., description="When to use routine: morning, evening, or both")
    steps: List[ProductStep] = Field(..., min_items=1, description="List of product steps")
    based_on_analysis_id: Optional[str] = Field(None, description="Analysis ID this routine is based on")
    
    @validator('steps')
    def validate_steps_order(cls, v):
        step_orders = [step.step_order for step in v]
        if len(step_orders) != len(set(step_orders)):
            raise ValueError("Step orders must be unique")
        return sorted(v, key=lambda x: x.step_order)
    
    class Config:
        json_schema_extra = {
            "example": {
                "routine_name": "My Morning Glow Routine",
                "routine_time": "morning",
                "steps": [
                    {
                        "step_order": 1,
                        "product_name": "Gentle Cleanser",
                        "product_category": "cleanser",
                        "instructions": "Apply to damp skin"
                    },
                    {
                        "step_order": 2,
                        "product_name": "Vitamin C Serum",
                        "product_category": "serum",
                        "instructions": "Apply 3-4 drops",
                        "wait_time_seconds": 60
                    }
                ]
            }
        }


class RoutineResponse(BaseModel):
    """Response model for routine data"""
    routine_id: str
    user_id: int
    routine_name: str
    routine_time: str
    steps: List[ProductStep]
    created_at: datetime
    updated_at: datetime
    based_on_analysis_id: Optional[str]
    is_active: bool = True
    
    class Config:
        json_schema_extra = {
            "example": {
                "routine_id": "550e8400-e29b-41d4-a716-446655440000",
                "user_id": 123,
                "routine_name": "My Morning Routine",
                "routine_time": "morning",
                "steps": [],
                "created_at": "2024-01-15T08:00:00",
                "updated_at": "2024-01-15T08:00:00",
                "based_on_analysis_id": "550e8400-e29b-41d4-a716-446655440001",
                "is_active": True
            }
        }


class RoutineListResponse(BaseModel):
    """Response model for list of routines"""
    total_count: int
    routines: List[RoutineResponse]
    
    class Config:
        json_schema_extra = {
            "example": {
                "total_count": 2,
                "routines": []
            }
        }


class RoutineAdherenceLog(BaseModel):
    """Model for tracking routine completion"""
    log_id: str
    routine_id: str
    completed_at: datetime
    steps_completed: List[int]
    notes: Optional[str]
    
    class Config:
        json_schema_extra = {
            "example": {
                "log_id": "650e8400-e29b-41d4-a716-446655440000",
                "routine_id": "550e8400-e29b-41d4-a716-446655440000",
                "completed_at": "2024-01-15T08:30:00",
                "steps_completed": [1, 2, 3],
                "notes": "Felt refreshing"
            }
        }


# Helper Functions

def generate_routine_from_analysis(analysis_data: dict, routine_time: str) -> List[ProductStep]:
    """
    Generate recommended routine steps based on skin analysis results.
    
    Args:
        analysis_data: Analysis results with detected concerns
        routine_time: "morning" or "evening"
    
    Returns:
        List of recommended product steps
    """
    steps = []
    step_counter = 1
    
    # Step 1: Always start with cleanser
    steps.append(ProductStep(
        step_order=step_counter,
        product_name="Gentle Hydrating Cleanser" if routine_time == "morning" else "Deep Cleansing Foam",
        product_category="cleanser",
        instructions="Apply to damp skin, massage gently for 60 seconds, rinse with lukewarm water",
        wait_time_seconds=0
    ))
    step_counter += 1
    
    # Step 2: Toner (optional but recommended)
    steps.append(ProductStep(
        step_order=step_counter,
        product_name="Balancing Toner",
        product_category="toner",
        instructions="Apply with cotton pad or pat into skin with hands",
        wait_time_seconds=30
    ))
    step_counter += 1
    
    # Analyze concerns and add treatment steps
    concerns = analysis_data.get("detections", [])
    
    for concern in concerns:
        concern_type = concern.get("concern_type")
        
        if concern_type == "acne" and step_counter <= 5:
            steps.append(ProductStep(
                step_order=step_counter,
                product_name="Salicylic Acid Treatment",
                product_category="serum",
                instructions="Apply to affected areas or entire face",
                wait_time_seconds=60
            ))
            step_counter += 1
        
        elif concern_type in ["fine_lines", "wrinkles"] and routine_time == "evening" and step_counter <= 5:
            steps.append(ProductStep(
                step_order=step_counter,
                product_name="Retinol Serum",
                product_category="serum",
                instructions="Apply pea-sized amount to face, avoiding eye area",
                wait_time_seconds=120
            ))
            step_counter += 1
        
        elif concern_type == "dark_spots" and step_counter <= 5:
            steps.append(ProductStep(
                step_order=step_counter,
                product_name="Vitamin C Brightening Serum" if routine_time == "morning" else "Niacinamide Serum",
                product_category="serum",
                instructions="Apply 3-4 drops, pat gently into skin",
                wait_time_seconds=60
            ))
            step_counter += 1
    
    # Moisturizer (always included)
    steps.append(ProductStep(
        step_order=step_counter,
        product_name="Lightweight Moisturizer" if routine_time == "morning" else "Rich Night Cream",
        product_category="moisturizer",
        instructions="Apply evenly to face and neck",
        wait_time_seconds=60
    ))
    step_counter += 1
    
    # Sunscreen (morning only)
    if routine_time == "morning":
        steps.append(ProductStep(
            step_order=step_counter,
            product_name="Broad Spectrum SPF 50 Sunscreen",
            product_category="sunscreen",
            instructions="Apply generous amount, reapply every 2 hours",
            wait_time_seconds=0
        ))
    
    return steps


# API Endpoints

@router.post(
    "/",
    response_model=RoutineResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create new routine",
    description="Create a new skincare routine with custom or AI-generated steps"
)
async def create_routine(
    request: CreateRoutineRequest,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
) -> RoutineResponse:
    """
    Create a new skincare routine.
    
    This endpoint allows users to:
    1. Create custom routines with their own product selections
    2. Generate AI-powered routines based on previous skin analysis
    
    Args:
        request: Routine creation request with steps
        current_user: Authenticated user
        db: Database session
    
    Returns:
        RoutineResponse with created routine details
    """
    try:
        # Generate unique routine ID
        routine_id = str(uuid.uuid4())
        
        # If based on analysis, fetch analysis data (future enhancement)
        # For now, use provided steps
        
        logger.info(f"Creating routine '{request.routine_name}' for user {current_user.id}")
        
        # Store routine in database
        # Note: In production, create a SkincareRoutine model
        # For now, we'll structure the response
        
        routine_response = RoutineResponse(
            routine_id=routine_id,
            user_id=current_user.id,
            routine_name=request.routine_name,
            routine_time=request.routine_time.value,
            steps=request.steps,
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow(),
            based_on_analysis_id=request.based_on_analysis_id,
            is_active=True
        )
        
        # TODO: Save to database when SkincareRoutine model is created
        
        logger.info(f"Routine {routine_id} created successfully")
        
        return routine_response
        
    except Exception as e:
        logger.error(f"Error creating routine: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to create routine"
        )


@router.get(
    "/{routine_id}",
    response_model=RoutineResponse,
    summary="Get routine by ID",
    description="Retrieve a specific skincare routine"
)
async def get_routine(
    routine_id: str,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
) -> RoutineResponse:
    """
    Retrieve a specific routine by ID.
    
    Args:
        routine_id: Unique routine identifier
        current_user: Authenticated user
        db: Database session
    
    Returns:
        RoutineResponse with routine details
    
    Raises:
        HTTPException: If routine not found
    """
    try:
        # TODO: Query from database when model is ready
        # For now, return mock response
        
        logger.info(f"Retrieving routine {routine_id} for user {current_user.id}")
        
        # Mock response
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Routine not found"
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error retrieving routine: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve routine"
        )


@router.get(
    "/",
    response_model=RoutineListResponse,
    summary="Get user's routines",
    description="Retrieve all skincare routines for the current user"
)
async def list_routines(
    routine_time: Optional[RoutineTime] = Query(None, description="Filter by routine time"),
    is_active: bool = Query(True, description="Filter by active status"),
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
) -> RoutineListResponse:
    """
    List all routines for the current user.
    
    Args:
        routine_time: Filter by morning/evening (optional)
        is_active: Filter by active status
        current_user: Authenticated user
        db: Database session
    
    Returns:
        RoutineListResponse with list of routines
    """
    try:
        logger.info(f"Listing routines for user {current_user.id}")
        
        # TODO: Query from database
        # Return empty list for now
        
        return RoutineListResponse(
            total_count=0,
            routines=[]
        )
        
    except Exception as e:
        logger.error(f"Error listing routines: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to list routines"
        )


@router.put(
    "/{routine_id}",
    response_model=RoutineResponse,
    summary="Update routine",
    description="Update an existing skincare routine"
)
async def update_routine(
    routine_id: str,
    request: CreateRoutineRequest,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
) -> RoutineResponse:
    """
    Update an existing routine.
    
    Args:
        routine_id: Unique routine identifier
        request: Updated routine data
        current_user: Authenticated user
        db: Database session
    
    Returns:
        RoutineResponse with updated routine details
    
    Raises:
        HTTPException: If routine not found
    """
    try:
        logger.info(f"Updating routine {routine_id} for user {current_user.id}")
        
        # TODO: Query and update in database
        
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Routine not found"
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error updating routine: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to update routine"
        )


@router.delete(
    "/{routine_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete routine",
    description="Delete a skincare routine"
)
async def delete_routine(
    routine_id: str,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Delete a routine.
    
    Args:
        routine_id: Unique routine identifier
        current_user: Authenticated user
        db: Database session
    
    Raises:
        HTTPException: If routine not found
    """
    try:
        logger.info(f"Deleting routine {routine_id} for user {current_user.id}")
        
        # TODO: Delete from database
        
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Routine not found"
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error deleting routine: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to delete routine"
        )


@router.post(
    "/{routine_id}/complete",
    response_model=RoutineAdherenceLog,
    status_code=status.HTTP_201_CREATED,
    summary="Log routine completion",
    description="Mark a routine as completed and track adherence"
)
async def log_routine_completion(
    routine_id: str,
    steps_completed: List[int] = Query(..., description="List of completed step orders"),
    notes: Optional[str] = Query(None, description="Optional notes"),
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
) -> RoutineAdherenceLog:
    """
    Log completion of a routine for adherence tracking.
    
    Args:
        routine_id: Unique routine identifier
        steps_completed: List of step orders that were completed
        notes: Optional completion notes
        current_user: Authenticated user
        db: Database session
    
    Returns:
        RoutineAdherenceLog with completion details
    
    Raises:
        HTTPException: If routine not found
    """
    try:
        logger.info(f"Logging completion for routine {routine_id} by user {current_user.id}")
        
        # Generate log ID
        log_id = str(uuid.uuid4())
        
        # TODO: Verify routine exists and belongs to user
        # TODO: Save completion log to database
        
        adherence_log = RoutineAdherenceLog(
            log_id=log_id,
            routine_id=routine_id,
            completed_at=datetime.utcnow(),
            steps_completed=steps_completed,
            notes=notes
        )
        
        logger.info(f"Routine completion logged: {log_id}")
        
        return adherence_log
        
    except Exception as e:
        logger.error(f"Error logging routine completion: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to log routine completion"
        )


@router.get(
    "/{routine_id}/adherence",
    summary="Get routine adherence statistics",
    description="Retrieve completion statistics and adherence rate for a routine"
)
async def get_routine_adherence(
    routine_id: str,
    days: int = Query(30, ge=1, le=365, description="Number of days to analyze"),
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
) -> dict:
    """
    Get adherence statistics for a routine.
    
    Args:
        routine_id: Unique routine identifier
        days: Number of days to analyze
        current_user: Authenticated user
        db: Database session
    
    Returns:
        Dictionary with adherence statistics
    
    Raises:
        HTTPException: If routine not found
    """
    try:
        logger.info(f"Retrieving adherence for routine {routine_id}")
        
        # TODO: Query completion logs from database
        # TODO: Calculate statistics
        
        # Mock response
        return {
            "routine_id": routine_id,
            "period_days": days,
            "total_completions": 0,
            "adherence_rate": 0.0,
            "average_completion_time": "00:00",
            "most_skipped_steps": [],
            "completion_streak": 0,
            "longest_streak": 0
        }
        
    except Exception as e:
        logger.error(f"Error retrieving adherence: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve adherence statistics"
        )


@router.post(
    "/generate",
    response_model=RoutineResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Generate AI-powered routine",
    description="Generate a personalized routine based on skin analysis results"
)
async def generate_ai_routine(
    analysis_id: str = Query(..., description="Analysis ID to base routine on"),
    routine_time: RoutineTime = Query(..., description="Morning or evening routine"),
    routine_name: Optional[str] = Query(None, description="Custom name for routine"),
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
) -> RoutineResponse:
    """
    Generate an AI-powered personalized routine based on skin analysis.
    
    Args:
        analysis_id: ID of skin analysis to base routine on
        routine_time: Morning or evening
        routine_name: Optional custom name
        current_user: Authenticated user
        db: AsyncSession: Database session
    
    Returns:
        RoutineResponse with generated routine
    
    Raises:
        HTTPException: If analysis not found
    """
    try:
        logger.info(f"Generating AI routine for user {current_user.id} based on analysis {analysis_id}")
        
        # TODO: Fetch analysis data from database
        # Mock analysis data for demonstration
        mock_analysis = {
            "detections": [
                {"concern_type": "acne", "severity": "moderate"},
                {"concern_type": "dark_spots", "severity": "mild"}
            ]
        }
        
        # Generate routine steps using helper function
        generated_steps = generate_routine_from_analysis(
            mock_analysis,
            routine_time.value
        )
        
        # Create routine name if not provided
        if not routine_name:
            routine_name = f"AI-Generated {routine_time.value.capitalize()} Routine"
        
        # Generate routine ID
        routine_id = str(uuid.uuid4())
        
        routine_response = RoutineResponse(
            routine_id=routine_id,
            user_id=current_user.id,
            routine_name=routine_name,
            routine_time=routine_time.value,
            steps=generated_steps,
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow(),
            based_on_analysis_id=analysis_id,
            is_active=True
        )
        
        # TODO: Save to database
        
        logger.info(f"AI routine {routine_id} generated successfully")
        
        return routine_response
        
    except Exception as e:
        logger.error(f"Error generating AI routine: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to generate AI routine"
        )