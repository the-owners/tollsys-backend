from typing import Annotated
from datetime import datetime
from fastapi import Depends, HTTPException, Query
from sqlmodel import Column, Field, Session, SQLModel, create_engine, select, column
import sqlalchemy as sa
from sqlalchemy.sql import func
from sqlalchemy import DateTime


class TollPaymentBase(SQLModel):
    receipt_nro: str 
    rate: float
    vehicle_type_id: int | None = Field(default=None, foreign_key='VehicleType.id') 
    booth_id: int | None = Field(default=None, foreign_key='Booth.id')

class TollPayment(TollPaymentBase, table=True):
    __tablename__ = 'TollPayment'
    id: int | None = Field(default=None, primary_key=True)
    receipt_nro: str 
    rate: float
    booth_id: int | None = Field(default=None, foreign_key='Booth.id')
    vehicle_id:int | None = Field(default=None, foreign_key='VehicleType.id')
    created_at: datetime | None = Field(default_factory=lambda: datetime.now())
    created_by: int | None = Field(default=None, foreign_key='User.id')
    updated_at: datetime | None = Field(default=None, sa_column=Column(DateTime(), onupdate=func.now()))
    updated_by: int | None = Field(default=None, foreign_key='User.id')

class TollPaymentPublic(TollPaymentBase):
    id: int
    receipt_nro: str
    rate: float
    vehicle_type_id: int
    booth_id: int
    created_at: datetime | None
    created_by: int | None
    updated_at: datetime | None
    updated_by: int | None
    

class TollPaymentCreate(TollPaymentBase):
    receipt_nro: str
    rate: float
    vehicle_type_id: int
    booth_id: int

class TollPaymentUpdate(TollPaymentBase):
    receipt_nro: str | None = None
    rate: float | None = None
    vehicle_type_id: int | None = None
    booth_id: int | None = None
    updated_by: int | None = None
