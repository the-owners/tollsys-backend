from typing import Annotated
from datetime import datetime
from fastapi import Depends, HTTPException, Query
from sqlmodel import Column, Field, Session, SQLModel, create_engine, select, column
import sqlalchemy as sa
from sqlalchemy.sql import func
from sqlalchemy import DateTime


class BoothBase(SQLModel):
    name: str 
    active: bool 
    status: str 
    toll_id: int | None = Field(default=None, foreign_key='Toll.id')

class Booth(BoothBase, table=True):
    __tablename__ = 'Booth'
    id: int | None = Field(default=None, primary_key=True)
    name: str 
    active: bool 
    status: str
    toll_id: int | None = Field(default=None, foreign_key='Toll.id')
    created_at: datetime | None = Field(default_factory=lambda: datetime.now())
    created_by: int | None = Field(default=None, foreign_key='User.id')
    updated_at: datetime | None = Field(default=None, sa_column=Column(DateTime(), onupdate=func.now()))
    updated_by: int | None = Field(default=None, foreign_key='User.id')

class BoothPublic(BoothBase):
    id: int
    name: str
    status: str
    active: bool 
    toll_id: int
    created_at: datetime | None
    created_by: int | None
    updated_at: datetime | None
    updated_by: int | None
    

class BoothCreate(BoothBase):
    name: str
    status: str
    active: bool 
    toll_id: int

class BoothUpdate(BoothBase):
    name: str| None = None
    status: str| None = None
    active: bool | None = None
    toll_id: int| None = None
    updated_by: int | None = None
