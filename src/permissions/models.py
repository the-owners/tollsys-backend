import datetime
from typing import Optional
from sqlmodel import Field, SQLModel, Index
from enum import Enum


class PermissionEnum(str, Enum):
    MANAGE_USERS = "manage_users"
    MANAGE_ROLES = "manage_roles"
    MANAGE_TOLLS = "manage_tolls"
    PROCESS_PAYMENT = "process_payment"
    GENERATE_REPORTS = "generate_reports"
    VIEW_TRANSACTIONS = "view_transactions"
    VIEW_OWN_DATA = "view_own_data"


class PermissionBase(SQLModel):
    name: Optional[str] = None


class Permission(PermissionBase, table=True):
    __tablename__ = "Permission"

    id: Optional[int] = Field(default=None, primary_key=True)
    created_at: Optional[datetime.datetime] = Field(default_factory=datetime.datetime.utcnow)
    updated_at: Optional[datetime.datetime] = Field(default_factory=datetime.datetime.utcnow)

    __table_args__ = (Index('idx_permission_name', 'name'),)


class PermissionCreate(PermissionBase):
    name: str


class PermissionUpdate(PermissionBase):
    pass


class PermissionPublic(PermissionBase):
    id: int
