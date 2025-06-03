from typing import Annotated, Generic, List, TypeVar
from datetime import datetime
from fastapi import Depends, HTTPException, Query
from sqlmodel import Column, Field, Session, SQLModel, create_engine, select, column
import sqlalchemy as sa
from sqlalchemy.sql import func
from sqlalchemy import DateTime
from pydantic import BaseModel

class PaymentMethodBase(SQLModel):
    name: str 
    icon: str
    active: bool 
    description: str
    exonerated: bool
    

class PaymentMethod(PaymentMethodBase, table=True):
    __tablename__ = 'PaymentMethod' # type: ignore
    id: int | None = Field(default=None, primary_key=True)
    created_at: datetime | None = Field(default_factory=lambda: datetime.now())
    created_by: int | None = Field(default=None, foreign_key='User.id')
    updated_at: datetime | None = Field(default=None, sa_column=Column(DateTime(), onupdate=func.now()))
    updated_by: int | None = Field(default=None, foreign_key='User.id')

class PaymentMethodPublic(PaymentMethodBase):
    id: int
    

class PaymentMethodCreate(PaymentMethodBase):
    pass

class PaymentMethodUpdate(PaymentMethodBase):
    name: str | None = None # type: ignore[assignment]
    icon:str | None = None
    active: bool | None = None # type: ignore[assignment]
    updated_by: int | None = None
    exonerated: bool | None = None

class Metadata(BaseModel):
    page: int
    total: int
    per_page: int
    total_pages: int
    search: str

class PaymentMethodResponse(BaseModel):
    metadata: Metadata
    data: List[PaymentMethodPublic]
    description: str | None = None
