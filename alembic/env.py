from logging.config import fileConfig
from sqlalchemy import engine_from_config, pool
from alembic import context
from sqlmodel import SQLModel

import os
import sys
from dotenv import load_dotenv

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))
# Agregamos la raíz del proyecto al path


# Carga variables del entorno desde .env
load_dotenv()

# Importa el engine y modelos
from database.core import engine

from app.models import *  # importa todos tus modelos para registrar metadata

# Configuración de Alembic
config = context.config

# Configura logging si se desea
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Establece metadata para autogenerar migraciones
target_metadata = SQLModel.metadata


def run_migrations_offline():
    """Ejecuta migraciones en modo offline."""
    url = str(engine.url)
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
        compare_type=True,  # Importante para detectar cambios en tipos de columnas
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


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
