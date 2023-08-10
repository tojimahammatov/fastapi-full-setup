"""add user table

Revision ID: 953b3657252f
Revises: bc7d67e2317e
Create Date: 2023-08-09 19:07:43.086392

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '953b3657252f'
down_revision: Union[str, None] = 'bc7d67e2317e'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table("users", sa.Column("id", sa.Integer(), primary_key=True),
                    sa.Column("email", sa.String(), nullable=False),
                    sa.Column("password", sa.String(), nullable=False),
                    sa.Column("created_at", sa.TIMESTAMP(timezone=True), 
                              server_default=sa.text("NOW()"), nullable=False),
                    sa.PrimaryKeyConstraint("id"),
                    sa.UniqueConstraint("email")
                    )
    pass


def downgrade() -> None:
    op.drop_table("users")
    pass
