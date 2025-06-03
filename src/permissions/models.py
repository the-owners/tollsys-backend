from enum import Enum
from typing import TYPE_CHECKING

from sqlmodel import Field, Relationship, SQLModel

from src.core.models import TimestampMixin

if TYPE_CHECKING:
    from src.role_permissions.models import RolePermission


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
    role_permissions: list["RolePermission"] = Relationship(back_populates="permission")


class PermissionCreate(PermissionBase):
    name: str


class PermissionUpdate(PermissionBase):
    pass


class PermissionPublic(PermissionBase):
    id: int
