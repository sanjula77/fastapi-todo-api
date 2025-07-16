"""add last few column to posts table

Revision ID: 783912a00edd
Revises: 17851ab7905a
Create Date: 2025-07-10 20:20:48.120776

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '783912a00edd'
down_revision: Union[str, Sequence[str], None] = '17851ab7905a'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column(
        'posts',
        sa.Column('published', sa.Boolean(), nullable=False, server_default=sa.text('TRUE')))
    op.add_column(
        'posts',
        sa.Column('created_at', sa.DateTime(), nullable=False, server_default=sa.func.now()))
    pass


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column('posts', 'published')
    op.drop_column('posts', 'created_at')
    pass
