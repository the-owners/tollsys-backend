import datetime
import decimal
from typing import Optional
from sqlmodel import Field, SQLModel
from enum import Enum
import sqlalchemy as sa
from sqlalchemy.sql import func
from sqlalchemy import Index
from ..tolls.models import *
from ..roles.models import *

class UserBase(SQLModel):
  pass


class User(SQLModel, table=True):

    __tablename__ = 'User'

    id: Optional[int] = Field(default=None, primary_key=True)
    name: Optional[str]
    username: Optional[str]
    password: Optional[str]
    role_id: int | None = Field(default=None, foreign_key='Role.id')
    toll_id: Optional[int] = Field(default=None, foreign_key='Toll.id')
    created_at: Optional[datetime.datetime]
    created_by: Optional[int] = Field(default=None, foreign_key='User.id')
    updated_at: Optional[datetime.datetime]
    updated_by: Optional[int] = Field(default=None, foreign_key='User.id')

    __table_args__ = (
                
    Index('idx_user_username', 'username'),
    Index('idx_user_role_id', 'role_id'),
    Index('idx_user_toll_id', 'toll_id'),
    Index('idx_user_created_by', 'created_by'),
    Index('idx_user_updated_by', 'updated_by'),
            )
