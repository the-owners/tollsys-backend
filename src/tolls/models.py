import datetime
import decimal
from typing import Optional
from sqlmodel import Field, SQLModel
from enum import Enum
import sqlalchemy as sa
from sqlalchemy.sql import func
from sqlalchemy import Index

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

