"""Database Connection & Session Management

Async SQLAlchemy database connections for PostgreSQL.
Provides session management and health checks.

Author: AI Engineering Team
Version: 1.0.0
"""

import logging
from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import (
    AsyncSession,
    create_async_engine,
    async_sessionmaker,
    AsyncEngine
)
from sqlalchemy.orm import declarative_base
from sqlalchemy.pool import NullPool, AsyncAdaptedQueuePool
from sqlalchemy import text

from app.core.config import settings

logger = logging.getLogger(__name__)

# Create declarative base for models
Base = declarative_base()

# Global engine and session maker
engine: AsyncEngine | None = None
SessionLocal: async_sessionmaker[AsyncSession] | None = None


async def init_db() -> None:
    """
    Initialize database connection pool.
    Called during application startup.
    """
    global engine, SessionLocal
    
    logger.info(f"Initializing database connection to {settings.POSTGRES_SERVER}")
    
    try:
        # Create async engine with connection pooling
        engine = create_async_engine(
            settings.SQLALCHEMY_DATABASE_URI,
            echo=settings.DEBUG,  # Log SQL queries in debug mode
            pool_size=settings.POSTGRES_POOL_SIZE,
            max_overflow=settings.POSTGRES_MAX_OVERFLOW,
            pool_pre_ping=True,  # Verify connections before using
            pool_recycle=3600,  # Recycle connections after 1 hour
            poolclass=AsyncAdaptedQueuePool if not settings.TESTING else NullPool,
        )
        
        # Create async session maker
        SessionLocal = async_sessionmaker(
            engine,
            class_=AsyncSession,
            expire_on_commit=False,
            autocommit=False,
            autoflush=False,
        )
        
        # Test database connection
        async with engine.begin() as conn:
            await conn.execute(text("SELECT 1"))
        
        logger.info("Database connection established successfully")
        
    except Exception as e:
        logger.error(f"Failed to initialize database: {str(e)}")
        raise


async def close_db() -> None:
    """
    Close database connections.
    Called during application shutdown.
    """
    global engine
    
    if engine:
        logger.info("Closing database connections")
        await engine.dispose()
        engine = None
        logger.info("Database connections closed")


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """
    Dependency for getting async database sessions.
    
    Usage:
        @app.get("/users")
        async def get_users(db: AsyncSession = Depends(get_db)):
            result = await db.execute(select(User))
            return result.scalars().all()
    """
    if SessionLocal is None:
        raise RuntimeError(
            "Database not initialized. Call init_db() during startup."
        )
    
    async with SessionLocal() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()


async def check_db_health() -> bool:
    """
    Check database connection health.
    Used by health check endpoints.
    
    Returns:
        bool: True if database is accessible, False otherwise
    """
    if not engine:
        return False
    
    try:
        async with engine.begin() as conn:
            await conn.execute(text("SELECT 1"))
        return True
    except Exception as e:
        logger.error(f"Database health check failed: {str(e)}")
        return False


async def create_tables() -> None:
    """
    Create all database tables.
    
    Note: In production, use Alembic migrations instead.
    This is useful for testing and development.
    """
    if not engine:
        raise RuntimeError("Database engine not initialized")
    
    logger.info("Creating database tables...")
    
    async with engine.begin() as conn:
        # Import all models to register them with Base
        from app.models import user, skin_analysis  # noqa: F401
        
        await conn.run_sync(Base.metadata.create_all)
    
    logger.info("Database tables created successfully")


async def drop_tables() -> None:
    """
    Drop all database tables.
    
    WARNING: This will delete all data!
    Only use in testing/development.
    """
    if not engine:
        raise RuntimeError("Database engine not initialized")
    
    if settings.ENVIRONMENT == "production":
        raise RuntimeError(
            "Cannot drop tables in production environment!"
        )
    
    logger.warning("Dropping all database tables...")
    
    async with engine.begin() as conn:
        from app.models import user, skin_analysis  # noqa: F401
        
        await conn.run_sync(Base.metadata.drop_all)
    
    logger.info("Database tables dropped")
