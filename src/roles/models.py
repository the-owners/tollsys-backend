import datetime
import decimal
from typing import Optional
from sqlmodel import Field, SQLModel
from enum import Enum
import sqlalchemy as sa
from sqlalchemy.sql import func
from sqlalchemy import Index

class Role(SQLModel, table=True):

    __tablename__ = 'Role'

    id: Optional[int] = Field(default=None, primary_key=True)
    name: Optional[str]
    created_at: Optional[datetime.datetime]
    created_by: Optional[int] = Field(foreign_key='User.id')
    updated_at: Optional[datetime.datetime]
    updated_by: Optional[int] = Field(foreign_key='User.id')

    __table_args__ = (
                
    Index('idx_role_name', 'name'),
    Index('idx_role_created_by', 'created_by'),
    Index('idx_role_updated_by', 'updated_by'),
    )
