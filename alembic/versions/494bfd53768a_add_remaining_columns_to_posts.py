"""add remaining columns to posts

Revision ID: 494bfd53768a
Revises: 88c89a20fb87
Create Date: 2023-08-09 19:17:29.492755

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '494bfd53768a'
down_revision: Union[str, None] = '88c89a20fb87'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column("posts", sa.Column("published", sa.Boolean(), nullable=False, server_default="TRUE"),)
    op.add_column("posts", sa.Column("created_at", sa.TIMESTAMP(timezone=True), nullable=False, server_default=sa.text("NOW()")),)
    pass


def downgrade() -> None:
    op.drop_column("posts", "published")
    op.drop_column("posts", "created_at")
    pass
