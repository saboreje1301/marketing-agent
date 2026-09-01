import os
from logging.config import fileConfig

from alembic import context
from sqlalchemy import engine_from_config, pool

# NO importar settings aquí (causa errores de validación)
# Leer DATABASE_URL directamente

config = context.config

# Estrategia de lectura de DATABASE_URL:
# 1. Variable de entorno (Render)
# 2. Si no, construir desde env vars individuales
# 3. Si no, usar default local
database_url = os.getenv("DATABASE_URL")

if not database_url:
    # Construir desde variables individuales
    db_host = os.getenv("DB_HOST", "localhost")
    db_port = os.getenv("DB_PORT", "5432")
    db_name = os.getenv("DB_NAME", "marketing_ai")
    db_user = os.getenv("DB_USER", "marketing_user")
    db_password = os.getenv("DB_PASSWORD", "marketing123")
    
    database_url = (
        f"postgresql+psycopg://"
        f"{db_user}:"
        f"{db_password}@"
        f"{db_host}:"
        f"{db_port}/"
        f"{db_name}"
    )

config.set_main_option("sqlalchemy.url", database_url)

# Importar Base DESPUÉS de configurar la BD
try:
    from app.database.base import Base
    target_metadata = Base.metadata
except Exception as e:
    print(f"⚠️  Warning: Could not import Base: {e}")
    target_metadata = None


if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# target_metadata ya está definida en el try/except arriba

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
        context.configure(connection=connection, target_metadata=target_metadata)

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
