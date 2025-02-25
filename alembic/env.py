from logging.config import fileConfig
from sqlalchemy import create_engine, pool
from alembic import context
import sys
import os



# Set up logging from alembic.ini
config = context.config
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Ensure the correct path to models.py is included
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

# Import Base from models.py
from app.models import Base  

# Metadata from SQLAlchemy models
target_metadata = Base.metadata


def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode."""
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """Run migrations in 'online' mode."""
    DATABASE_URL = config.get_main_option("sqlalchemy.url")  # Get DB URL from alembic.ini
    connectable = create_engine(DATABASE_URL, poolclass=pool.NullPool)

    with connectable.connect() as connection:
        context.configure(connection=connection, target_metadata=target_metadata)

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
