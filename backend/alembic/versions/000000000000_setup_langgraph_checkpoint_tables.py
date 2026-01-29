"""setup_langgraph_checkpoint_tables

Revision ID: 000000000000
Revises:
Create Date: 2025-12-02 00:00:00.000000

This migration sets up the LangGraph checkpoint tables required by
langgraph-checkpoint-postgres. It must run before all other migrations.

See: https://pypi.org/project/langgraph-checkpoint-postgres/
"""

from typing import Sequence, Union

from alembic import op


# revision identifiers, used by Alembic.
revision: str = "000000000000"
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Set up LangGraph checkpoint tables using the library's setup method."""
    import os
    from langgraph.checkpoint.postgres import PostgresSaver

    # Get database URL from environment (more reliable than extracting from connection)
    # Fall back to alembic config if not set
    db_url = os.environ.get("DATABASE_URL")
    if not db_url:
        from alembic import context
        db_url = context.config.get_main_option("sqlalchemy.url")

    # Convert SQLAlchemy URL to psycopg format
    # postgresql+psycopg://user:pass@host:port/db -> postgresql://user:pass@host:port/db
    if db_url and "+psycopg" in db_url:
        db_url = db_url.replace("+psycopg", "")

    # PostgresSaver.from_conn_string handles connection setup properly
    with PostgresSaver.from_conn_string(db_url) as checkpointer:
        checkpointer.setup()


def downgrade() -> None:
    """Drop LangGraph checkpoint tables.

    Note: The checkpoint tables store conversation state. Dropping them
    will permanently delete all checkpoint data.
    """
    # Drop tables created by langgraph-checkpoint-postgres
    # These are the tables created by the setup() method
    op.execute("DROP TABLE IF EXISTS checkpoint_writes CASCADE")
    op.execute("DROP TABLE IF EXISTS checkpoint_blobs CASCADE")
    op.execute("DROP TABLE IF EXISTS checkpoints CASCADE")
    op.execute("DROP TABLE IF EXISTS checkpoint_migrations CASCADE")
