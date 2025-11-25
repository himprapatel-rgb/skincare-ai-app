"""Application Configuration using Pydantic Settings

Environment-based configuration with validation and type safety.
Supports .env files and environment variables.

Author: AI Engineering Team
Version: 1.0.0
"""

import secrets
from typing import List, Optional, Union
from pydantic import AnyHttpUrl, field_validator, EmailStr
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings with environment variable support."""
    
    # API Configuration
    PROJECT_NAME: str = "Skincare AI API"
    VERSION: str = "1.0.0"
    DESCRIPTION: str = "AI-powered skincare analysis and recommendation system"
    API_V1_STR: str = "/api/v1"
    
    # Environment
    DEBUG: bool = False
    ENVIRONMENT: str = "production"  # development, staging, production
    
    # Security
    SECRET_KEY: str = secrets.token_urlsafe(32)
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7  # 7 days
    REFRESH_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 30  # 30 days
    ALGORITHM: str = "RS256"  # RSA signing
    
    # CORS
    ALLOWED_ORIGINS: List[Union[str, AnyHttpUrl]] = [
        "http://localhost:3000",
        "http://localhost:8080",
        "https://skincare-ai.app",
    ]
    
    @field_validator("ALLOWED_ORIGINS", mode="before")
    @classmethod
    def parse_cors_origins(cls, v: Union[str, List[str]]) -> List[str]:
        if isinstance(v, str):
            return [origin.strip() for origin in v.split(",")]
        return v
    
    # PostgreSQL Database
    POSTGRES_SERVER: str = "localhost"
    POSTGRES_PORT: int = 5432
    POSTGRES_USER: str = "skincare_user"
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str = "skincare_ai"
    POSTGRES_POOL_SIZE: int = 20
    POSTGRES_MAX_OVERFLOW: int = 40
    
    @property
    def SQLALCHEMY_DATABASE_URI(self) -> str:
        """Build PostgreSQL connection string."""
        return (
            f"postgresql+asyncpg://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}"
            f"@{self.POSTGRES_SERVER}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"
        )
    
    # MongoDB
    MONGODB_URL: str = "mongodb://localhost:27017"
    MONGODB_DB: str = "skincare_ai_ingredients"
    MONGODB_MAX_POOL_SIZE: int = 100
    MONGODB_MIN_POOL_SIZE: int = 10
    
    # Redis Cache
    REDIS_HOST: str = "localhost"
    REDIS_PORT: int = 6379
    REDIS_DB: int = 0
    REDIS_PASSWORD: Optional[str] = None
    REDIS_SSL: bool = False
    REDIS_TTL: int = 3600  # 1 hour default TTL
    
    @property
    def REDIS_URL(self) -> str:
        """Build Redis connection string."""
        auth = f":{self.REDIS_PASSWORD}@" if self.REDIS_PASSWORD else ""
        protocol = "rediss" if self.REDIS_SSL else "redis"
        return f"{protocol}://{auth}{self.REDIS_HOST}:{self.REDIS_PORT}/{self.REDIS_DB}"
    
    # AWS S3 / MinIO Storage
    S3_ENDPOINT_URL: Optional[str] = None  # For MinIO or S3-compatible
    S3_BUCKET_NAME: str = "skincare-ai-uploads"
    S3_REGION: str = "us-east-1"
    AWS_ACCESS_KEY_ID: Optional[str] = None
    AWS_SECRET_ACCESS_KEY: Optional[str] = None
    
    # Image Upload Limits
    MAX_UPLOAD_SIZE: int = 10 * 1024 * 1024  # 10MB
    ALLOWED_IMAGE_TYPES: List[str] = ["image/jpeg", "image/png", "image/webp"]
    IMAGE_COMPRESSION_QUALITY: int = 85
    
    # ML Model Paths
    MODEL_BASE_PATH: str = "/app/models"
    ACNE_DETECTION_MODEL: str = "acne_yolov8n.tflite"
    WRINKLE_DETECTION_MODEL: str = "wrinkle_unet.tflite"
    PIGMENTATION_MODEL: str = "pigmentation_deeplab.tflite"
    SKIN_TYPE_MODEL: str = "skin_type_mobilenet.tflite"
    
    # ML Model Settings
    ML_BATCH_SIZE: int = 1
    ML_NUM_THREADS: int = 4
    ML_CONFIDENCE_THRESHOLD: float = 0.75
    ML_NMS_IOU_THRESHOLD: float = 0.45
    
    # Rate Limiting
    RATE_LIMIT_PER_MINUTE: int = 60
    RATE_LIMIT_PER_HOUR: int = 1000
    RATE_LIMIT_PER_DAY: int = 10000
    
    # Email (SendGrid / AWS SES)
    SMTP_HOST: Optional[str] = None
    SMTP_PORT: int = 587
    SMTP_USER: Optional[str] = None
    SMTP_PASSWORD: Optional[str] = None
    SMTP_FROM_EMAIL: EmailStr = "noreply@skincare-ai.app"
    SMTP_FROM_NAME: str = "Skincare AI"
    
    # Notification Services
    FIREBASE_CREDENTIALS_PATH: Optional[str] = None
    APNS_KEY_PATH: Optional[str] = None
    APNS_KEY_ID: Optional[str] = None
    APNS_TEAM_ID: Optional[str] = None
    
    # Monitoring & Logging
    SENTRY_DSN: Optional[str] = None
    LOG_LEVEL: str = "INFO"
    LOG_FORMAT: str = "json"  # json or text
    
    # External API Keys
    OPENAI_API_KEY: Optional[str] = None  # For GPT-based features
    STRIPE_API_KEY: Optional[str] = None  # For payments
    STRIPE_WEBHOOK_SECRET: Optional[str] = None
    
    # Feature Flags
    ENABLE_DERMATOLOGIST_BOOKING: bool = False
    ENABLE_SOCIAL_SHARING: bool = True
    ENABLE_PRODUCT_RECOMMENDATIONS: bool = True
    ENABLE_AI_ROUTINE_BUILDER: bool = True
    
    # Performance Tuning
    WORKER_COUNT: int = 4
    WORKER_TIMEOUT: int = 120
    KEEPALIVE: int = 5
    
    # Testing
    TESTING: bool = False
    TEST_DATABASE_URL: Optional[str] = None
    
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
        extra="ignore",
    )


# Create global settings instance
settings = Settings()


# Development environment check
def is_development() -> bool:
    """Check if running in development mode."""
    return settings.ENVIRONMENT == "development" or settings.DEBUG


def is_production() -> bool:
    """Check if running in production mode."""
    return settings.ENVIRONMENT == "production" and not settings.DEBUG
