import datetime
import decimal
from typing import Optional
from sqlmodel import Field, SQLModel, Column
from enum import Enum
import sqlalchemy as sa
from sqlalchemy.sql import func
from sqlalchemy import Index, DateTime
from ..tolls.models import *
from ..roles.models import *

class UserBase(SQLModel):
    name: str
    username: str
    role_id: Optional[int] = Field(default=None, foreign_key='Role.id')
    toll_id: Optional[int] = Field(default=None, foreign_key='Toll.id')

class User(UserBase, table=True):
    __tablename__ = 'User'

    id: Optional[int] = Field(default=None, primary_key=True)
    password: Optional[str]

    # Unique constraint en username
    __table_args__ = (
        Index('uq_user_username', 'username', unique=True),
        Index('idx_user_role_id', 'role_id'),
        Index('idx_user_toll_id', 'toll_id'),
        Index('idx_user_created_by', 'created_by'),
        Index('idx_user_updated_by', 'updated_by'),
    )

    # Timestamps y auditoría
    created_at: datetime.datetime = Field(
        default_factory=datetime.datetime.utcnow
    )
    created_by: Optional[int] = Field(default=None, foreign_key='User.id')
    updated_at: Optional[datetime.datetime] = Field(
        default=None,
        sa_column=Column(DateTime(), onupdate=func.now())
    )
    updated_by: Optional[int] = Field(default=None, foreign_key='User.id')

class UserCreate(UserBase):
    password: str

class UserUpdate(SQLModel):
    name: Optional[str] = None
    username: Optional[str] = None
    password: Optional[str] = None
    role_id: Optional[int] = None
    toll_id: Optional[int] = None

class UserPublic(UserBase):
    id: int
    role: Optional[RolePublic] = None
    toll: Optional[TollPublic] = None
