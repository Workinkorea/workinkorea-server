import os
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy import MetaData, DateTime, create_engine
from sqlalchemy.orm import sessionmaker, Session, DeclarativeBase, Mapped, mapped_column
from datetime import datetime
from app.core.settings import SETTINGS

meta = MetaData()

db_schema = os.getenv("DB_SCHEMA", "public")

# search_path를 URL에 직접 추가
def get_async_url():
    base_url = SETTINGS.DATABASE_ASYNC_URL
    if db_schema != "public":
        return f"{base_url}?options=-csearch_path%3D{db_schema}"
    return base_url

def get_sync_url():
    base_url = SETTINGS.DATABASE_SYNC_URL
    if db_schema != "public":
        return f"{base_url}?options=-csearch_path%3D{db_schema}"
    return base_url

async_engine = create_async_engine(
    get_async_url(),
    echo=True,
    future=True,
)

async_session = async_sessionmaker(
    async_engine, expire_on_commit=False, class_=AsyncSession)

sync_engine = create_engine(
    get_sync_url(),
    echo=True,
    future=True,
)

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
            await session.commit()
        except Exception:
            await session.rollback()
            raise


# 베이스 모델
class Base(DeclarativeBase):
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=datetime.now(),
        nullable=False
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=datetime.now(),
        nullable=False
    )


# redis
import redis.asyncio as redis

async def get_redis_client() -> redis.Redis:
    async with redis.Redis(host=SETTINGS.REDIS_HOST, port=SETTINGS.REDIS_PORT, db=SETTINGS.REDIS_DB) as client:
        try:
            yield client
        except Exception as e:
            print(f"Redis connection error: {e}")
            raise ConnectionError(f"Failed to connect to Redis: {e}")