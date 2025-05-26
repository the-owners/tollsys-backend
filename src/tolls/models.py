from typing import Annotated
from datetime import datetime
from fastapi import Depends, HTTPException, Query
from sqlmodel import Column, Field, Session, SQLModel, create_engine, select, column, Index
import sqlalchemy as sa
from sqlalchemy.sql import func
from sqlalchemy import DateTime

class TollBase(SQLModel):
    tax_id: str 
    legal_name: str
    address: str
    

class Toll(TollBase, table=True):
    __tablename__ = 'Toll'
    id: int | None = Field(default=None, primary_key=True)
    tax_id: str 
    legal_name: str
    address: str
    created_at: datetime | None = Field(default_factory=lambda: datetime.now())
    created_by: int | None = Field(default=None, foreign_key='User.id')
    updated_at: datetime | None = Field(default=None, sa_column=Column(DateTime(), onupdate=func.now()))
    updated_by: int | None = Field(default=None, foreign_key='User.id')

    __table_args__ = (
                
    Index('idx_toll_tax_id', 'tax_id'),
    Index('idx_toll_created_by', 'created_by'),
    Index('idx_toll_updated_by', 'updated_by'),
            )


class TollPublic(TollBase):
    id: int
    tax_id: str 
    legal_name: str
    address: str


class TollCreate(TollBase):
    tax_id: str 
    legal_name: str
    address: str


class TollUpdate(TollBase):
    tax_id: str | None = None # type: ignore[assignment]
    legal_name:str | None = None
    address: str | None = None
    updated_by: int | None = None
