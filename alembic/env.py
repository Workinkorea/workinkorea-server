from app.database import Base
from logging.config import fileConfig

from sqlalchemy import engine_from_config
from sqlalchemy import pool

from alembic import context

from app.core.config import SETTINGS

# 모델 추가
from app.auth.models import *

# alembic 설정
config = context.config


# 데이터베이스 URL 설정
config.set_main_option("sqlalchemy.url", SETTINGS.DATABASE_SYNC_URL)


# 로깅 설정
if config.config_file_name is not None:
    fileConfig(config.config_file_name)


# 베이스 모델
target_metadata = Base.metadata


# alembic 기본설정
def run_migrations_offline() -> None:
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection, target_metadata=target_metadata
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
