# Backend Code Samples - Complete Implementation

## Authentication & Security Module

### JWT Token Handler (`backend/app/core/security.py`)

```python
from datetime import datetime, timedelta
from typing import Optional
from jose import JWTError, jwt
from passlib.context import CryptContext
from fastapi import Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
import logging

from app.core.config import settings
from app.core.database import get_db
from app.models.user import User

logger = logging.getLogger(__name__)

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify password against hash"""
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    """Hash password"""
    return pwd_context.hash(password)

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """Create JWT access token"""
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(
            hours=settings.JWT_EXPIRATION_HOURS
        )
    
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(
        to_encode,
        settings.JWT_SECRET_KEY,
        algorithm=settings.JWT_ALGORITHM
    )
    return encoded_jwt

async def get_current_user(
    token: str = Depends(HTTPBearer()),
    db: AsyncSession = Depends(get_db)
) -> User:
    """Get current authenticated user from token"""
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(
            token,
            settings.JWT_SECRET_KEY,
            algorithms=[settings.JWT_ALGORITHM]
        )
        user_id: str = payload.get("sub")
        if user_id is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    
    # Query user from database
    user = await db.query(User).filter(User.user_id == user_id).first()
    if user is None:
        raise credentials_exception
    return user
```

## Database Models

### User ORM Model (`backend/app/models/user.py`)

```python
from sqlalchemy import Column, String, Integer, Float, DateTime, Boolean
from sqlalchemy.dialects.postgresql import JSON, UUID
from datetime import datetime
import uuid

from app.core.database import Base

class User(Base):
    __tablename__ = "users"
    
    user_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    email = Column(String, unique=True, nullable=False, index=True)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    hashed_password = Column(String, nullable=False)
    age = Column(Integer, nullable=True)
    skin_type = Column(String, nullable=True)  # normal, dry, oily, sensitive, combination
    is_active = Column(Boolean, default=True)
    preferences = Column(JSON, default={})
    profile_picture_url = Column(String, nullable=True)
    last_login = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __repr__(self):
        return f"<User {self.email}>"
```

### Skin Analysis Result Model (`backend/app/models/analysis_result.py`)

```python
from sqlalchemy import Column, String, Integer, Float, DateTime, ForeignKey, JSON
from sqlalchemy.dialects.postgresql import UUID
from datetime import datetime
import uuid

from app.core.database import Base

class SkinAnalysisResult(Base):
    __tablename__ = "skin_analysis_results"
    
    analysis_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.user_id"), nullable=False)
    
    # Skin metrics
    skin_score = Column(Float, nullable=False)  # 0-100
    hydration_level = Column(Float)  # 0-100
    oiliness_level = Column(Float)  # 0-100
    elasticity_level = Column(Float)  # 0-100
    pore_size = Column(Float)  # 0-100
    
    # Analysis details
    skin_type_detected = Column(String)  # Detected skin type
    conditions_detected = Column(JSON, default=list)  # e.g., ["acne", "dryness"]
    recommendations = Column(JSON, default=list)  # Personalized recommendations
    routine = Column(JSON, default={})  # Morning and evening routines
    
    # Image data
    image_url = Column(String, nullable=True)
    image_base64 = Column(String, nullable=True)  # For processing
    
    # Metadata
    analysis_duration_seconds = Column(Float)
    confidence_score = Column(Float)  # Confidence in analysis
    
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
```

## API Request/Response Models

### Pydantic Schemas (`backend/app/schemas/analysis.py`)

```python
from pydantic import BaseModel, EmailStr
from typing import Optional, List
from datetime import datetime

class SkinAnalysisRequest(BaseModel):
    image_url: str
    skin_type_hint: Optional[str] = None
    
class SkinMetrics(BaseModel):
    hydration: float
    oiliness: float
    elasticity: float
    pores: float
    
class SkinAnalysisResponse(BaseModel):
    analysis_id: str
    skin_score: float
    metrics: SkinMetrics
    conditions: List[str]
    recommendations: List[str]
    routine: dict
    created_at: datetime
    
    class Config:
        from_attributes = True
```

## Database Configuration

### Enhanced Database Setup (`backend/app/core/database.py`)

```python
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import declarative_base
from sqlalchemy import event
import logging

from app.core.config import settings

logger = logging.getLogger(__name__)

engine = create_async_engine(
    settings.DATABASE_URL,
    echo=settings.DEBUG,
    pool_size=20,
    max_overflow=40,
    pool_pre_ping=True,
    pool_recycle=3600,
)

AsyncSessionLocal = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autoflush=False,
    autocommit=False,
)

Base = declarative_base()

async def get_db() -> AsyncSession:
    """Dependency for getting database session"""
    async with AsyncSessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()

async def init_db():
    """Initialize database connections"""
    try:
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
        logger.info("Database initialized successfully")
    except Exception as e:
        logger.error(f"Error initializing database: {e}")
        raise

async def close_db():
    """Close database connections"""
    await engine.dispose()
    logger.info("Database connections closed")

async def check_db_health() -> bool:
    """Check database health"""
    try:
        async with engine.connect() as conn:
            await conn.execute(text("SELECT 1"))
        return True
    except Exception as e:
        logger.error(f"Database health check failed: {e}")
        return False
```

## Advanced Features

### Caching with Redis (`backend/app/core/cache.py`)

```python
import redis.asyncio as redis
import json
import logging

from app.core.config import settings

logger = logging.getLogger(__name__)

redis_client = None

async def init_redis():
    global redis_client
    try:
        redis_client = await redis.from_url(
            settings.REDIS_URL,
            encoding="utf8",
            decode_responses=True
        )
        await redis_client.ping()
        logger.info("Redis cache initialized successfully")
    except Exception as e:
        logger.error(f"Error initializing Redis: {e}")
        raise

async def close_redis():
    if redis_client:
        await redis_client.close()

async def cache_get(key: str):
    """Get value from cache"""
    try:
        if redis_client:
            value = await redis_client.get(key)
            return json.loads(value) if value else None
    except Exception as e:
        logger.error(f"Cache get error: {e}")
    return None

async def cache_set(key: str, value: any, ttl: int = 3600):
    """Set value in cache with TTL"""
    try:
        if redis_client:
            await redis_client.setex(
                key,
                ttl,
                json.dumps(value)
            )
    except Exception as e:
        logger.error(f"Cache set error: {e}")
```

## Deployment & Production Checklist

- [ ] Configure PostgreSQL database in production
- [ ] Set up Redis cache cluster
- [ ] Configure JWT secrets and API keys
- [ ] Set up email service (SMTP)
- [ ] Enable HTTPS/SSL certificates
- [ ] Configure CORS for mobile app
- [ ] Set up monitoring and logging
- [ ] Configure backup strategy
- [ ] Set up CI/CD pipeline
- [ ] Load testing and optimization
- [ ] Security audit and penetration testing
- [ ] Set up alerting and monitoring dashboards
