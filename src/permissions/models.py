from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List, TYPE_CHECKING
from datetime import datetime

if TYPE_CHECKING:
    from src.role_permissions.models import RolePermission

class PermissionBase(SQLModel):
    name: str = Field(index=True, max_length=50)
    description: Optional[str] = Field(default=None, max_length=255)

class Permission(PermissionBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: Optional[datetime] = None
    
    roles: List["RolePermission"] = Relationship(back_populates="permission")

class PermissionCreate(PermissionBase):
    pass

class PermissionRead(PermissionBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime]

class PermissionUpdate(SQLModel):
    name: Optional[str] = None
    description: Optional[str] = None