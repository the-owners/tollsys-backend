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
    # here's some duped code ig
    # Reflect existing tables
    # user_table = sa.Table(
    #     'User',
    #     op.get_context().opts['target_metadata'],
    #     sa.Column('id', sa.Integer()),
    #     sa.Column('name', sa.String()),
    #     sa.Column('username', sa.String()),
    #     sa.Column('password', sa.String()),
    #     sa.Column('role_id', sa.Integer()),
    #     sa.Column('toll_id', sa.Integer()),
    #     sa.Column('created_at', sa.DateTime()),
    #     sa.Column('created_by', sa.Integer()),
    #     autoload=True
    # )
    
    # role_table = sa.Table(
    #     'Role',
    #     op.get_context().opts['target_metadata'],
    #     sa.Column('id', sa.Integer()),
    #     sa.Column('name', sa.String()),
    #     sa.Column('created_at', sa.DateTime()),
    #     sa.Column('created_by', sa.Integer()),
    #     autoload=True
    # )

    # toll_table = sa.Table(
    #     'Toll',
    #     op.get_context().opts['target_metadata'],
    #     sa.Column('id', sa.Integer()),
    #     sa.Column('tax_id', sqlmodel.sql.sqltypes.AutoString()),
    #     sa.Column('legal_name', sqlmodel.sql.sqltypes.AutoString()),
    #     sa.Column('address', sqlmodel.sql.sqltypes.AutoString()),
    #     sa.Column('created_at', sa.DateTime()),
    #     sa.Column('created_by', sa.Integer()),
    #     sa.Column('updated_at', sa.DateTime()),
    #     sa.Column('updated_by', sa.Integer()),
    #     autoload=True
    # )
    inspector = sa.inspect(op.get_bind())

    # Method 2: Access the metadata directly (carefully!)
    metadata = op.get_context().opts['target_metadata']
    user_table = metadata.tables['User']
    role_table = metadata.tables['Role']
    toll_table = metadata.tables['Toll']

    # Insert initial data (handles circular references)
    op.bulk_insert(
        user_table,
        [{
            'id': 1,
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
            'id': 1,
            'name': 'admin',
            'created_at': datetime.utcnow(),
            'created_by': 1,  # Reference existing user
            'updated_at': datetime.utcnow(),
            'updated_by': 1
        }]
    )

    op.bulk_insert(
        toll_table,
        [{
            'id': 1,
            'tax_id': 'V123456789',
            'created_at': datetime.utcnow(),
            'created_by': 1,  # Reference existing user
            'updated_at': datetime.utcnow(),
            'updated_by': 1
        }]
    )
    
    # Update user to complete the circle
    op.execute(
        user_table.update()
        .where(user_table.c.id == 1)
        .values(
            role_id=1,
            toll_id=1,
            created_by=1
        )
    )


def downgrade() -> None:
    """Downgrade schema."""
    pass
