"""initial tables, without fk constraints, temporary nullable columns

Revision ID: a72951a86ce4
Revises: 
Create Date: 2025-05-10 16:03:30.442439

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
import sqlmodel.sql.sqltypes


# revision identifiers, used by Alembic.
revision: str = 'a72951a86ce4'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table('Permission',
    sa.Column('id', sa.Integer(), nullable=True),
    sa.Column('name', sqlmodel.sql.sqltypes.AutoString(), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    with op.batch_alter_table('Permission', schema=None) as batch_op:
        batch_op.create_index('idx_permission_name', ['name'], unique=False)

    op.create_table('Role',
    sa.Column('id', sa.Integer(), nullable=True),
    sa.Column('name', sqlmodel.sql.sqltypes.AutoString(), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('created_by', sa.Integer(), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.Column('updated_by', sa.Integer(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    with op.batch_alter_table('Role', schema=None) as batch_op:
        batch_op.create_index('idx_role_created_by', ['created_by'], unique=False)
        batch_op.create_index('idx_role_name', ['name'], unique=False)
        batch_op.create_index('idx_role_updated_by', ['updated_by'], unique=False)

    op.create_table('Toll',
    sa.Column('id', sa.Integer(), nullable=True),
    sa.Column('tax_id', sqlmodel.sql.sqltypes.AutoString(), nullable=True),
    sa.Column('legal_name', sqlmodel.sql.sqltypes.AutoString(), nullable=True),
    sa.Column('address', sqlmodel.sql.sqltypes.AutoString(), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('created_by', sa.Integer(), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.Column('updated_by', sa.Integer(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    with op.batch_alter_table('Toll', schema=None) as batch_op:
        batch_op.create_index('idx_toll_created_by', ['created_by'], unique=False)
        batch_op.create_index('idx_toll_tax_id', ['tax_id'], unique=False)
        batch_op.create_index('idx_toll_updated_by', ['updated_by'], unique=False)

    op.create_table('User',
    sa.Column('id', sa.Integer(), nullable=True),
    sa.Column('name', sqlmodel.sql.sqltypes.AutoString(), nullable=True),
    sa.Column('username', sqlmodel.sql.sqltypes.AutoString(), nullable=True),
    sa.Column('password', sqlmodel.sql.sqltypes.AutoString(), nullable=True),
    sa.Column('role_id', sa.Integer(), nullable=True),
    sa.Column('toll_id', sa.Integer(), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('created_by', sa.Integer(), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.Column('updated_by', sa.Integer(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    with op.batch_alter_table('User', schema=None) as batch_op:
        batch_op.create_index('idx_user_created_by', ['created_by'], unique=False)
        batch_op.create_index('idx_user_role_id', ['role_id'], unique=False)
        batch_op.create_index('idx_user_toll_id', ['toll_id'], unique=False)
        batch_op.create_index('idx_user_updated_by', ['updated_by'], unique=False)
        batch_op.create_index('idx_user_username', ['username'], unique=False)

    op.create_table('Booth',
    sa.Column('id', sa.Integer(), nullable=True),
    sa.Column('name', sqlmodel.sql.sqltypes.AutoString(), nullable=True),
    sa.Column('active', sa.Boolean(), nullable=True),
    sa.Column('status', sa.Enum('AVAILABLE', 'CLOSED', 'MAINTENANCE', 'OCCUPIED', name='boothstatus'), nullable=True),
    sa.Column('toll_id', sa.Integer(), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('created_by', sa.Integer(), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.Column('updated_by', sa.Integer(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    with op.batch_alter_table('Booth', schema=None) as batch_op:
        batch_op.create_index('idx_booth_created_by', ['created_by'], unique=False)
        batch_op.create_index('idx_booth_toll_id', ['toll_id'], unique=False)
        batch_op.create_index('idx_booth_updated_by', ['updated_by'], unique=False)

    op.create_table('PaymentMethod',
    sa.Column('id', sa.Integer(), nullable=True),
    sa.Column('name', sqlmodel.sql.sqltypes.AutoString(), nullable=True),
    sa.Column('icon', sqlmodel.sql.sqltypes.AutoString(), nullable=True),
    sa.Column('active', sa.Boolean(), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('created_by', sa.Integer(), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.Column('updated_by', sa.Integer(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    with op.batch_alter_table('PaymentMethod', schema=None) as batch_op:
        batch_op.create_index('idx_payment_method_active', ['active'], unique=False)
        batch_op.create_index('idx_payment_method_created_by', ['created_by'], unique=False)
        batch_op.create_index('idx_payment_method_name', ['name'], unique=False)
        batch_op.create_index('idx_payment_method_updated_by', ['updated_by'], unique=False)

    op.create_table('RolePermission',
    sa.Column('id', sa.Integer(), nullable=True),
    sa.Column('role_id', sa.Integer(), nullable=True),
    sa.Column('permission_id', sa.Integer(), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('created_by', sa.Integer(), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.Column('updated_by', sa.Integer(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    with op.batch_alter_table('RolePermission', schema=None) as batch_op:
        batch_op.create_index('idx_role_permission_created_by', ['created_by'], unique=False)
        batch_op.create_index('idx_role_permission_permission_id', ['permission_id'], unique=False)
        batch_op.create_index('idx_role_permission_role_id', ['role_id'], unique=False)
        batch_op.create_index('idx_role_permission_updated_by', ['updated_by'], unique=False)

    op.create_table('UserSession',
    sa.Column('id', sa.Integer(), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()'), nullable=True),
    sa.Column('created_by', sa.Integer(), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.Column('updated_by', sa.Integer(), nullable=True),
    sa.Column('closed_at', sa.DateTime(), nullable=True),
    sa.Column('closing_reason', sqlmodel.sql.sqltypes.AutoString(), nullable=True),
    sa.Column('closing_observations', sa.Text(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    with op.batch_alter_table('UserSession', schema=None) as batch_op:
        batch_op.create_index('idx_user_session_created_by', ['created_by'], unique=False)
        batch_op.create_index('idx_user_session_updated_by', ['updated_by'], unique=False)
        batch_op.create_index('idx_user_session_user_id', ['user_id'], unique=False)

    op.create_table('VehicleType',
    sa.Column('id', sa.Integer(), nullable=True),
    sa.Column('name', sqlmodel.sql.sqltypes.AutoString(), nullable=True),
    sa.Column('icon', sqlmodel.sql.sqltypes.AutoString(), nullable=True),
    sa.Column('rate', sa.Numeric(), nullable=True),
    sa.Column('active', sa.Boolean(), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('created_by', sa.Integer(), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.Column('updated_by', sa.Integer(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    with op.batch_alter_table('VehicleType', schema=None) as batch_op:
        batch_op.create_index('idx_vehicle_type_active', ['active'], unique=False)
        batch_op.create_index('idx_vehicle_type_created_by', ['created_by'], unique=False)
        batch_op.create_index('idx_vehicle_type_name', ['name'], unique=False)
        batch_op.create_index('idx_vehicle_type_updated_by', ['updated_by'], unique=False)

    op.create_table('BoothCashSession',
    sa.Column('id', sa.Integer(), nullable=True),
    sa.Column('booth_id', sa.Integer(), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('opened_at', sa.DateTime(), nullable=True),
    sa.Column('initial_amount', sa.Numeric(), nullable=True),
    sa.Column('closing_amount', sa.Numeric(), nullable=True),
    sa.Column('closing_reason', sqlmodel.sql.sqltypes.AutoString(), nullable=True),
    sa.Column('closing_observations', sa.Text(), nullable=True),
    sa.Column('closed_at', sa.DateTime(), nullable=True),
    sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()'), nullable=True),
    sa.Column('created_by', sa.Integer(), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.Column('updated_by', sa.Integer(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    with op.batch_alter_table('BoothCashSession', schema=None) as batch_op:
        batch_op.create_index('idx_booth_cash_session_booth_id', ['booth_id'], unique=False)
        batch_op.create_index('idx_booth_cash_session_created_by', ['created_by'], unique=False)
        batch_op.create_index('idx_booth_cash_session_updated_by', ['updated_by'], unique=False)
        batch_op.create_index('idx_booth_cash_session_user_id', ['user_id'], unique=False)

    op.create_table('TollPayment',
    sa.Column('id', sa.Integer(), nullable=True),
    sa.Column('receipt_nro', sqlmodel.sql.sqltypes.AutoString(), nullable=True),
    sa.Column('rate', sa.Numeric(), nullable=True),
    sa.Column('vehicle_type_id', sa.Integer(), nullable=True),
    sa.Column('booth_id', sa.Integer(), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('paymented_at', sa.DateTime(), nullable=True),
    sa.Column('created_by', sa.Integer(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('receipt_nro')
    )
    with op.batch_alter_table('TollPayment', schema=None) as batch_op:
        batch_op.create_index('idx_toll_payment_booth_id', ['booth_id'], unique=False)
        batch_op.create_index('idx_toll_payment_created_at', ['created_at'], unique=False)
        batch_op.create_index('idx_toll_payment_created_by', ['created_by'], unique=False)
        batch_op.create_index('idx_toll_payment_receipt_nro', ['receipt_nro'], unique=False)
        batch_op.create_index('idx_toll_payment_vehicle_type_id', ['vehicle_type_id'], unique=False)

    op.create_table('TollPaymentMethod',
    sa.Column('id', sa.Integer(), nullable=True),
    sa.Column('toll_payment_id', sa.Integer(), nullable=True),
    sa.Column('payment_method_id', sa.Integer(), nullable=True),
    sa.Column('amount', sa.Numeric(), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('created_by', sa.Integer(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    with op.batch_alter_table('TollPaymentMethod', schema=None) as batch_op:
        batch_op.create_index('idx_toll_payment_method_created_by', ['created_by'], unique=False)
        batch_op.create_index('idx_toll_payment_method_payment_method_id', ['payment_method_id'], unique=False)
        batch_op.create_index('idx_toll_payment_method_toll_payment_id', ['toll_payment_id'], unique=False)

    # ### end Alembic commands ###


def downgrade() -> None:
    """Downgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('TollPaymentMethod', schema=None) as batch_op:
        batch_op.drop_index('idx_toll_payment_method_toll_payment_id')
        batch_op.drop_index('idx_toll_payment_method_payment_method_id')
        batch_op.drop_index('idx_toll_payment_method_created_by')

    op.drop_table('TollPaymentMethod')
    with op.batch_alter_table('TollPayment', schema=None) as batch_op:
        batch_op.drop_index('idx_toll_payment_vehicle_type_id')
        batch_op.drop_index('idx_toll_payment_receipt_nro')
        batch_op.drop_index('idx_toll_payment_created_by')
        batch_op.drop_index('idx_toll_payment_created_at')
        batch_op.drop_index('idx_toll_payment_booth_id')

    op.drop_table('TollPayment')
    with op.batch_alter_table('BoothCashSession', schema=None) as batch_op:
        batch_op.drop_index('idx_booth_cash_session_user_id')
        batch_op.drop_index('idx_booth_cash_session_updated_by')
        batch_op.drop_index('idx_booth_cash_session_created_by')
        batch_op.drop_index('idx_booth_cash_session_booth_id')

    op.drop_table('BoothCashSession')
    with op.batch_alter_table('VehicleType', schema=None) as batch_op:
        batch_op.drop_index('idx_vehicle_type_updated_by')
        batch_op.drop_index('idx_vehicle_type_name')
        batch_op.drop_index('idx_vehicle_type_created_by')
        batch_op.drop_index('idx_vehicle_type_active')

    op.drop_table('VehicleType')
    with op.batch_alter_table('UserSession', schema=None) as batch_op:
        batch_op.drop_index('idx_user_session_user_id')
        batch_op.drop_index('idx_user_session_updated_by')
        batch_op.drop_index('idx_user_session_created_by')

    op.drop_table('UserSession')
    with op.batch_alter_table('RolePermission', schema=None) as batch_op:
        batch_op.drop_index('idx_role_permission_updated_by')
        batch_op.drop_index('idx_role_permission_role_id')
        batch_op.drop_index('idx_role_permission_permission_id')
        batch_op.drop_index('idx_role_permission_created_by')

    op.drop_table('RolePermission')
    with op.batch_alter_table('PaymentMethod', schema=None) as batch_op:
        batch_op.drop_index('idx_payment_method_updated_by')
        batch_op.drop_index('idx_payment_method_name')
        batch_op.drop_index('idx_payment_method_created_by')
        batch_op.drop_index('idx_payment_method_active')

    op.drop_table('PaymentMethod')
    with op.batch_alter_table('Booth', schema=None) as batch_op:
        batch_op.drop_index('idx_booth_updated_by')
        batch_op.drop_index('idx_booth_toll_id')
        batch_op.drop_index('idx_booth_created_by')

    op.drop_table('Booth')
    with op.batch_alter_table('User', schema=None) as batch_op:
        batch_op.drop_index('idx_user_username')
        batch_op.drop_index('idx_user_updated_by')
        batch_op.drop_index('idx_user_toll_id')
        batch_op.drop_index('idx_user_role_id')
        batch_op.drop_index('idx_user_created_by')

    op.drop_table('User')
    with op.batch_alter_table('Toll', schema=None) as batch_op:
        batch_op.drop_index('idx_toll_updated_by')
        batch_op.drop_index('idx_toll_tax_id')
        batch_op.drop_index('idx_toll_created_by')

    op.drop_table('Toll')
    with op.batch_alter_table('Role', schema=None) as batch_op:
        batch_op.drop_index('idx_role_updated_by')
        batch_op.drop_index('idx_role_name')
        batch_op.drop_index('idx_role_created_by')

    op.drop_table('Role')
    with op.batch_alter_table('Permission', schema=None) as batch_op:
        batch_op.drop_index('idx_permission_name')

    op.drop_table('Permission')
    # ### end Alembic commands ###
    # FALTA QUITAR TYPE boothstatus
