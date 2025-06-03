from enum import Enum

from sqlmodel import Field, SQLModel

from src.core.models import TimestampMixin


class PermissionEnum(str, Enum):
    MANAGE_USERS = "manage_users"
    MANAGE_ROLES = "manage_roles"
    MANAGE_TOLLS = "manage_tolls"
    PROCESS_PAYMENT = "process_payment"
    GENERATE_REPORTS = "generate_reports"
    VIEW_TRANSACTIONS = "view_transactions"
    VIEW_OWN_DATA = "view_own_data"


class PermissionBase(SQLModel):
    name: str | None = Field(default=None, index=True)


class Permission(TimestampMixin, PermissionBase, table=True):
    __tablename__: str = "Permission"

    id: int | None = Field(default=None, primary_key=True)


class PermissionCreate(PermissionBase):
    name: str


class PermissionUpdate(PermissionBase):
    pass


class PermissionPublic(PermissionBase):
    id: int
