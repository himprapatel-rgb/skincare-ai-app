"""Skincare AI App - FastAPI Backend Main Application

Industry-standard FastAPI application with async support,
microservices architecture, and comprehensive error handling.

Author: AI Engineering Team
Version: 1.0.0
Last Updated: November 25, 2025
"""

import sys
import logging
from contextlib import asynccontextmanager
from typing import AsyncGenerator

from fastapi import FastAPI, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZipMiddleware
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException
import uvicorn

from app.core.config import settings
from app.core.logging import setup_logging
from app.core.database import init_db, close_db
from app.core.cache import init_redis, close_redis
from app.core.monitoring import init_monitoring

# Import routers from microservices
from app.api.v1.routes import auth, analysis, routine, progress, ingredients
from app.api.v1.routes import users, notifications, dermatologist, skin_scan

# Setup logging
setup_logging()
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator:
    """Manage application lifecycle - startup and shutdown events."""
    # Startup
    logger.info("Starting Skincare AI API...")
    
    try:
        # Initialize databases
        await init_db()
        logger.info("Database connections established")
        
        # Initialize Redis cache
        await init_redis()
        logger.info("Redis cache initialized")
        
        # Initialize monitoring
        await init_monitoring()
        logger.info("Monitoring systems initialized")
        
        logger.info("Skincare AI API started successfully")
        
    except Exception as e:
        logger.error(f"Failed to start application: {str(e)}")
        sys.exit(1)
    
    yield
    
    # Shutdown
    logger.info("Shutting down Skincare AI API...")
    
    try:
        await close_redis()
        await close_db()
        logger.info("All connections closed successfully")
        
    except Exception as e:
        logger.error(f"Error during shutdown: {str(e)}")


# Create FastAPI application
app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    description=settings.DESCRIPTION,
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
    docs_url=f"{settings.API_V1_STR}/docs",
    redoc_url=f"{settings.API_V1_STR}/redoc",
    lifespan=lifespan,
)


# Middleware Configuration
# =======================

# CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["X-Request-ID", "X-Rate-Limit"],
)

# GZip compression for responses > 1KB
app.add_middleware(GZipMiddleware, minimum_size=1000)


# Custom Exception Handlers
# ==========================

@app.exception_handler(StarletteHTTPException)
async def http_exception_handler(
    request: Request, 
    exc: StarletteHTTPException
) -> JSONResponse:
    """Handle HTTP exceptions with detailed error responses."""
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": {
                "code": exc.status_code,
                "message": exc.detail,
                "path": str(request.url),
                "method": request.method,
            }
        },
    )


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(
    request: Request,
    exc: RequestValidationError
) -> JSONResponse:
    """Handle request validation errors."""
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={
            "error": {
                "code": 422,
                "message": "Validation error",
                "details": exc.errors(),
                "path": str(request.url),
            }
        },
    )


@app.exception_handler(Exception)
async def general_exception_handler(
    request: Request,
    exc: Exception
) -> JSONResponse:
    """Handle unexpected errors."""
    logger.error(
        f"Unhandled exception: {str(exc)}",
        exc_info=True,
        extra={"path": str(request.url), "method": request.method}
    )
    
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "error": {
                "code": 500,
                "message": "Internal server error",
                "detail": str(exc) if settings.DEBUG else "An error occurred",
            }
        },
    )


# Health Check Endpoints
# =======================

@app.get("/health", tags=["Health"])
async def health_check():
    """Basic health check endpoint."""
    return {
        "status": "healthy",
        "version": settings.VERSION,
        "service": "skincare-ai-api"
    }


@app.get("/health/detailed", tags=["Health"])
async def detailed_health_check():
    """Detailed health check including database and cache status."""
    from app.core.database import check_db_health
    from app.core.cache import check_redis_health
    
    db_status = await check_db_health()
    redis_status = await check_redis_health()
    
    return {
        "status": "healthy" if db_status and redis_status else "degraded",
        "version": settings.VERSION,
        "checks": {
            "database": "ok" if db_status else "error",
            "cache": "ok" if redis_status else "error",
        }
    }


# API Routes
# ===========

# Include all microservice routers
app.include_router(
    auth.router,
    prefix=f"{settings.API_V1_STR}/auth",
    tags=["Authentication"]
)

app.include_router(
    users.router,
    prefix=f"{settings.API_V1_STR}/users",
    tags=["Users"]
)

app.include_router(
    analysis.router,
    prefix=f"{settings.API_V1_STR}/analysis",
    tags=["Skin Analysis"]
)

app.include_router(
    routine.router,
    prefix=f"{settings.API_V1_STR}/routine",
    tags=["Skincare Routine"]
)

app.include_router(
    progress.router,
    prefix=f"{settings.API_V1_STR}/progress",
    tags=["Progress Tracking"]
)

app.include_router(
    ingredients.router,
    prefix=f"{settings.API_V1_STR}/ingredients",
    tags=["Ingredients"]
)

app.include_router(
    notifications.router,
    prefix=f"{settings.API_V1_STR}/notifications",
    tags=["Notifications"]
)

app.include_router(
    dermatologist.router,
    prefix=f"{settings.API_V1_STR}/dermatologist",
    tags=["Dermatologist Services"]
)

app.include_router(
    skin_scan.router,
    prefix=f"{settings.API_V1_STR}/skin-scan",
    tags=["Skin Scan"]
)
# Root endpoint
@app.get("/", tags=["Root"])
async def root():
    """API root endpoint with service information."""
    return {
        "service": settings.PROJECT_NAME,
        "version": settings.VERSION,
        "docs": f"{settings.API_V1_STR}/docs",
        "health": "/health",
        "status": "running"
    }


if __name__ == "__main__":
    # Run with uvicorn for development
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.DEBUG,
        log_level="info",
        access_log=True,
    )
