import redis.asyncio as redis
from typing import Any

class AuthRedisRepository:
    def __init__(self,  redis_client: redis.Redis):
        self.redis = redis_client

    async def check_redis_ping(self):
        return await self.redis.ping()

    async def set_redis(self, key: str, value: Any, ex: int):
        """
        set email certification code to redis
        """
        return await self.redis.set(key, value, ex=ex)
    
    async def get_redis(self, key: str):
        """
        get email certification code from redis
        """
        return await self.redis.get(key)

    async def delete_redis(self, key):
        """
        delete email certification code from redis
        """
        return await self.redis.delete(key)

    async def check_timeout_redis(self, key: str):
        """
        check redis timeout
        """
        return await self.redis.ttl(key)