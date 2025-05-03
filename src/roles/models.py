from enum import Enum
from sqlmodel import Field, SQLModel, Relationship
from typing import List, Optional
import datetime

class SystemRoles(str, Enum):               # Roles como enumeración para evitar errores de texto.
    ADMIN = "admin"                         # str como clase padre para serialización JSON automática.
    CASHIER = "taquillero"
    USER = "usuario"

class PermissionBase(SQLModel):
    name: str = Field(unique=True, index=True)
    description: str

class Permission(PermissionBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    created_at: datetime.datetime = Field(default_factory=datetime.utcnow)
    roles: List["Role"] = Relationship(back_populates="permissions", link_model=RolePermission)

class RoleBase(SQLModel):
    name: SystemRoles = Field(unique=True, index=True)
    description: str

class Role(RoleBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    created_at: datetime.datetime = Field(default_factory=datetime.utcnow)
    users: List["User"] = Relationship(back_populates="role")
    permissions: List[Permission] = Relationship(back_populates="roles", link_model=RolePermission)

class RolePermission(SQLModel, table=True):
    role_id: int = Field(foreign_key="role.id", primary_key=True)
    permission_id: int = Field(foreign_key="permission.id", primary_key=True)
    granted_at: datetime.datetime = Field(default_factory=datetime.utcnow)                          #posibles roles