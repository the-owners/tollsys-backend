import datetime
import decimal
from typing import Optional
from sqlmodel import Field, SQLModel
from enum import Enum
import sqlalchemy as sa
from sqlalchemy.sql import func
from sqlalchemy import Index

class PermissionEnum(str, Enum):
    # Administración
    MANAGE_USERS = "manage_users"
    MANAGE_ROLES = "manage_roles"
    MANAGE_TOLLS = "manage_tolls"
    
    # Operaciones
    PROCESS_PAYMENT = "process_payment"
    GENERATE_REPORTS = "generate_reports"
    
    # Consultas
    VIEW_TRANSACTIONS = "view_transactions"
    VIEW_OWN_DATA = "view_own_data"


class PermissionBase(SQLModel):
    pass

class Permission(SQLModel, table=True):

    __tablename__ = 'Permission'

    id: Optional[int] = Field(default=None, primary_key=True)
    name: Optional[str]
    created_at: Optional[datetime.datetime] = Field(default=None)
    updated_at: Optional[datetime.datetime] = Field(default=None)

    __table_args__ = (
    Index('idx_permission_name', 'name'),
            )