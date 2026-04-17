"""add_password_to_users_and_user_id_to_diagnosis_answers

Revision ID: 43fb6d20bdd9
Revises: 74bb0a42d89e
Create Date: 2026-04-17 16:51:59.287533

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '43fb6d20bdd9'
down_revision: Union[str, Sequence[str], None] = '74bb0a42d89e'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('users', sa.Column('password', sa.String(), nullable=True))
    op.add_column('diagnosis_answers', sa.Column('user_id', sa.Integer(), nullable=True))
    op.create_index(op.f('ix_diagnosis_answers_user_id'), 'diagnosis_answers', ['user_id'], unique=False)
    op.create_foreign_key(None, 'diagnosis_answers', 'users', ['user_id'], ['id'])


def downgrade() -> None:
    op.drop_constraint(None, 'diagnosis_answers', type_='foreignkey')
    op.drop_index(op.f('ix_diagnosis_answers_user_id'), table_name='diagnosis_answers')
    op.drop_column('diagnosis_answers', 'user_id')
    op.drop_column('users', 'password')
