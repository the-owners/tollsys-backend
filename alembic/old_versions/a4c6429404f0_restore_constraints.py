"""restore constraints

Revision ID: a4c6429404f0
Revises: ac9f2fb2413a
Create Date: 2025-05-11 14:55:06.209480

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
import sqlmodel.sql.sqltypes


# revision identifiers, used by Alembic.
revision: str = "a4c6429404f0"
down_revision: Union[str, None] = "ac9f2fb2413a"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_foreign_key("fk_toll_user_c", "Toll", "User", ["created_by"], ["id"])
    op.create_foreign_key("fk_toll_user_u", "Toll", "User", ["updated_by"], ["id"])
    op.create_foreign_key("fk_role_user_c", "Role", "User", ["created_by"], ["id"])
    op.create_foreign_key("fk_role_user_u", "Role", "User", ["updated_by"], ["id"])
    op.create_foreign_key("fk_booth_toll", "Booth", "Toll", ["toll_id"], ["id"])
    op.create_foreign_key("fk_booth_user_c", "Booth", "User", ["created_by"], ["id"])
    op.create_foreign_key("fk_booth_user_u", "Booth", "User", ["updated_by"], ["id"])
    op.create_foreign_key("fk_boothcashsession_booth", "BoothCashSession", "Booth", ["booth_id"], ["id"])
    op.create_foreign_key("fk_boothcashsession_user", "BoothCashSession", "User", ["user_id"], ["id"])
    op.create_foreign_key("fk_boothcashsession_user_c", "BoothCashSession", "User", ["created_by"], ["id"])
    op.create_foreign_key("fk_boothcashsession_user_u", "BoothCashSession", "User", ["updated_by"], ["id"])
    op.create_foreign_key("fk_user_role", "User", "Role", ["role_id"], ["id"])
    op.create_foreign_key("fk_user_toll", "User", "Toll", ["toll_id"], ["id"])
    op.create_foreign_key("fk_user_user_c", "User", "User", ["created_by"], ["id"])
    op.create_foreign_key("fk_user_user_u", "User", "User", ["updated_by"], ["id"])
    op.create_foreign_key("fk_usersession_user", "UserSession", "User", ["user_id"], ["id"])
    op.create_foreign_key("fk_usersession_user_c", "UserSession", "User", ["created_by"], ["id"])
    op.create_foreign_key("fk_usersession_user_u", "UserSession", "User", ["updated_by"], ["id"])
    op.create_foreign_key("fk_rolepermission_role", "RolePermission", "Role", ["role_id"], ["id"])
    op.create_foreign_key("fk_rolepermission_permission", "RolePermission", "Permission", ["permission_id"], ["id"])
    op.create_foreign_key("fk_rolepermission_user_c", "RolePermission", "User", ["created_by"], ["id"])
    op.create_foreign_key("fk_rolepermission_user_u", "RolePermission", "User", ["updated_by"], ["id"])
    op.create_foreign_key("fk_vehicletype_user_c", "VehicleType", "User", ["created_by"], ["id"])
    op.create_foreign_key("fk_vehicletype_user_u", "VehicleType", "User", ["updated_by"], ["id"])
    op.create_foreign_key("fk_paymentmethod_user_c", "PaymentMethod", "User", ["created_by"], ["id"])
    op.create_foreign_key("fk_paymentmethod_user_u", "PaymentMethod", "User", ["updated_by"], ["id"])
    op.create_foreign_key("fk_tollpayment_vehicletype", "TollPayment", "VehicleType", ["vehicle_type_id"], ["id"])
    op.create_foreign_key("fk_tollpayment_booth", "TollPayment", "Booth", ["booth_id"], ["id"])
    op.create_foreign_key("fk_tollpayment_user_c", "TollPayment", "User", ["created_by"], ["id"])
    op.create_foreign_key("fk_tollpaymentmethod_tollpayment", "TollPaymentMethod", "TollPayment", ["toll_payment_id"], ["id"])
    op.create_foreign_key("fk_tollpaymentmethod_paymentmethod", "TollPaymentMethod", "PaymentMethod", ["payment_method_id"], ["id"])
    op.create_foreign_key("fk_tollpaymentmethod_user_c", "TollPaymentMethod", "User", ["created_by"], ["id"])
    
    


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_constraint("fk_toll_user_c", "Toll")
    op.drop_constraint("fk_toll_user_u", "Toll")
    op.drop_constraint("fk_role_user_c", "Role")
    op.drop_constraint("fk_role_user_u", "Role")
    op.drop_constraint("fk_booth_toll", "Booth")
    op.drop_constraint("fk_booth_user_c", "Booth")
    op.drop_constraint("fk_booth_user_u", "Booth")
    op.drop_constraint("fk_boothcashsession_booth", "BoothCashSession")
    op.drop_constraint("fk_boothcashsession_user", "BoothCashSession")
    op.drop_constraint("fk_boothcashsession_user_c", "BoothCashSession")
    op.drop_constraint("fk_boothcashsession_user_u", "BoothCashSession")
    op.drop_constraint("fk_user_role", "User")
    op.drop_constraint("fk_user_toll", "User")
    op.drop_constraint("fk_user_user_c", "User")
    op.drop_constraint("fk_user_user_u", "User")
    op.drop_constraint("fk_usersession_user", "UserSession")
    op.drop_constraint("fk_usersession_user_c", "UserSession")
    op.drop_constraint("fk_usersession_user_u", "UserSession")
    op.drop_constraint("fk_rolepermission_role", "RolePermission")
    op.drop_constraint("fk_rolepermission_permission", "RolePermission")
    op.drop_constraint("fk_rolepermission_user_c", "RolePermission")
    op.drop_constraint("fk_rolepermission_user_u", "RolePermission")
    op.drop_constraint("fk_vehicletype_user_c", "VehicleType")
    op.drop_constraint("fk_vehicletype_user_u", "VehicleType")
    op.drop_constraint("fk_paymentmethod_user_c", "PaymentMethod")
    op.drop_constraint("fk_paymentmethod_user_u", "PaymentMethod")
    op.drop_constraint("fk_tollpayment_vehicletype", "TollPayment")
    op.drop_constraint("fk_tollpayment_booth", "TollPayment")
    op.drop_constraint("fk_tollpayment_user_c", "TollPayment")
    op.drop_constraint("fk_tollpaymentmethod_tollpayment", "TollPaymentMethod")
    op.drop_constraint("fk_tollpaymentmethod_paymentmethod", "TollPaymentMethod")
    op.drop_constraint("fk_tollpaymentmethod_user_c", "TollPaymentMethod")
