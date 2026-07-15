"""Add taller filter metadata

Revision ID: e8c4d1f7a9b2
Revises: f3a2b6c9d4e1
Create Date: 2026-07-15 00:10:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "e8c4d1f7a9b2"
down_revision: Union[str, Sequence[str], None] = "f3a2b6c9d4e1"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def _has_column(table_name: str, column_name: str) -> bool:
    inspector = sa.inspect(op.get_bind())
    return any(column["name"] == column_name for column in inspector.get_columns(table_name))


def upgrade() -> None:
    if not _has_column("taller", "ciudad"):
        op.add_column("taller", sa.Column("ciudad", sa.String(length=100), nullable=True))

    if not _has_column("taller", "fecha_creacion"):
        op.add_column(
            "taller",
            sa.Column("fecha_creacion", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=True),
        )


def downgrade() -> None:
    if _has_column("taller", "fecha_creacion"):
        op.drop_column("taller", "fecha_creacion")

    if _has_column("taller", "ciudad"):
        op.drop_column("taller", "ciudad")
