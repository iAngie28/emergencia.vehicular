"""Add taller inhabilitacion metadata

Revision ID: a7d9e2c4b6f8
Revises: e8c4d1f7a9b2
Create Date: 2026-07-15 00:20:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "a7d9e2c4b6f8"
down_revision: Union[str, Sequence[str], None] = "e8c4d1f7a9b2"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def _has_column(table_name: str, column_name: str) -> bool:
    inspector = sa.inspect(op.get_bind())
    return any(column["name"] == column_name for column in inspector.get_columns(table_name))


def upgrade() -> None:
    if not _has_column("taller", "tipo_inhabilitacion"):
        op.add_column("taller", sa.Column("tipo_inhabilitacion", sa.String(length=20), nullable=True))

    if not _has_column("taller", "motivo_inhabilitacion"):
        op.add_column("taller", sa.Column("motivo_inhabilitacion", sa.String(length=500), nullable=True))

    if not _has_column("taller", "fecha_inhabilitacion"):
        op.add_column("taller", sa.Column("fecha_inhabilitacion", sa.DateTime(timezone=True), nullable=True))

    if not _has_column("taller", "inhabilitado_por_usuario_id"):
        op.add_column("taller", sa.Column("inhabilitado_por_usuario_id", sa.Integer(), nullable=True))


def downgrade() -> None:
    for column_name in (
        "inhabilitado_por_usuario_id",
        "fecha_inhabilitacion",
        "motivo_inhabilitacion",
        "tipo_inhabilitacion",
    ):
        if _has_column("taller", column_name):
            op.drop_column("taller", column_name)
