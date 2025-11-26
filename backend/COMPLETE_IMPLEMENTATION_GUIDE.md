# Skincare AI - Complete Backend Implementation Guide

## Table of Contents
1. Security Module (security.py)
2. Database Setup (database.py)
3. Cache Module (cache.py)
4. Logging Configuration (logging.py)
5. Pydantic Schemas
6. Database Models
7. API Route Handlers
8. Deployment Guide

---

## 1. Security Module: `app/core/security.py`

```python
from datetime import datetime, timedelta
from typing import Optional
from jose import JWTError, jwt
from passlib.context import CryptContext
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthCredentials
from sqlalchemy.ext.asyncio import AsyncSession
import logging

from app.core.config import settings
from app.core.database import get_db
from app.models.user import User

logger = logging.getLogger(__name__)
security = HTTPBearer()

# Password context for bcrypt hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify plain password against hashed password"""
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    """Hash password using bcrypt"""
    return pwd_context.hash(password)

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """Create JWT access token"""
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt

def create_refresh_token(data: dict) -> str:
    """Create JWT refresh token"""
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS)
    to_encode.update({"exp": expire, "type": "refresh"})
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt

async def get_current_user(credentials: HTTPAuthCredentials = Depends(security), db: AsyncSession = Depends(get_db)) -> User:
    """Get current authenticated user from JWT token"""
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    try:
        payload = jwt.decode(credentials.credentials, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        user_id: str = payload.get("sub")
        if user_id is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    
    # Query user from database
    result = await db.execute(select(User).where(User.user_id == user_id))
    user = result.scalar_one_or_none()
    
    if user is None:
        raise credentials_exception
    
    return user
```

---

## 2. Database Setup: `app/core/database.py`

```python
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import declarative_base
from sqlalchemy import text
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
    """Initialize database tables"""
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

---

## 3. Cache Module: `app/core/cache.py`

```python
import redis.asyncio as redis
import json
import logging

from app.core.config import settings

logger = logging.getLogger(__name__)

redis_client = None

async def init_redis():
    """Initialize Redis connection"""
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
    """Close Redis connection"""
    if redis_client:
        await redis_client.close()
        logger.info("Redis connection closed")

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
            await redis_client.setex(key, ttl, json.dumps(value))
    except Exception as e:
        logger.error(f"Cache set error: {e}")

async def cache_delete(key: str):
    """Delete value from cache"""
    try:
        if redis_client:
            await redis_client.delete(key)
    except Exception as e:
        logger.error(f"Cache delete error: {e}")
```

---

## 4. Logging Configuration: `app/core/logging.py`

```python
import logging
import logging.handlers
import json
from datetime import datetime
from app.core.config import settings

def setup_logging():
    """Setup logging configuration"""
    log_level = getattr(logging, settings.LOG_LEVEL)
    
    # Create logger
    logger = logging.getLogger()
    logger.setLevel(log_level)
    
    # Create formatter
    if settings.LOG_FORMAT == "json":
        formatter = JsonFormatter()
    else:
        formatter = logging.Formatter(
            '[%(asctime)s] %(levelname)s in %(module)s: %(message)s'
        )
    
    # File handler
    file_handler = logging.handlers.RotatingFileHandler(
        'logs/app.log',
        maxBytes=10485760,  # 10MB
        backupCount=10
    )
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)
    
    # Console handler
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)
    
    return logger

class JsonFormatter(logging.Formatter):
    """JSON formatter for structured logging"""
    def format(self, record):
        log_data = {
            'timestamp': datetime.utcnow().isoformat(),
            'level': record.levelname,
            'logger': record.name,
            'message': record.getMessage(),
            'module': record.module,
            'function': record.funcName,
            'line': record.lineno,
        }
        if record.exc_info:
            log_data['exception'] = self.formatException(record.exc_info)
        return json.dumps(log_data)
```

---

## 5-7. Key Implementation Notes

### Pydantic Schemas Location
- `app/schemas/user.py` - User registration/login/profile
- `app/schemas/analysis.py` - Skin analysis requests/responses
- `app/schemas/routine.py` - Skincare routine schemas
- `app/schemas/notification.py` - Notification schemas

### Database Models Location
- `app/models/user.py` - User model with soft delete
- `app/models/skin_analysis.py` - Analysis results
- `app/models/routine.py` - Routine data
- `app/models/notification.py` - Notifications

### API Routes Location
- `app/api/v1/routes/auth.py` - Authentication routes
- `app/api/v1/routes/users.py` - User management
- `app/api/v1/routes/analysis.py` - Skin analysis
- `app/api/v1/routes/routine.py` - Routine management
- `app/api/v1/routes/notifications.py` - Notifications
- `app/api/v1/routes/dermatologist.py` - Consultant booking

---

## 8. Deployment Checklist

- [ ] PostgreSQL database configured
- [ ] Redis cache cluster set up
- [ ] JWT secrets configured
- [ ] CORS configured for mobile app
- [ ] HTTPS/SSL certificates installed
- [ ] Email service (SMTP) configured
- [ ] Monitoring and logging enabled
- [ ] Backup strategy implemented
- [ ] CI/CD pipeline set up
- [ ] Load testing completed
- [ ] Security audit performed
- [ ] Alerting/monitoring dashboards created

---

## Getting Started

1. Clone the repository
2. Install dependencies: `pip install -r requirements.txt`
3. Configure .env file
4. Run migrations: `alembic upgrade head`
5. Start server: `uvicorn app.main:app --reload`
6. Access docs at http://localhost:8000/api/v1/docs

---

*Last Updated: November 26, 2025*
*Status: Ready for Implementation*