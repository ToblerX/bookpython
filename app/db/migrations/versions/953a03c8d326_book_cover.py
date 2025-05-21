"""book cover

Revision ID: 953a03c8d326
Revises: 6eae1930cafb
Create Date: 2025-05-09 20:42:41.270535

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '953a03c8d326'
down_revision: Union[str, None] = '6eae1930cafb'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
