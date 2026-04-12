"""fix: add ondelete CASCADE to foreign keys

Revision ID: 74bb0a42d89e
Revises: f6379ed575e3
Create Date: 2026-04-11

"""
from typing import Sequence, Union

from alembic import op


# revision identifiers, used by Alembic.
revision: str = '74bb0a42d89e'
down_revision: Union[str, None] = 'f6379ed575e3'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # resumes.user_id -> CASCADE
    op.drop_constraint('resumes_user_id_fkey', 'resumes', type_='foreignkey')
    op.create_foreign_key('resumes_user_id_fkey', 'resumes', 'users', ['user_id'], ['id'], ondelete='CASCADE')

    # schools.resume_id -> CASCADE
    op.drop_constraint('schools_resume_id_fkey', 'schools', type_='foreignkey')
    op.create_foreign_key('schools_resume_id_fkey', 'schools', 'resumes', ['resume_id'], ['id'], ondelete='CASCADE')

    # career_history.resume_id -> CASCADE
    op.drop_constraint('career_history_resume_id_fkey', 'career_history', type_='foreignkey')
    op.create_foreign_key('career_history_resume_id_fkey', 'career_history', 'resumes', ['resume_id'], ['id'], ondelete='CASCADE')

    # licenses.resume_id -> CASCADE
    op.drop_constraint('licenses_resume_id_fkey', 'licenses', type_='foreignkey')
    op.create_foreign_key('licenses_resume_id_fkey', 'licenses', 'resumes', ['resume_id'], ['id'], ondelete='CASCADE')

    # introduction.resume_id -> CASCADE
    op.drop_constraint('introduction_resume_id_fkey', 'introduction', type_='foreignkey')
    op.create_foreign_key('introduction_resume_id_fkey', 'introduction', 'resumes', ['resume_id'], ['id'], ondelete='CASCADE')

    # language_skills.resume_id -> CASCADE
    op.drop_constraint('language_skills_resume_id_fkey', 'language_skills', type_='foreignkey')
    op.create_foreign_key('language_skills_resume_id_fkey', 'language_skills', 'resumes', ['resume_id'], ['id'], ondelete='CASCADE')

    # notices.author_id -> SET NULL
    op.drop_constraint('notices_author_id_fkey', 'notices', type_='foreignkey')
    op.create_foreign_key('notices_author_id_fkey', 'notices', 'users', ['author_id'], ['id'], ondelete='SET NULL')


def downgrade() -> None:
    # revert all to no ondelete action
    op.drop_constraint('resumes_user_id_fkey', 'resumes', type_='foreignkey')
    op.create_foreign_key('resumes_user_id_fkey', 'resumes', 'users', ['user_id'], ['id'])

    op.drop_constraint('schools_resume_id_fkey', 'schools', type_='foreignkey')
    op.create_foreign_key('schools_resume_id_fkey', 'schools', 'resumes', ['resume_id'], ['id'])

    op.drop_constraint('career_history_resume_id_fkey', 'career_history', type_='foreignkey')
    op.create_foreign_key('career_history_resume_id_fkey', 'career_history', 'resumes', ['resume_id'], ['id'])

    op.drop_constraint('licenses_resume_id_fkey', 'licenses', type_='foreignkey')
    op.create_foreign_key('licenses_resume_id_fkey', 'licenses', 'resumes', ['resume_id'], ['id'])

    op.drop_constraint('introduction_resume_id_fkey', 'introduction', type_='foreignkey')
    op.create_foreign_key('introduction_resume_id_fkey', 'introduction', 'resumes', ['resume_id'], ['id'])

    op.drop_constraint('language_skills_resume_id_fkey', 'language_skills', type_='foreignkey')
    op.create_foreign_key('language_skills_resume_id_fkey', 'language_skills', 'resumes', ['resume_id'], ['id'])

    op.drop_constraint('notices_author_id_fkey', 'notices', type_='foreignkey')
    op.create_foreign_key('notices_author_id_fkey', 'notices', 'users', ['author_id'], ['id'])
