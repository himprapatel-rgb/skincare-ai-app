"""Redis cache utilities for caching frequently accessed data."""

from typing import Any, Optional

import redis.asyncio as redis
from redis.asyncio import Redis

from app.core.config import settings


class RedisCache:
    """Redis cache client wrapper."""

    def __init__(self):
        """Initialize Redis cache."""
        self.redis: Optional[Redis] = None

    async def connect(self) -> None:
        """Connect to Redis server."""
        self.redis = await redis.from_url(
            settings.REDIS_URL,
            encoding="utf8",
            decode_responses=True,
        )

    async def disconnect(self) -> None:
        """Disconnect from Redis server."""
        if self.redis:
            await self.redis.close()

    async def get(self, key: str) -> Optional[Any]:
        """Get value from cache.
        
        Args:
            key: Cache key
            
        Returns:
            Cached value or None if not found
        """
        if not self.redis:
            return None
        value = await self.redis.get(key)
        return value

    async def set(
        self, key: str, value: str, expire: int = 3600
    ) -> bool:
        """Set value in cache.
        
        Args:
            key: Cache key
            value: Value to cache
            expire: Expiration time in seconds (default: 1 hour)
            
        Returns:
            True if successful
        """
        if not self.redis:
            return False
        await self.redis.setex(key, expire, value)
        return True

    async def delete(self, key: str) -> bool:
        """Delete value from cache.
        
        Args:
            key: Cache key
            
        Returns:
            Number of keys deleted
        """
        if not self.redis:
            return False
        await self.redis.delete(key)
        return True

    async def clear(self) -> bool:
        """Clear all cache.
        
        Returns:
            True if successful
        """
        if not self.redis:
            return False
        await self.redis.flushdb()
        return True


# Global cache instance
cache = RedisCache()