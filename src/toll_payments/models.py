import decimal
from typing import Annotated, Generic, List, TypeVar
from datetime import datetime
import uuid
from fastapi import Depends, HTTPException, Query
from sqlmodel import Column, Field, Session, SQLModel, create_engine, select, column, Relationship
import sqlalchemy as sa
from sqlalchemy.sql import func
from sqlalchemy import DateTime
from pydantic import BaseModel
from src.booths.models import BoothPublic
from src.tolls.models import TollPublic
from src.vehicle_types.models import VehicleTypePublic
from src.payment_methods.models import PaymentMethod, PaymentMethodPublic

class TollPaymentBase(SQLModel):
    booth_id: int = Field(foreign_key="Booth.id")
    toll_id: int = Field(foreign_key="Toll.id")
    car_type_id: int = Field(foreign_key="VehicleType.id")


class PaymentMethodTP(SQLModel, table=True):  # New table for payment methods
    __tablename__: str = "PaymentMethodTP"
    id: int | None = Field(default=None, primary_key=True)
    toll_payment_id: int = Field(foreign_key="TollPayment.id")  # Foreign key to TollPayment
    payment_method_id: int = Field(foreign_key="PaymentMethod.id")  # Foreign key to PaymentMethod
    amount: decimal.Decimal = Field(default=0)

    toll_payment: "TollPayment" = Relationship(back_populates="amounts")


class PaymentMethodTPCreate(SQLModel):
    payment_method_id: int
    value: decimal.Decimal


class PaymentMethodTPResponse(SQLModel):
    """
    Represents the fields of PaymentMethodTP that should be exposed in the API response.
    """
    amount: decimal.Decimal
    id: int
    toll_payment_id: int
    payment_method_id: int
    # If you also need the PaymentMethod details, you would add:
    # payment_method: PaymentMethodPublic # (assuming you define PaymentMethodPublic)

# Wrapper model to encapsulate PaymentMethodTPResponse under the "payment_method" key
class PaymentMethodTPWrapper(SQLModel):
    """
    Wraps a PaymentMethodTPResponse object under the 'payment_method' key
    for the desired API response format.
    """
    payment_method: PaymentMethodPublic
    amount: decimal.Decimal

class TollPayment(TollPaymentBase, table=True):
    __tablename__: str = "TollPayment"
    id: int | None = Field(default=None, primary_key=True)
    receipt_nro: str | None = Field(unique=True, default_factory=lambda: str(uuid.uuid4()))
    booth: "Booth" = Relationship(back_populates="toll_payments")
    toll: "Toll" = Relationship(back_populates="toll_payments")
    car_type: "VehicleType" = Relationship(back_populates="toll_payments")
    amounts: list[PaymentMethodTP] = Relationship(back_populates="toll_payment")  # Relationship to PaymentMethodTP
    created_at: datetime | None = Field(default_factory=lambda: datetime.now())
    created_by: int | None = Field(default=None, foreign_key="User.id")
    updated_at: datetime | None = Field(default=None, sa_column=Column(DateTime(), onupdate=func.now()))
    updated_by: int | None = Field(default=None, foreign_key="User.id")


class TollPaymentCreate(SQLModel):
    car_type_id: int
    multiple_payment_methods: bool
    amounts: list[PaymentMethodTPCreate]  # List of dictionaries with payment_method_id and amount


class TollPaymentPublic(SQLModel):
    id: int
    receipt_nro: str
    toll: "TollPublic"
    booth: "BoothPublic"
    car_type: "VehicleTypePublic"
    amounts: list[PaymentMethodTPWrapper]
    created_at: datetime
