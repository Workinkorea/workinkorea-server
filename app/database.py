import os
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy import MetaData, DateTime, func, create_engine
from sqlalchemy.orm import sessionmaker, Session, DeclarativeBase, Mapped, mapped_column
from datetime import datetime
from app.core.settings import SETTINGS

meta = MetaData()

# dev 환경에서만 search_path 설정
db_schema = os.getenv("DB_SCHEMA", "public")
connect_args = {"server_settings": {"search_path": db_schema}} if db_schema != "public" else {}

async_engine = create_async_engine(
    SETTINGS.DATABASE_ASYNC_URL,
    echo=True,
    future=True,
    connect_args=connect_args
)
async_session = async_sessionmaker(
    async_engine, expire_on_commit=False, class_=AsyncSession)

sync_engine = create_engine(
    SETTINGS.DATABASE_SYNC_URL,
    echo=True,
    future=True,
    connect_args=connect_args
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