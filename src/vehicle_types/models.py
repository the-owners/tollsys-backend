from typing import Annotated
from datetime import datetime
from fastapi import Depends, HTTPException, Query
from sqlmodel import Column, Field, Session, SQLModel, create_engine, select, column
import sqlalchemy as sa
from sqlalchemy.sql import func
from sqlalchemy import DateTime

class VehicleTypeBase(SQLModel):
    name: str 
    icon: str
    rate: float
    active: bool 
    

class VehicleType(VehicleTypeBase, table=True):
    __tablename__ = 'VehicleType'
    id: int | None = Field(default=None, primary_key=True)
    name: str 
    icon: str
    rate: float
    active:bool
    created_at: datetime | None = Field(default_factory=lambda: datetime.now())
    created_by: int | None = Field(default=None, foreign_key='User.id')
    updated_at: datetime | None = Field(default=None, sa_column=Column(DateTime(), onupdate=func.now()))
    updated_by: int | None = Field(default=None, foreign_key='User.id')

class VehicleTypePublic(VehicleTypeBase):
    id: int
    name: str
    icon:str
    rate: float
    active: bool 
    created_at: datetime | None
    created_by: int | None
    updated_at: datetime | None
    updated_by: int | None
    

class VehicleTypeCreate(VehicleTypeBase):
    name: str
    icon: str
    rate: float
    active: bool

class VehicleTypeUpdate(VehicleTypeBase):
    name: str | None = None # type: ignore[assignment]
    icon:str | None = None
    rate:float | None = None
    active: bool | None = None # type: ignore[assignment]
    updated_by: int | None = None
