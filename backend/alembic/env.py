from logging.config import fileConfig
from sqlalchemy import engine_from_config, pool
from alembic import context

from sqlmodel import SQLModel
from app.db.models import User  # import all SQLModels so metadata is complete
from app.db.models import *     # import any additional models including Profile
from app.db.engine import engine  # your actual engine

config = context.config

fileConfig(config.config_file_name)

# IMPORTANT: Use SQLModel metadata
target_metadata = SQLModel.metadata


def run_migrations_offline():
    url = engine.url.render_as_string(hide_password=False)
    print(url)
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        compare_type=True,  # detect column type changes
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online():
    connectable = engine_from_config(
        config.get_section(config.config_ini_section),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
        future=True,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
            compare_type=True,
            compare_server_default=True,
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
