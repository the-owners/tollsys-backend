import datetime
import decimal
from typing import Optional
from sqlmodel import Field, SQLModel
from enum import Enum
import sqlalchemy as sa
from sqlalchemy.sql import func
from sqlalchemy import Index
class User(SQLModel, table=True):

    __tablename__ = 'User'

    id: Optional[int] = Field(default=None, primary_key=True)
    name: Optional[str]
    username: Optional[str]
    password: Optional[str]
    role_id: Optional[int] = Field(foreign_key='Role.id')
    toll_id: Optional[int] = Field(foreign_key='Toll.id')
    created_at: Optional[datetime.datetime]
    created_by: Optional[int] = Field(foreign_key='User.id')
    updated_at: Optional[datetime.datetime]
    updated_by: Optional[int] = Field(foreign_key='User.id')

    __table_args__ = (
                
    Index('idx_user_username', 'username'),
    Index('idx_user_role_id', 'role_id'),
    Index('idx_user_toll_id', 'toll_id'),
    Index('idx_user_created_by', 'created_by'),
    Index('idx_user_updated_by', 'updated_by'),
            )



class UserSession(SQLModel, table=True):

    __tablename__ = 'UserSession'

    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key='User.id')
    created_at: Optional[datetime.datetime] = Field(sa_column_kwargs={'server_default': func.now()})
    created_by: Optional[int] = Field(foreign_key='User.id')
    updated_at: Optional[datetime.datetime]
    updated_by: Optional[int] = Field(foreign_key='User.id')
    closed_at: Optional[datetime.datetime]
    closing_reason: Optional[str]
    closing_observations: Optional[str] = Field(sa_type=sa.Text())

    __table_args__ = (
                
    Index('idx_user_session_user_id', 'user_id'),
    Index('idx_user_session_created_by', 'created_by'),
    Index('idx_user_session_updated_by', 'updated_by'),
            )



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



class Permission(SQLModel, table=True):

    __tablename__ = 'Permission'

    id: Optional[int] = Field(default=None, primary_key=True)
    name: Optional[str]
    created_at: Optional[datetime.datetime]
    updated_at: Optional[datetime.datetime]

    __table_args__ = (
                
    Index('idx_permission_name', 'name'),
            )


class RolePermission(SQLModel, table=True):

    __tablename__ = 'RolePermission'

    id: Optional[int] = Field(default=None, primary_key=True)
    role_id: Optional[int] = Field(foreign_key='Role.id')
    permission_id: Optional[int] = Field(foreign_key='Permission.id')
    created_at: Optional[datetime.datetime]
    created_by: Optional[int] = Field(foreign_key='User.id')
    updated_at: Optional[datetime.datetime]
    updated_by: Optional[int] = Field(foreign_key='User.id')

    __table_args__ = (
                
    Index('idx_role_permission_role_id', 'role_id'),
    Index('idx_role_permission_permission_id', 'permission_id'),
    Index('idx_role_permission_created_by', 'created_by'),
    Index('idx_role_permission_updated_by', 'updated_by'),
            )