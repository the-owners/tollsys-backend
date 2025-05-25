from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, TYPE_CHECKING
from datetime import datetime

if TYPE_CHECKING:
    from src.roles.models import Role
    from src.permissions.models import Permission

class RolePermissionBase(SQLModel):
    role_id: int = Field(foreign_key="role.id")
    permission_id: int = Field(foreign_key="permission.id")

class RolePermission(RolePermissionBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    created_by: int
    updated_at: Optional[datetime] = None
    updated_by: Optional[int] = None
    
    role: "Role" = Relationship(back_populates="permissions")
    permission: "Permission" = Relationship(back_populates="roles")


class RolePermissionCreate(RolePermissionBase):
    pass

class RolePermissionRead(RolePermissionBase):
    id: int
    created_at: datetime
    created_by: int

class RolePermissionUpdate(SQLModel):
    role_id: Optional[int] = None
    permission_id: Optional[int] = None