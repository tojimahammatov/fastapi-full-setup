"""add content column to posts table

Revision ID: bc7d67e2317e
Revises: 522bbdb3c411
Create Date: 2023-08-09 19:02:00.719400

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'bc7d67e2317e'
down_revision: Union[str, None] = '522bbdb3c411'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column("posts", sa.Column("content", sa.String(), nullable=False))
    pass


def downgrade() -> None:
    op.drop_column("posts", "content")
    pass
