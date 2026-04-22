import asyncio
import logging
import sys
from pathlib import Path
from logging.config import fileConfig

from alembic import context
from sqlalchemy import pool
from sqlalchemy.ext.asyncio import create_async_engine

if sys.platform.startswith("win"):
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

# Add parent directory to path to resolve src module
sys.path.insert(0, str(Path(__file__).parent.parent.parent))
sys.path.insert(0, str(Path(__file__).parent.parent))

from core import settings
from infra.persist.base import Base
from infra.persist.models import *  # noqa: F403


config = context.config

# Логирование: работаем и без alembic.ini
cfg_file = config.config_file_name
if cfg_file and Path(cfg_file).exists():
    fileConfig(cfg_file)
else:
    logging.basicConfig(level=logging.INFO)

target_metadata = Base.metadata
print("Loaded tables:", list(target_metadata.tables.keys()))


def is_sqlite_url(url: str) -> bool:
    return url.startswith("sqlite")


def run_migrations_offline():
    """Offline режим — генерим SQL без подключения."""
    url = settings.database_url
    if not url:
        raise RuntimeError("DATABASE_URL was not found. Check .env")
    if is_sqlite_url(url):
        context.configure(
            url=url,  # offline ок и с async-схемой
            target_metadata=target_metadata,
            literal_binds=True,
            dialect_opts={"paramstyle": "named"},
            render_as_batch=True
        )
    else:
        context.configure(
            url=url,  # offline ок и с async-схемой
            target_metadata=target_metadata,
            literal_binds=True,
            dialect_opts={"paramstyle": "named"}
        )
    with context.begin_transaction():
        context.run_migrations()


def do_run_migrations(connection):
    """Синхронная часть, которую Alembic ожидает внутри run_sync()."""
    if is_sqlite_url(str(connection.engine.url)):
        context.configure(connection=connection, target_metadata=target_metadata, render_as_batch=True)
    else:
        context.configure(connection=connection, target_metadata=target_metadata)
    with context.begin_transaction():
        context.run_migrations()


async def run_migrations_online():
    """Online режим — асинхронное подключение к БД."""
    url = settings.database_url
    if not url:
        raise RuntimeError("DATABASE_URL was not found. Check .env")

    engine = create_async_engine(url, poolclass=pool.NullPool, future=True)

    async with engine.connect() as conn:
        # ВАЖНО: прогоняем синхронные миграции внутри async-коннекта
        await conn.run_sync(do_run_migrations)

    await engine.dispose()


if context.is_offline_mode():
    run_migrations_offline()
else:
    asyncio.run(run_migrations_online())
