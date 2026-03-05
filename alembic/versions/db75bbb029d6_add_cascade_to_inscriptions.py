"""add_cascade_to_inscriptions

Revision ID: db75bbb029d6
Revises: d10f6ace258c
Create Date: 2026-03-04 23:39:06.920292

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'db75bbb029d6'
down_revision: Union[str, Sequence[str], None] = 'd10f6ace258c'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema - SQLite: recréer la table avec CASCADE"""
    
    # 1. Renommer l'ancienne table
    op.rename_table('inscriptions', 'inscriptions_old')
    
    # 2. Recréer la table avec les bonnes contraintes FK
    op.create_table(
        'inscriptions',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('session_id', sa.Integer(), nullable=False),
        sa.Column('statut', sa.String(), nullable=False),
        sa.Column('date_inscription', sa.DateTime(), nullable=True),
        sa.Column('created_at', sa.DateTime(), server_default=sa.text('(CURRENT_TIMESTAMP)'), nullable=False),
        sa.Column('updated_at', sa.DateTime(), server_default=sa.text('(CURRENT_TIMESTAMP)'), nullable=False),
        
        # ✅ FK avec CASCADE pour user_id ET session_id
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['session_id'], ['sessions.id'], ondelete='CASCADE'),
        
        sa.PrimaryKeyConstraint('id')
    )
    
    # 3. Copier les données existantes
    op.execute("""
        INSERT INTO inscriptions (id, user_id, session_id, statut, date_inscription, created_at, updated_at)
        SELECT id, user_id, session_id, statut, date_inscription, created_at, updated_at
        FROM inscriptions_old
    """)
    
    # 4. Supprimer l'ancienne table
    op.drop_table('inscriptions_old')
    
    # 5. Recréer les index
    op.create_index(op.f('ix_inscriptions_id'), 'inscriptions', ['id'], unique=False)
    op.create_index(op.f('ix_inscriptions_user_id'), 'inscriptions', ['user_id'], unique=False)
    op.create_index(op.f('ix_inscriptions_session_id'), 'inscriptions', ['session_id'], unique=False)


def downgrade() -> None:
    """Downgrade schema - SQLite: retour sans CASCADE"""
    
    # 1. Renommer la table actuelle
    op.rename_table('inscriptions', 'inscriptions_new')
    
    # 2. Recréer la table SANS CASCADE (état précédent)
    op.create_table(
        'inscriptions',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('session_id', sa.Integer(), nullable=False),
        sa.Column('statut', sa.String(), nullable=False),
        sa.Column('date_inscription', sa.DateTime(), nullable=True),
        sa.Column('created_at', sa.DateTime(), server_default=sa.text('(CURRENT_TIMESTAMP)'), nullable=False),
        sa.Column('updated_at', sa.DateTime(), server_default=sa.text('(CURRENT_TIMESTAMP)'), nullable=False),
        
        # ❌ FK sans CASCADE (état avant migration)
        sa.ForeignKeyConstraint(['user_id'], ['users.id']),
        sa.ForeignKeyConstraint(['session_id'], ['sessions.id']),
        
        sa.PrimaryKeyConstraint('id')
    )
    
    # 3. Copier les données
    op.execute("""
        INSERT INTO inscriptions (id, user_id, session_id, statut, date_inscription, created_at, updated_at)
        SELECT id, user_id, session_id, statut, date_inscription, created_at, updated_at
        FROM inscriptions_new
    """)
    
    # 4. Supprimer la table temporaire
    op.drop_table('inscriptions_new')
    
    # 5. Recréer les index
    op.create_index(op.f('ix_inscriptions_id'), 'inscriptions', ['id'], unique=False)
    op.create_index(op.f('ix_inscriptions_user_id'), 'inscriptions', ['user_id'], unique=False)
    op.create_index(op.f('ix_inscriptions_session_id'), 'inscriptions', ['session_id'], unique=False)