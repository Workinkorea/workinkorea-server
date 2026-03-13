import os
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy import MetaData, DateTime, event, create_engine, text
from sqlalchemy.orm import sessionmaker, Session, DeclarativeBase, Mapped, mapped_column
from datetime import datetime
from app.core.settings import SETTINGS

meta = MetaData()

db_schema = os.getenv("DB_SCHEMA", "public")

async_engine = create_async_engine(
    SETTINGS.DATABASE_ASYNC_URL,
    echo=True,
    future=True,
)

# 비동기 엔진 연결 시 search_path 설정
@event.listens_for(async_engine.sync_engine, "connect")
def set_search_path_async(dbapi_connection, connection_record):
    cursor = dbapi_connection.cursor()
    cursor.execute(f"SET search_path TO {db_schema}")
    cursor.close()

async_session = async_sessionmaker(
    async_engine, expire_on_commit=False, class_=AsyncSession)

sync_engine = create_engine(
    SETTINGS.DATABASE_SYNC_URL,
    echo=True,
    future=True,
)

# 동기 엔진 연결 시 search_path 설정
@event.listens_for(sync_engine, "connect")
def set_search_path_sync(dbapi_connection, connection_record):
    cursor = dbapi_connection.cursor()
    cursor.execute(f"SET search_path TO {db_schema}")
    cursor.close()

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