"""add foreign-key to posts table

Revision ID: 17851ab7905a
Revises: 117e5a04f798
Create Date: 2025-07-10 19:35:48.082708

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '17851ab7905a'
down_revision: Union[str, Sequence[str], None] = '117e5a04f798'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column(
        'posts',
        sa.Column('user_id', sa.Integer(), nullable=True)
    )
    op.create_foreign_key(
        'fk_posts_user_id',
        'posts',
        'user',
        ['user_id'],
        ['id'],
        ondelete='CASCADE'
    )
    pass


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_constraint('fk_posts_user_id', 'posts', type_='foreignkey')
    op.drop_column('posts', 'user_id')
    pass
