from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List, TYPE_CHECKING

if TYPE_CHECKING:
    from src.permissions.models import PermissionRead
from datetime import datetime

if TYPE_CHECKING:
    from src.users.models import User
    from src.role_permissions.models import RolePermission

class RoleBase(SQLModel):
    name: str = Field(
        index=True,
        max_length=50,
        nullable=False,
        sa_column_kwargs={"unique": True}  # Asegura nombres únicos
    )
    description: Optional[str] = Field(
        default=None,
        max_length=255,
        nullable=True
    )

class Role(RoleBase, table=True):
    __tablename__ = "Role"  # Nombre explícito en plural
    
    id: Optional[int] = Field(
        default=None,
        primary_key=True,
        nullable=False
    )
    created_at: datetime = Field(
        default_factory=datetime.utcnow,
        nullable=False,
        sa_column_kwargs={"server_default": "CURRENT_TIMESTAMP"}
    )
    created_by: int = Field(
        foreign_key="User.id",
        nullable=False
    )
    updated_at: Optional[datetime] = Field(
        default=None,
        nullable=True
    )
    updated_by: Optional[int] = Field(
        default=None,
        foreign_key="User.id",
        nullable=True
    )
    
    # Relaciones mejor definidas
    users: List["User"] = Relationship(
        back_populates="role",
        sa_relationship_kwargs={"lazy": "selectin"}  # Mejor carga de relaciones
    )
    permissions: List["RolePermission"] = Relationship(
        back_populates="role",
        sa_relationship_kwargs={
            "lazy": "selectin",
            "cascade": "all, delete-orphan"
        }
    )

class RoleCreate(RoleBase):
    created_by: int  # Campo requerido para creación

class RoleRead(RoleBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime]
    created_by: int
    updated_by: Optional[int]

class RoleUpdate(SQLModel):
    name: Optional[str] = Field(
        default=None,
        max_length=50,
        description="Nuevo nombre para el rol"
    )
    description: Optional[str] = Field(
        default=None,
        max_length=255,
        description="Nueva descripción para el rol"
    )
    updated_by: Optional[int] = Field(
        default=None,
        description="ID del usuario que actualiza"
    )

class RolePublic(RoleRead):
    permissions: List["PermissionRead"] = Field(
        default_factory=list,
        description="Lista de permisos asignados"
    )