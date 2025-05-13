from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List, TYPE_CHECKING
from datetime import datetime

if TYPE_CHECKING:
    from src.users.models import User
    from src.role_permissions.models import RolePermission

class RoleBase(SQLModel):
    name: str = Field(index=True, max_length=50)
    description: Optional[str] = Field(default=None, max_length=255)

class Role(RoleBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    created_by: int
    updated_at: Optional[datetime] = None
    updated_by: Optional[int] = None
    
    users: List["User"] = Relationship(back_populates="role")
    permissions: List["RolePermission"] = Relationship(back_populates="role")

class RoleCreate(RoleBase):
    pass

class RoleRead(RoleBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime]

class RoleUpdate(SQLModel):
    name: Optional[str] = None
    description: Optional[str] = None

class RolePublic(RoleBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime]