"""initial data

Revision ID: ac9f2fb2413a
Revises: a72951a86ce4
Create Date: 2025-05-10 16:17:55.981635

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
import sqlmodel.sql.sqltypes
from datetime import datetime

# revision identifiers, used by Alembic.
revision: str = 'ac9f2fb2413a'
down_revision: Union[str, None] = 'a72951a86ce4'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # ok so, there's no good way of doing data migration with alembic so,
    # this line below is gpt sorcery ngl
    metadata = op.get_context().opts['target_metadata']
    user_table = metadata.tables['User']
    role_table = metadata.tables['Role']
    toll_table = metadata.tables['Toll']

    # Insert initial data (handles circular references)
    op.bulk_insert(
        user_table,
        [{
            'id': 0,
            'name': 'Superuser',
            'username': 'root',
            'password': '$2b$12$AIR2ZnzYAWfWoS/gp39aHO9/A7LhbEP/K0AJFTWVSAfzxi//J/VNa',  # toor
            'role_id': None,  # Temporary NULL
            'toll_id': None,  # Temporary NULL
            'created_at': datetime.utcnow(),
            'created_by': None,
            'updated_at': datetime.utcnow(),
            'created_by': None
        }]
    )
    
    op.bulk_insert(
        role_table,
        [{
            'id': 0,
            'name': 'admin',
            'created_at': datetime.utcnow(),
            'created_by': 0,  # Reference existing user
            'updated_at': datetime.utcnow(),
            'updated_by': 0
        }]
    )

    op.bulk_insert(
        toll_table,
        [{
            'id': 0,
            'tax_id': 'V123456789',
            'legal_name': 'Sample toll',
            'address': 'Sample address',
            'created_at': datetime.utcnow(),
            'created_by': 0,  # Reference existing user
            'updated_at': datetime.utcnow(),
            'updated_by': 0
        }]
    )
    
    # Update user to complete the circle
    op.execute(
        user_table.update()
        .where(user_table.c.id == 0)
        .values(
            role_id=0,
            toll_id=0,
            created_by=0,
            updated_by=0
        )
    )


def downgrade() -> None:
    """Downgrade schema."""
    metadata = op.get_context().opts['target_metadata']
    user_table = metadata.tables['User']
    role_table = metadata.tables['Role']
    toll_table = metadata.tables['Toll']
    op.execute(
        user_table.delete()
        .where(user_table.c.id == 0)
    )
    op.execute(
        role_table.delete()
        .where(role_table.c.id == 0)
    )
    op.execute(
        toll_table.delete()
        .where(toll_table.c.id == 0)
    )
