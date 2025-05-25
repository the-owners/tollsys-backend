import sys, os
# —————— AJUSTE DE PYTHONPATH ——————
# Hacer visible el directorio raíz (donde está 'src/')
root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, root)
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from logging.config import fileConfig
from sqlalchemy import engine_from_config, pool
from alembic import context
from dotenv import load_dotenv
import warnings
import sqlalchemy as sa

# Cargar variables de entorno
dotenv_path = os.path.join(root, '.env')
if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)


# URL de la base de datos (toma de .env o sqlite por defecto)
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///tollsys-backend.db")

# Importar metadata de tus modelos
from src.database import models
from sqlmodel import SQLModel
#from src.database.models import SQLModel  # Asegúrate de que src/database/__init__.py exista

# Configuración de Alembic
target_metadata = SQLModel.metadata
config = context.config
if config.config_file_name:
    fileConfig(config.config_file_name)

# Suprimir warnings de dependencias circulares
warnings.filterwarnings(
    "ignore",
    message="Cannot correctly sort tables; there are unresolvable cycles",
    category=sa.exc.SAWarning
)


def run_migrations_offline() -> None:
    """Ejecutar migraciones en modo 'offline'."""
    url = DATABASE_URL
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
        render_as_batch=True,
        user_module_prefix="sqlmodel.sql.sqltypes",
        process_revision_directives=lambda *args, **kwargs: None
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """Ejecutar migraciones en modo 'online'."""
    # Si no está definido en alembic.ini, usar DATABASE_URL
    if not config.get_main_option("sqlalchemy.url"):
        config.set_main_option("sqlalchemy.url", DATABASE_URL)

    connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
            render_as_batch=True,
            user_module_prefix="sqlmodel.sql.sqltypes",
            process_revision_directives=lambda *args, **kwargs: None
        )

        with context.begin_transaction():
            context.run_migrations()


# Ejecutar según el modo
if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
