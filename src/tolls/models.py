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

class TollPublic(SQLModel):
    id: int | None = None
    legal_name: str | None = Field(default=None, alias="legal_name")