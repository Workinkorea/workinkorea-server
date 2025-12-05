import redis.asyncio as redis
from app.auth.repositories.redis import AuthRedisRepository
from fastapi.responses import JSONResponse

class AuthRedisService:
    def __init__(self, redis_client: redis.Redis):
        self.auth_redis_repository = AuthRedisRepository(redis_client)

    async def set_email_certify_code(self, email: str, code: int):
        """
        set email certification code to redis
        args:
            email: str
            code: int
        """
        return await self.auth_redis_repository.set_redis(email, code, ex=60*3)
    
    async def get_email_certify_code(self, email: str, code: int):
        """
        get email certification code from redis
        args:
            email: str
        """
        get_redis_code = await self.auth_redis_repository.get_redis(email)
        if not get_redis_code:
            return JSONResponse(content={"error": "Email certification code not found"}, status_code=404)
        
        if get_redis_code != code:
            return JSONResponse(content={"error": "Email certification code is incorrect"}, status_code=400)

        # 자동으로 시간 끝나면 삭제하게?
        delete_redis_code = await self.auth_redis_repository.delete_redis(email)
        if not delete_redis_code:
            return JSONResponse(content={"error": "Failed to delete email certification code"}, status_code=500)

        return True
    
    async def check_email_code_timeout(self, email: str):
        """
        check code timeout
        args:
            email: str
        """
        return await self.auth_redis_repository.check_timeout_redis(email)

    async def set_refresh_token(self, refresh_token: str, email: str, ex: int = 60*60*24*10):
        """
        set refresh token to redis
        args:
            user_id: int
            refresh_token: str
        """
        return await self.auth_redis_repository.set_redis(refresh_token, email, ex=60*60*24*10) # 10 days

    async def delete_refresh_token(self, refresh_token: str):
        """
        delete refresh token from redis
        args:
            refresh_token: str
        """
        return await self.auth_redis_repository.delete_redis(refresh_token)
    
    async def get_refresh_token(self, refresh_token: str):
        """
        get refresh token from redis
        args:
            refresh_token: str
        """
        return await self.auth_redis_repository.get_redis(refresh_token)