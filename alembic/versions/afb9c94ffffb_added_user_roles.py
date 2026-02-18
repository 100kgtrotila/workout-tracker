"""Added user roles

Revision ID: afb9c94ffffb
Revises: 7b399ebc26f7
Create Date: 2026-02-17 22:25:39.256590

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'afb9c94ffffb'
down_revision: Union[str, Sequence[str], None] = '7b399ebc26f7'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column("users", sa.Column("role", sa.String(length=20), nullable=True))

    op.execute("UPDATE users SET role = 'user'")

    op.alter_column("users", "role", nullable=False)


def downgrade() -> None:
    op.drop_column('users', 'role')
