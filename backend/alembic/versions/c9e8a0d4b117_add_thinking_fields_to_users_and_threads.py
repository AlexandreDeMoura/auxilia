"""add_thinking_fields_to_users_and_threads

Revision ID: c9e8a0d4b117
Revises: a57400e4fb11
Create Date: 2026-05-02 00:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "c9e8a0d4b117"
down_revision: Union[str, Sequence[str], None] = "a57400e4fb11"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column(
        "users",
        sa.Column(
            "thinking_controls_enabled",
            sa.Boolean(),
            server_default=sa.text("false"),
            nullable=False,
        ),
    )
    op.add_column("threads", sa.Column("thinking_enabled", sa.Boolean(), nullable=True))
    op.add_column("threads", sa.Column("thinking_effort", sa.String(), nullable=True))


def downgrade() -> None:
    op.drop_column("threads", "thinking_effort")
    op.drop_column("threads", "thinking_enabled")
    op.drop_column("users", "thinking_controls_enabled")
