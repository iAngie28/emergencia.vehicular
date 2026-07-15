"""Allow one reporte per incident target type

Revision ID: f3a2b6c9d4e1
Revises: c7e4a9b2f610
Create Date: 2026-07-15 00:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "f3a2b6c9d4e1"
down_revision: Union[str, Sequence[str], None] = "c7e4a9b2f610"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


NEW_UNIQUE = "uq_reporte_incidente_tipo"
INCIDENTE_INDEX = "ix_reporte_incidente_id"


def _create_reporte_table() -> None:
    op.create_table(
        "reporte",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("usuario_id", sa.Integer(), nullable=False),
        sa.Column("incidente_id", sa.Integer(), nullable=False),
        sa.Column("taller_id", sa.Integer(), nullable=False),
        sa.Column("tecnico_id", sa.Integer(), nullable=True),
        sa.Column("tipo_reporte", sa.String(length=20), nullable=False),
        sa.Column("motivo", sa.String(length=150), nullable=False),
        sa.Column("descripcion", sa.Text(), nullable=False),
        sa.Column("estado", sa.String(length=20), nullable=True),
        sa.Column("respuesta", sa.Text(), nullable=True),
        sa.Column("fecha_creacion", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=True),
        sa.Column("fecha_resolucion", sa.DateTime(timezone=True), nullable=True),
        sa.ForeignKeyConstraint(["incidente_id"], ["incidente.id"], ondelete="RESTRICT"),
        sa.ForeignKeyConstraint(["taller_id"], ["taller.id"], ondelete="RESTRICT"),
        sa.ForeignKeyConstraint(["tecnico_id"], ["usuario.id"], ondelete="SET NULL"),
        sa.ForeignKeyConstraint(["usuario_id"], ["usuario.id"], ondelete="RESTRICT"),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("incidente_id", "tipo_reporte", name=NEW_UNIQUE),
    )
    _create_reporte_indexes()


def _create_reporte_indexes() -> None:
    op.create_index(op.f("ix_reporte_id"), "reporte", ["id"], unique=False)
    op.create_index(op.f("ix_reporte_usuario_id"), "reporte", ["usuario_id"], unique=False)
    op.create_index(op.f(INCIDENTE_INDEX), "reporte", ["incidente_id"], unique=False)
    op.create_index(op.f("ix_reporte_taller_id"), "reporte", ["taller_id"], unique=False)
    op.create_index(op.f("ix_reporte_tecnico_id"), "reporte", ["tecnico_id"], unique=False)


def _columns_match(index_or_constraint: dict, columns: list[str]) -> bool:
    return list(index_or_constraint.get("column_names") or []) == columns


def _drop_unique_incidente_only(inspector: sa.Inspector) -> bool:
    dropped_incidente_index = False

    for constraint in inspector.get_unique_constraints("reporte"):
        name = constraint.get("name")
        if name and _columns_match(constraint, ["incidente_id"]):
            op.drop_constraint(name, "reporte", type_="unique")

    for index in inspector.get_indexes("reporte"):
        name = index.get("name")
        if name and index.get("unique") and _columns_match(index, ["incidente_id"]):
            op.drop_index(name, table_name="reporte")
            dropped_incidente_index = name == INCIDENTE_INDEX

    return dropped_incidente_index


def _has_unique(inspector: sa.Inspector, name: str) -> bool:
    return any(constraint.get("name") == name for constraint in inspector.get_unique_constraints("reporte"))


def _has_nonunique_incidente_index(inspector: sa.Inspector) -> bool:
    return any(
        not index.get("unique")
        and index.get("name") == INCIDENTE_INDEX
        and _columns_match(index, ["incidente_id"])
        for index in inspector.get_indexes("reporte")
    )


def _sqlite_recreate_reporte(unique_sql: str) -> None:
    bind = op.get_bind()
    bind.exec_driver_sql("PRAGMA foreign_keys=OFF")
    try:
        op.execute("ALTER TABLE reporte RENAME TO reporte_old")
        op.execute(
            f"""
            CREATE TABLE reporte (
                id INTEGER NOT NULL,
                usuario_id INTEGER NOT NULL,
                incidente_id INTEGER NOT NULL,
                taller_id INTEGER NOT NULL,
                tecnico_id INTEGER,
                tipo_reporte VARCHAR(20) NOT NULL,
                motivo VARCHAR(150) NOT NULL,
                descripcion TEXT NOT NULL,
                estado VARCHAR(20),
                respuesta TEXT,
                fecha_creacion DATETIME DEFAULT CURRENT_TIMESTAMP,
                fecha_resolucion DATETIME,
                PRIMARY KEY (id),
                FOREIGN KEY(incidente_id) REFERENCES incidente (id) ON DELETE RESTRICT,
                FOREIGN KEY(taller_id) REFERENCES taller (id) ON DELETE RESTRICT,
                FOREIGN KEY(tecnico_id) REFERENCES usuario (id) ON DELETE SET NULL,
                FOREIGN KEY(usuario_id) REFERENCES usuario (id) ON DELETE RESTRICT,
                {unique_sql}
            )
            """
        )
        op.execute(
            """
            INSERT INTO reporte (
                id, usuario_id, incidente_id, taller_id, tecnico_id, tipo_reporte,
                motivo, descripcion, estado, respuesta, fecha_creacion, fecha_resolucion
            )
            SELECT
                id, usuario_id, incidente_id, taller_id, tecnico_id, tipo_reporte,
                motivo, descripcion, estado, respuesta, fecha_creacion, fecha_resolucion
            FROM reporte_old
            """
        )
        op.execute("DROP TABLE reporte_old")
        _create_reporte_indexes()
    finally:
        bind.exec_driver_sql("PRAGMA foreign_keys=ON")


def upgrade() -> None:
    bind = op.get_bind()
    inspector = sa.inspect(bind)

    if not inspector.has_table("reporte"):
        _create_reporte_table()
        return

    if bind.dialect.name == "sqlite":
        _sqlite_recreate_reporte(f"CONSTRAINT {NEW_UNIQUE} UNIQUE (incidente_id, tipo_reporte)")
        return

    _drop_unique_incidente_only(inspector)
    if not _has_nonunique_incidente_index(inspector):
        op.create_index(op.f(INCIDENTE_INDEX), "reporte", ["incidente_id"], unique=False)

    inspector = sa.inspect(bind)
    if not _has_unique(inspector, NEW_UNIQUE):
        op.create_unique_constraint(NEW_UNIQUE, "reporte", ["incidente_id", "tipo_reporte"])


def downgrade() -> None:
    bind = op.get_bind()
    inspector = sa.inspect(bind)

    if not inspector.has_table("reporte"):
        return

    duplicates = bind.execute(
        sa.text(
            """
            SELECT incidente_id
            FROM reporte
            GROUP BY incidente_id
            HAVING COUNT(*) > 1
            """
        )
    ).fetchall()
    if duplicates:
        raise RuntimeError("Cannot downgrade reporte uniqueness while an incident has multiple reportes.")

    if bind.dialect.name == "sqlite":
        _sqlite_recreate_reporte("UNIQUE (incidente_id)")
        return

    if _has_unique(inspector, NEW_UNIQUE):
        op.drop_constraint(NEW_UNIQUE, "reporte", type_="unique")

    for index in inspector.get_indexes("reporte"):
        name = index.get("name")
        if name == INCIDENTE_INDEX and not index.get("unique") and _columns_match(index, ["incidente_id"]):
            op.drop_index(name, table_name="reporte")

    op.create_index(op.f(INCIDENTE_INDEX), "reporte", ["incidente_id"], unique=True)
