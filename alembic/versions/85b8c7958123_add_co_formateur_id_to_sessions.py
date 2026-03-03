"""add co_formateur_id to sessions

Revision ID: 85b8c7958123
Revises: b38bf7802471
Create Date: 2026-03-03 02:14:40.093091

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "85b8c7958123"
down_revision: Union[str, Sequence[str], None] = "b38bf7802471"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Add co_formateur_id column to sessions
    with op.batch_alter_table("sessions") as batch_op:
        batch_op.add_column(
            sa.Column(
                "co_formateur_id",
                sa.Integer(),
                nullable=True,
            )
        )
        batch_op.create_foreign_key(
            "fk_sessions_co_formateur",
            "users",
            ["co_formateur_id"],
            ["id"],
            ondelete="CASCADE",
        )


def downgrade() -> None:
    with op.batch_alter_table("sessions") as batch_op:
        batch_op.drop_column("co_formateur_id")
