from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy import MetaData, DateTime, func, create_engine
from sqlalchemy.orm import sessionmaker, Session, DeclarativeBase, Mapped, mapped_column
from datetime import datetime
from app.core.settings import SETTINGS

meta = MetaData()
async_engine = create_async_engine(SETTINGS.DATABASE_ASYNC_URL, echo=True, future=True)
async_session = async_sessionmaker(
    async_engine, expire_on_commit=False, class_=AsyncSession)


sync_engine = create_engine(SETTINGS.DATABASE_SYNC_URL, echo=True, future=True)
sync_session = sessionmaker(
    sync_engine, expire_on_commit=False, class_=Session)

# 동기 세션(alembic 사용용)
def get_sync_session() -> Session:
    with sync_session() as session:
        try:
            yield session
            session.commit()
        except Exception:
            session.rollback()
            raise

# 비동기 세션
async def get_async_session() -> AsyncSession:
    async with async_session() as session:
        try:
            yield session
            await session.commit() # 세션이 종료될 때 자동으로 커밋됨
        except Exception:
            await session.rollback() # 문제가 발생하면 자동으로 롤백됨
            raise


# 베이스 모델
class Base(DeclarativeBase):
    created_at : Mapped[datetime] = mapped_column(
        DateTime(timezone=True), 
        default=datetime.now(),
        nullable=False
        )

    updated_at : Mapped[datetime] = mapped_column(
        DateTime(timezone=True), 
        default=datetime.now(),
        nullable=False
        )


# redis 
import redis.asyncio as redis

async def redis_client() -> redis.Redis:
    try:
        return await redis.Redis(host=SETTINGS.REDIS_HOST, port=SETTINGS.REDIS_PORT, db=SETTINGS.REDIS_DB)
    except Exception as e:
        print(f"Redis connection error: {e}")
        raise ConnectionError(f"Failed to connect to Redis: {e}")