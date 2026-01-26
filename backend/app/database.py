from contextlib import asynccontextmanager

from langgraph.checkpoint.postgres.aio import AsyncPostgresSaver
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

from app.settings import app_settings

engine = create_async_engine(
    app_settings.database_url,
    pool_pre_ping=True,
    future=True,
)

AsyncSessionLocal = sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
)


async def get_db() -> AsyncSession:
    async with AsyncSessionLocal() as session:
        yield session


@asynccontextmanager
async def get_checkpointer():
    # AsyncPostgresSaver expects a native psycopg3 connection string (postgresql://)
    # not the SQLAlchemy dialect URL (postgresql+psycopg://)
    conn_string = app_settings.database_url.replace("postgresql+psycopg://", "postgresql://")
    async with AsyncPostgresSaver.from_conn_string(conn_string) as checkpointer:
        yield checkpointer
