import datetime
import decimal
from typing import Optional
from sqlmodel import Field, SQLModel
from enum import Enum
import sqlalchemy as sa
from sqlalchemy.sql import func
from sqlalchemy import Index


class BoothStatus(str, Enum):

    AVAILABLE = 'AVAILABLE'
    CLOSED = 'CLOSED'
    MAINTENANCE = 'MAINTENANCE'
    OCCUPIED = 'OCCUPIED'
    

class Toll(SQLModel, table=True):

    __tablename__ = 'Toll'

    id: Optional[int] = Field(default=None, primary_key=True)
    tax_id: Optional[str]
    legal_name: Optional[str]
    address: Optional[str]
    created_at: Optional[datetime.datetime]
    created_by: Optional[int] = Field(foreign_key='User.id')
    updated_at: Optional[datetime.datetime]
    updated_by: Optional[int] = Field(foreign_key='User.id')

    __table_args__ = (
                
    Index('idx_toll_tax_id', 'tax_id'),
    Index('idx_toll_created_by', 'created_by'),
    Index('idx_toll_updated_by', 'updated_by'),
            )



class Booth(SQLModel, table=True):

    __tablename__ = 'Booth'

    id: Optional[int] = Field(default=None, primary_key=True)
    name: Optional[str]
    active: Optional[bool]
    status: Optional[BoothStatus] = Field(sa_type=sa.Enum(BoothStatus))
    toll_id: Optional[int] = Field(foreign_key='Toll.id')
    created_at: Optional[datetime.datetime]
    created_by: Optional[int] = Field(foreign_key='User.id')
    updated_at: Optional[datetime.datetime]
    updated_by: Optional[int] = Field(foreign_key='User.id')

    __table_args__ = (
                
    Index('idx_booth_toll_id', 'toll_id'),
    Index('idx_booth_created_by', 'created_by'),
    Index('idx_booth_updated_by', 'updated_by'),
            )



class BoothCashSession(SQLModel, table=True):

    __tablename__ = 'BoothCashSession'

    id: Optional[int] = Field(default=None, primary_key=True)
    booth_id: int = Field(foreign_key='Booth.id')
    user_id: int = Field(foreign_key='User.id')
    opened_at: datetime.datetime
    initial_amount: Optional[decimal.Decimal] = Field(sa_type=sa.Numeric())
    closing_amount: Optional[decimal.Decimal] = Field(sa_type=sa.Numeric())
    closing_reason: Optional[str]
    closing_observations: Optional[str] = Field(sa_type=sa.Text())
    closed_at: Optional[datetime.datetime]
    created_at: Optional[datetime.datetime] = Field(sa_column_kwargs={'server_default': func.now()})
    created_by: Optional[int] = Field(foreign_key='User.id')
    updated_at: Optional[datetime.datetime]
    updated_by: Optional[int] = Field(foreign_key='User.id')

    __table_args__ = (
                
    Index('idx_booth_cash_session_booth_id', 'booth_id'),
    Index('idx_booth_cash_session_user_id', 'user_id'),
    Index('idx_booth_cash_session_created_by', 'created_by'),
    Index('idx_booth_cash_session_updated_by', 'updated_by'),
            )



class User(SQLModel, table=True):

    __tablename__ = 'User'

    id: Optional[int] = Field(default=None, primary_key=True)
    name: Optional[str]
    username: Optional[str]
    password: Optional[str]
    role_id: Optional[int] = Field(foreign_key='Role.id')
    toll_id: Optional[int] = Field(foreign_key='Toll.id')
    created_at: Optional[datetime.datetime]
    created_by: Optional[int] = Field(foreign_key='User.id')
    updated_at: Optional[datetime.datetime]
    updated_by: Optional[int] = Field(foreign_key='User.id')

    __table_args__ = (
                
    Index('idx_user_username', 'username'),
    Index('idx_user_role_id', 'role_id'),
    Index('idx_user_toll_id', 'toll_id'),
    Index('idx_user_created_by', 'created_by'),
    Index('idx_user_updated_by', 'updated_by'),
            )



class UserSession(SQLModel, table=True):

    __tablename__ = 'UserSession'

    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key='User.id')
    created_at: Optional[datetime.datetime] = Field(sa_column_kwargs={'server_default': func.now()})
    created_by: Optional[int] = Field(foreign_key='User.id')
    updated_at: Optional[datetime.datetime]
    updated_by: Optional[int] = Field(foreign_key='User.id')
    closed_at: Optional[datetime.datetime]
    closing_reason: Optional[str]
    closing_observations: Optional[str] = Field(sa_type=sa.Text())

    __table_args__ = (
                
    Index('idx_user_session_user_id', 'user_id'),
    Index('idx_user_session_created_by', 'created_by'),
    Index('idx_user_session_updated_by', 'updated_by'),
            )



class Role(SQLModel, table=True):

    __tablename__ = 'Role'

    id: Optional[int] = Field(default=None, primary_key=True)
    name: Optional[str]
    created_at: Optional[datetime.datetime]
    created_by: Optional[int] = Field(foreign_key='User.id')
    updated_at: Optional[datetime.datetime]
    updated_by: Optional[int] = Field(foreign_key='User.id')

    __table_args__ = (
                
    Index('idx_role_name', 'name'),
    Index('idx_role_created_by', 'created_by'),
    Index('idx_role_updated_by', 'updated_by'),
            )



class Permission(SQLModel, table=True):

    __tablename__ = 'Permission'

    id: Optional[int] = Field(default=None, primary_key=True)
    name: Optional[str]
    created_at: Optional[datetime.datetime]
    updated_at: Optional[datetime.datetime]

    __table_args__ = (
                
    Index('idx_permission_name', 'name'),
            )



class RolePermission(SQLModel, table=True):

    __tablename__ = 'RolePermission'

    id: Optional[int] = Field(default=None, primary_key=True)
    role_id: Optional[int] = Field(foreign_key='Role.id')
    permission_id: Optional[int] = Field(foreign_key='Permission.id')
    created_at: Optional[datetime.datetime]
    created_by: Optional[int] = Field(foreign_key='User.id')
    updated_at: Optional[datetime.datetime]
    updated_by: Optional[int] = Field(foreign_key='User.id')

    __table_args__ = (
                
    Index('idx_role_permission_role_id', 'role_id'),
    Index('idx_role_permission_permission_id', 'permission_id'),
    Index('idx_role_permission_created_by', 'created_by'),
    Index('idx_role_permission_updated_by', 'updated_by'),
            )



class VehicleType(SQLModel, table=True):

    __tablename__ = 'VehicleType'

    id: Optional[int] = Field(default=None, primary_key=True)
    name: Optional[str]
    icon: Optional[str]
    rate: Optional[decimal.Decimal] = Field(sa_type=sa.Numeric())
    active: Optional[bool]
    created_at: Optional[datetime.datetime]
    created_by: Optional[int] = Field(foreign_key='User.id')
    updated_at: Optional[datetime.datetime]
    updated_by: Optional[int] = Field(foreign_key='User.id')

    __table_args__ = (
                
    Index('idx_vehicle_type_name', 'name'),
    Index('idx_vehicle_type_active', 'active'),
    Index('idx_vehicle_type_created_by', 'created_by'),
    Index('idx_vehicle_type_updated_by', 'updated_by'),
            )



class PaymentMethod(SQLModel, table=True):

    __tablename__ = 'PaymentMethod'

    id: Optional[int] = Field(default=None, primary_key=True)
    name: Optional[str]
    icon: Optional[str]
    active: Optional[bool]
    created_at: Optional[datetime.datetime]
    created_by: Optional[int] = Field(foreign_key='User.id')
    updated_at: Optional[datetime.datetime]
    updated_by: Optional[int] = Field(foreign_key='User.id')

    __table_args__ = (
                
    Index('idx_payment_method_name', 'name'),
    Index('idx_payment_method_active', 'active'),
    Index('idx_payment_method_created_by', 'created_by'),
    Index('idx_payment_method_updated_by', 'updated_by'),
            )



class TollPayment(SQLModel, table=True):

    __tablename__ = 'TollPayment'

    id: Optional[int] = Field(default=None, primary_key=True)
    receipt_nro: Optional[str] = Field(unique=True)
    rate: Optional[decimal.Decimal] = Field(sa_type=sa.Numeric())
    vehicle_type_id: Optional[int] = Field(foreign_key='VehicleType.id')
    booth_id: Optional[int] = Field(foreign_key='Booth.id')
    created_at: Optional[datetime.datetime]
    paymented_at: Optional[datetime.datetime]
    created_by: Optional[int] = Field(foreign_key='User.id')

    __table_args__ = (
                
    Index('idx_toll_payment_receipt_nro', 'receipt_nro'),
    Index('idx_toll_payment_vehicle_type_id', 'vehicle_type_id'),
    Index('idx_toll_payment_booth_id', 'booth_id'),
    Index('idx_toll_payment_created_by', 'created_by'),
    Index('idx_toll_payment_created_at', 'created_at'),
            )



class TollPaymentMethod(SQLModel, table=True):

    __tablename__ = 'TollPaymentMethod'

    id: Optional[int] = Field(default=None, primary_key=True)
    toll_payment_id: Optional[int] = Field(foreign_key='TollPayment.id')
    payment_method_id: Optional[int] = Field(foreign_key='PaymentMethod.id')
    amount: Optional[decimal.Decimal] = Field(sa_type=sa.Numeric())
    created_at: Optional[datetime.datetime]
    created_by: Optional[int] = Field(foreign_key='User.id')

    __table_args__ = (
                
    Index('idx_toll_payment_method_toll_payment_id', 'toll_payment_id'),
    Index('idx_toll_payment_method_payment_method_id', 'payment_method_id'),
    Index('idx_toll_payment_method_created_by', 'created_by'),
            )

