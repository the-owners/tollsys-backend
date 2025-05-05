from logging.config import fileConfig
from sqlalchemy import engine_from_config, pool
from alembic import context
from sqlmodel import SQLModel

import os
import sys
from dotenv import load_dotenv

# Agrega 'src' al PYTHONPATH para que los imports absolutos funcionen
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))

# Cargar variables de entorno desde .env
load_dotenv()

# Importa el motor de base de datos
from database.core import engine

# Importa los modelos para que SQLModel registre su metadata
# Ajusta los paths de acuerdo a tu estructura en 'src'
from users.models import *
from tolls.models import *
from roles.models import *

# Configuración de Alembic
config = context.config

# Habilita logging de Alembic
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Metadata de SQLModel para autogenerar migraciones
target_metadata = SQLModel.metadata


def run_migrations_offline():
    """Ejecuta migraciones en modo offline."""
    url = str(engine.url)
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
        compare_type=True,
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online():
    """Ejecuta migraciones en modo online."""
    connectable = engine

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
            compare_type=True,
        )

        with context.begin_transaction():
            context.run_migrations()


# Selecciona el modo de ejecución
if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
