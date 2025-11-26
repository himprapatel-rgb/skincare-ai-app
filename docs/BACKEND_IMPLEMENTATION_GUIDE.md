# Skincare AI Backend Implementation Guide

## Overview
This guide provides comprehensive backend implementation code for the Skincare AI Flask/FastAPI application.

## 1. Missing Route Files to Create

### 1.1 Users Route (`backend/app/api/v1/routes/users.py`)

```python
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

class UserProfileResponse(BaseModel):
    user_id: str
    email: str
    first_name: str
    last_name: str
    age: Optional[int] = None
    skin_type: Optional[str] = None
    created_at: datetime
    updated_at: datetime

class UpdateUserRequest(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    age: Optional[int] = None
    skin_type: Optional[str] = None

@router.get("/me", response_model=UserProfileResponse)
async def get_current_user_profile(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    try:
        logger.info(f"Fetching profile for user {current_user.user_id}")
        return {
            "user_id": current_user.user_id,
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

@router.put("/me", response_model=UserProfileResponse)
async def update_user_profile(
    update_data: UpdateUserRequest,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    try:
        if update_data.first_name:
            current_user.first_name = update_data.first_name
        if update_data.last_name:
            current_user.last_name = update_data.last_name
        if update_data.age:
            current_user.age = update_data.age
        if update_data.skin_type:
            current_user.skin_type = update_data.skin_type
        
        current_user.updated_at = datetime.utcnow()
        db.add(current_user)
        await db.commit()
        await db.refresh(current_user)
        
        return current_user
    except Exception as e:
        await db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to update user profile"
        )

@router.delete("/me")
async def delete_user_account(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    try:
        current_user.is_active = False
        db.add(current_user)
        await db.commit()
        return {"message": "Account deleted successfully"}
    except Exception as e:
        await db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to delete account"
        )
```

### 1.2 Notifications Route (`backend/app/api/v1/routes/notifications.py`)

```python
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import datetime
import logging

from app.core.database import get_db
from app.core.security import get_current_user
from app.models.user import User

logger = logging.getLogger(__name__)
router = APIRouter()

@router.get("/")
async def get_notifications(
    limit: int = 20,
    offset: int = 0,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    try:
        logger.info(f"Fetching notifications for user {current_user.user_id}")
        notifications = [
            {
                "id": "notif_1",
                "title": "Time for your morning routine",
                "message": "Don't forget your skincare routine",
                "timestamp": datetime.utcnow(),
                "read": False,
                "type": "reminder"
            }
        ]
        return {"notifications": notifications, "total": len(notifications)}
    except Exception as e:
        logger.error(f"Error fetching notifications: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to fetch notifications"
        )

@router.post("/{notification_id}/read")
async def mark_notification_as_read(
    notification_id: str,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    try:
        return {"message": "Notification marked as read"}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to update notification"
        )
```

### 1.3 Dermatologist Route (`backend/app/api/v1/routes/dermatologist.py`)

```python
from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File
from sqlalchemy.ext.asyncio import AsyncSession
from pydantic import BaseModel
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

@router.post("/consult")
async def request_dermatologist_consultation(
    request: DermatologistConsultationRequest,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    try:
        logger.info(f"Consultation request from user {current_user.user_id}")
        return {
            "consultation_id": "cons_123",
            "status": "pending",
            "question": request.question,
            "created_at": datetime.utcnow(),
            "estimated_response_time": "24 hours"
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to create consultation"
        )

@router.get("/consultations")
async def get_my_consultations(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    try:
        return {
            "consultations": [],
            "total": 0
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to fetch consultations"
        )
```

## 2. Enhanced ORM Models to Add

### 2.1 Update User Model (`backend/app/models/user.py`)

Add these fields:
- `preferences`: JSON field for user preferences
- `is_active`: Boolean field
- `last_login`: DateTime field
- `profile_picture_url`: String field

### 2.2 Create Analysis Result Model (`backend/app/models/analysis_result.py`)

```python
from sqlalchemy import Column, String, Integer, Float, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import JSON
from datetime import datetime
from app.core.database import Base

class AnalysisResult(Base):
    __tablename__ = "analysis_results"
    
    id = Column(String, primary_key=True)
    user_id = Column(String, ForeignKey("users.user_id"), nullable=False)
    skin_score = Column(Float)
    hydration = Column(Float)
    oiliness = Column(Float)
    elasticity = Column(Float)
    pores = Column(Float)
    recommendations = Column(JSON)
    image_url = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
```

## 3. Environment Variables to Configure

Add to `.env`:
```
DATABASE_URL=postgresql+asyncpg://user:password@localhost/skincare_db
REDIS_URL=redis://localhost:6379/0
JWT_SECRET_KEY=your-secret-key-here
JWT_ALGORITHM=HS256
JWT_EXPIRATION_HOURS=24
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=your-email@gmail.com
SMTP_PASSWORD=your-app-password
```

## 4. Testing the Backend

```bash
# Install dependencies
pip install -r requirements.txt

# Run migrations
alembic upgrade head

# Start the server
uvicorn app.main:app --reload

# Access Swagger docs
http://localhost:8000/api/v1/docs
```

## 5. API Endpoints Summary

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/v1/auth/register` | Register new user |
| POST | `/api/v1/auth/login` | User login |
| GET | `/api/v1/users/me` | Get current user profile |
| PUT | `/api/v1/users/me` | Update user profile |
| POST | `/api/v1/analysis` | Submit skin analysis |
| GET | `/api/v1/recommendations` | Get personalized recommendations |
| GET | `/api/v1/notifications` | Get user notifications |
| POST | `/api/v1/dermatologist/consult` | Request dermatologist consultation |

## 6. Next Steps

1. Implement all route files
2. Add database migrations
3. Configure authentication
4. Set up email notifications
5. Integrate AI/ML models for analysis
6. Add comprehensive testing
7. Deploy to production
