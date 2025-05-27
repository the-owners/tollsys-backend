import decimal
from typing import Annotated, Generic, List, TypeVar
from datetime import datetime
from fastapi import Depends, HTTPException, Query
from sqlmodel import Column, Field, Session, SQLModel, create_engine, select, column
import sqlalchemy as sa
from sqlalchemy.sql import func
from sqlalchemy import DateTime
from pydantic import BaseModel
from src.booths.models import BoothPublic
from src.tolls.models import TollPublic
from src.vehicle_types.models import VehicleTypePublic
from src.payment_methods.models import PaymentMethodPublic

class TollPaymentBase(SQLModel):
    pass


class PaymentMethodTPResponse(SQLModel):
    payment_method: PaymentMethodPublic
    amount: int


class TollPayment(TollPaymentBase, table=True):
    __tablename__ = 'TollPayment'
    id: int | None = Field(default=None, primary_key=True)
    receipt_nro: str | None = Field(unique=True)
    booth: BoothPublic
    toll: TollPublic
    car_type: VehicleTypePublic
    amounts: list[PaymentMethodTPResponse]
    created_at: datetime | None = Field(default_factory=lambda: datetime.now())
    created_by: int | None = Field(default=None, foreign_key='User.id')
    updated_at: datetime | None = Field(default=None, sa_column=Column(DateTime(), onupdate=func.now()))
    updated_by: int | None = Field(default=None, foreign_key='User.id')


class PaymentMethodTPCreate(SQLModel):
    payment_method_id: int
    value: decimal.Decimal


class TollPaymentCreate(SQLModel):
    car_type_id: int
    multiple_payment_methods: bool
    amounts: list[PaymentMethodTPCreate]


class TollPaymentPublic(TollPaymentBase):
    id: int
    receipt_nro: str
    booth: BoothPublic
    toll: TollPublic
    car_type: VehicleTypePublic
    amounts: list[PaymentMethodTPResponse]
    created_at: datetime
