"""change_user_role_from_enum_to_string

Revision ID: 9c60084e309c
Revises: b38bf7802471
Create Date: 2026-03-03 10:21:57.303416

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '9c60084e309c'
down_revision: Union[str, Sequence[str], None] = 'b38bf7802471'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema: change role from ENUM to VARCHAR."""
    # SQLite ne supporte pas ALTER COLUMN directement
    # On recrée la table avec le bon type
    with op.batch_alter_table('users') as batch_op:
        batch_op.alter_column(
            'role',
            existing_type=sa.String(),  # SQLite stocke tout en String de toute façon
            type_=sa.String(),
            nullable=False
        )


def downgrade() -> None:
    with op.batch_alter_table('users') as batch_op:
        batch_op.alter_column(
            'role',
            existing_type=sa.String(),
            type_=sa.String(),
            nullable=False
        )