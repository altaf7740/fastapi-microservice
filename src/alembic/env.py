# src/alembic/env.py
from __future__ import annotations

import asyncio
import os
from logging.config import fileConfig

from sqlalchemy import pool
from sqlalchemy.engine import Connection
from sqlalchemy.ext.asyncio import AsyncEngine, create_async_engine

from alembic import context
from core.config.database import Base  # your declarative Base

# Alembic config
config = context.config

# Logging
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Pull DB URL from environment; fall back to ini if missing
db_url = os.getenv("APP_DATABASE_URL")
if db_url:
    config.set_main_option("sqlalchemy.url", db_url)

# Metadata for autogenerate
target_metadata = Base.metadata


def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode."""
    url = config.get_main_option("sqlalchemy.url")
    if not url:
        raise RuntimeError("sqlalchemy.url is not set. Ensure APP_DATABASE_URL or alembic.ini provides it.")

    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
        compare_type=True,
        compare_server_default=True,
    )
    with context.begin_transaction():
        context.run_migrations()


def _run_sync_migrations(connection: Connection) -> None:
    """Run migrations given a sync Connection (inside async run_sync)."""
    context.configure(
        connection=connection,
        target_metadata=target_metadata,
        compare_type=True,
        compare_server_default=True,
    )
    with context.begin_transaction():
        context.run_migrations()


async def run_migrations_online() -> None:
    """Run migrations in 'online' mode using an async engine."""
    url = config.get_main_option("sqlalchemy.url")
    if not url:
        raise RuntimeError("sqlalchemy.url is not set. Ensure APP_DATABASE_URL or alembic.ini provides it.")

    connectable: AsyncEngine = create_async_engine(url, poolclass=pool.NullPool)

    async with connectable.connect() as async_conn:
        await async_conn.run_sync(_run_sync_migrations)

    await connectable.dispose()


if context.is_offline_mode():
    run_migrations_offline()
else:
    asyncio.run(run_migrations_online())
