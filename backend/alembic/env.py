from logging.config import fileConfig
import os

from sqlalchemy import engine_from_config
from sqlalchemy import pool

from alembic import context

from app.models.base import Base  # Import the new Base
from app.models import *  # Import all new models

# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config

# Interpret the config file for Python logging.
# This line sets up loggers basically.
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# add your model's MetaData object here
# for 'autogenerate' support
# from myapp import mymodel
# target_metadata = mymodel.Base.metadata
target_metadata = Base.metadata

# Configuración dinámica de URL de base de datos según entorno
def get_database_url():
    """Obtiene la URL de base de datos según el entorno"""
    environment = os.getenv("ENVIRONMENT", "development")
    
    if environment == "test":
        # URL para base de datos de testing
        return os.getenv(
            "TEST_DATABASE_URL", 
            "postgresql://viejos_trapos_user:viejos_trapos_pass@postgres_test:5432/viejos_trapos_test_db"
        )
    else:
        # URL para base de datos de desarrollo
        return os.getenv(
            "DATABASE_URL", 
            "postgresql://viejos_trapos_user:viejos_trapos_pass@postgres:5432/viejos_trapos_db"
        )

# Override sqlalchemy.url with environment-specific URL
config.set_main_option("sqlalchemy.url", get_database_url())

# other values from the config, defined by the needs of env.py,
# can be acquired:
# my_important_option = config.get_main_option("my_important_option")
# ... etc.


def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode.

    This configures the context with just a URL
    and not an Engine, though an Engine is acceptable
    here as well.  By skipping the Engine creation
    we don't even need a DBAPI to be available.

    Calls to context.execute() here emit the given string to the
    script output.

    """
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
    """Run migrations in 'online' mode.

    In this scenario we need to create an Engine
    and associate a connection with the context.

    """
    connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection, target_metadata=target_metadata
        )

        with context.begin_transaction():
            context.run_migrations()


# Ejecutar migraciones cuando se llama desde alembic
if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
