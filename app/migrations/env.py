from logging.config import fileConfig
from sqlalchemy.ext.asyncio import create_async_engine
from alembic import context
import os
import asyncio
from dotenv import load_dotenv
from models.shop_models import Model

load_dotenv()

config = context.config
config.set_main_option("sqlalchemy.url", os.getenv('DB_URL'))

if config.config_file_name is not None:
    fileConfig(config.config_file_name)

target_metadata = Model.metadata


async def run_migrations_online() -> None:
    """Запускаем миграции в 'online' режиме."""
    connectable = create_async_engine(
        config.get_main_option("sqlalchemy.url"),
        future=True,
        echo=True,
    )

    async with connectable.connect() as connection:
        await connection.run_sync(do_run_migrations)


def do_run_migrations(connection) -> None:
    """Выполняем миграции."""
    context.configure(
        connection=connection,
        target_metadata=target_metadata,
    )

    with connection.begin():
        context.run_migrations()


def run_migrations_offline() -> None:
    """Запускаем миграции в 'offline' режиме."""
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    asyncio.run(run_migrations_online())
