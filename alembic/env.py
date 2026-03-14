from app.database import Base
from logging.config import fileConfig

from sqlalchemy import create_engine
from sqlalchemy import pool

from alembic import context

from app.core.settings import SETTINGS

import os

# 모델 추가
from app.auth.models import *
from app.profile.models.profile import *
from app.profile.models.contact import *
from app.profile.models.position import *
from app.profile.models.country import *
from app.profile.models.account_config import *
from app.profile.models.company_profile import *
from app.posts.models.company_post import *

from app.posts.models.resume import *
from app.posts.models.language_skill import *
from app.posts.models.school import *
from app.posts.models.career_history import *
from app.posts.models.introduction import *
from app.posts.models.license import *

from app.admin.models.notice import *

from app.diagnosis.models.diagnosis_answer import *

# alembic 설정
config = context.config

# 로깅 설정
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# 베이스 모델
target_metadata = Base.metadata

# dev 스키마 설정
db_schema = os.getenv("DB_SCHEMA", "public")


def run_migrations_offline() -> None:
    url = SETTINGS.DATABASE_SYNC_URL
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
        include_schemas=True,
        version_table_schema=db_schema,
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    engine = create_engine(
        SETTINGS.DATABASE_SYNC_URL,
        poolclass=pool.NullPool,
        connect_args={"options": f"-csearch_path={db_schema}"},
    )

    with engine.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
            include_schemas=True,
            version_table_schema=db_schema,
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()