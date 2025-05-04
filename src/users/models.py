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
  role_id: int | None = Field(default=None, foreign_key='Role.id')
  toll_id: int | None = Field(default=None, foreign_key='Toll.id')
  created_at: datetime.datetime | None = Field(default=datetime.datetime.now)
  created_by: int | None = Field(default=None, foreign_key='User.id')
  updated_at: datetime.datetime | None = Field(sa_column=Column(DateTime(), onupdate=func.now()))
  updated_by: int | None = Field(default=None, foreign_key='User.id')


class User(UserBase, table=True):
  __tablename__ = 'User'

  id: int | None = Field(default=None, primary_key=True)
  password: str | None

  __table_args__ = (
  Index('idx_user_username', 'username'),
  Index('idx_user_role_id', 'role_id'),
  Index('idx_user_toll_id', 'toll_id'),
  Index('idx_user_created_by', 'created_by'),
  Index('idx_user_updated_by', 'updated_by'),
  )

class UserPublic(UserBase):
  id: int
  name: str
  username: str
  role_id: int
  toll_id: int
  # this shouldn't be nullable but fastapi crashes for some reason
  created_at: datetime.datetime | None
  created_by: int | None
  updated_at: datetime.datetime | None
  updated_by: int | None


class UserCreate(UserBase):
  name: str
  username: str
  password: str
  role_id: int
  toll_id: int
  created_by: int # this should be automatically picked up from the current user but i'll leave it like this for now
  # ditto for updated_by

class UserUpdate(UserBase):
  name: str | None = None # type: ignore[assignment]
  username: str | None = None # type: ignore[assignment]
  password: str | None = None # type: ignore[assignment]
  role_id: int | None = None # type: ignore[assignment]
  toll_id: int | None = None # type: ignore[assignment]
  updated_by: int | None = None # type: ignore[assignment]
