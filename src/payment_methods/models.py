from typing import Annotated
from datetime import datetime
from fastapi import Depends, HTTPException, Query
from sqlmodel import Column, Field, Session, SQLModel, create_engine, select, column
import sqlalchemy as sa
from sqlalchemy.sql import func
from sqlalchemy import Index, DateTime

class PaymentMethodBase(SQLModel):
    name: str = Field(index=True)
    active: bool = Field(default=True)
    amount: int = Field(default=True)
    created_at: datetime.datetime | None = Field(default=datetime.datetime.now)
    created_by: int | None = Field(default=None, foreign_key='User.id')
    updated_at: datetime.datetime | None = Field(sa_column=Column(DateTime(), onupdate=func.now()))
    updated_by: int | None = Field(default=None, foreign_key='User.id')

class PaymentMethod(PaymentMethodBase, table=True):
    __tablename__ = "PaymentMethod"
    id: int | None = Field(default=None, primary_key=True)

    __table_args__ = (
        # name, active, amount, created_at, created_by, updated_at, updated_by
        Index('idx_paymentMethod_name', 'name'),
        Index('idx_paymentMethod_active', 'active'),
        Index('idx_paymentMethod_amount', 'amount'),
        Index('idx_paymentMethod_created_by', 'created_by'),
        Index('idx_paymentMethod_updated_at', 'updated_at'),
        Index('idx_paymentMethod_updated_by', 'updated_by')
    )

class PaymentMethodPublic(PaymentMethodBase):
    id: int

class PaymentMethodCreate(PaymentMethodBase):
    name: str
    active: bool

# nullable to allow for partial update, but
# here we ignore sum shit cuz mypy gets obnoxious otherwise
class PaymentMethodUpdate(PaymentMethodBase):
    name: str | None = None # type: ignore[assignment]
    active: bool | None = None # type: ignore[assignment]
