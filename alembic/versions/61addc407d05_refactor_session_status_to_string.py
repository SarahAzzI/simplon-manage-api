"""refactor session status to string

Revision ID: 61addc407d05
Revises: 9c60084e309c
Create Date: 2026-03-03 21:49:13.498624

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '61addc407d05'
down_revision: Union[str, Sequence[str], None] = '9c60084e309c'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema: change statut from Enum to String."""
    with op.batch_alter_table('sessions') as batch_op:
        batch_op.alter_column(
            'statut',
            existing_type=sa.Enum('PLANIFIEE', 'EN_COURS', 'TERMINEE', 'ANNULEE', name='sessionstatus'),
            type_=sa.String(),
            nullable=False
        )
    
    # Conversion des données : on passe des anciennes clés Enum (Français) aux nouvelles valeurs String (Français)
    # Note : On utilise les clés Françaises dans le WHERE car c'est ce qui est actuellement stocké en base.
    op.execute("UPDATE sessions SET statut = 'planifiée' WHERE statut = 'PLANIFIEE'")
    op.execute("UPDATE sessions SET statut = 'en_cours' WHERE statut = 'EN_COURS'")
    op.execute("UPDATE sessions SET statut = 'terminée' WHERE statut = 'TERMINEE'")
    op.execute("UPDATE sessions SET statut = 'annulée' WHERE statut = 'ANNULEE'")


def downgrade() -> None:
    """Downgrade schema."""
    with op.batch_alter_table('sessions') as batch_op:
        batch_op.alter_column(
            'statut',
            existing_type=sa.String(),
            type_=sa.Enum('PLANIFIEE', 'EN_COURS', 'TERMINEE', 'ANNULEE', name='sessionstatus'),
            nullable=False
        )
