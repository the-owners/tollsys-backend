from __future__ import annotations
from datetime import datetime
from typing import Optional, List
from sqlmodel import SQLModel, Field, Relationship

#audit mixin cummons fields for all models
class AuditMixin(SQLModel):
    id: Optional[int] = Field(default=None, primary_key=True)
    created_at: datetime = Field(
        default_factory=datetime.utcnow,
        sa_column_kwargs={"server_default": "now()"}
    )
    created_by: int = Field(foreign_key="user.id", nullable=False)
    updated_at: datetime = Field(
        default_factory=datetime.utcnow,
        sa_column_kwargs={
            "server_default": "now()",
            "onupdate": datetime.utcnow,
            "server_onupdate": "now()"
        }
    )
    updated_by: int = Field(foreign_key="user.id", nullable=False)


class User(AuditMixin, table=True):
    __tablename__ = "user"

    username: str = Field(index=True, unique=True, max_length=50)
    hashed_password: str = Field(max_length=255)
    name: str = Field(max_length=100)
    role_id: int = Field(foreign_key="role.id", nullable=False)
    toll_id: int = Field(foreign_key="toll.id", nullable=False)
    is_active: bool = Field(default=True)

    role:    Role            = Relationship(back_populates="users")
    toll:    Toll            = Relationship(back_populates="users")
    sessions: List[UserSession] = Relationship(back_populates="user")


class UserSession(AuditMixin, table=True):
    __tablename__ = "user_session"

    user_id: int               = Field(foreign_key="user.id", nullable=False)
    closed_at: Optional[datetime] = None
    closing_reason: Optional[str] = Field(max_length=255)

    user: User = Relationship(back_populates="sessions")


class Role(AuditMixin, table=True):
    __tablename__ = "role"

    name: str = Field(index=True, unique=True, max_length=50)

    users:       List[User]           = Relationship(back_populates="role")
    permissions: List[RolePermission] = Relationship(back_populates="role")


class Permission(AuditMixin, table=True):
    __tablename__ = "permission"

    name: str        = Field(unique=True, max_length=50)
    description: str = Field(max_length=255)

    role_permissions: List[RolePermission] = Relationship(back_populates="permission")


class RolePermission(SQLModel, table=True):
    __tablename__ = "role_permission"

    role_id:       int = Field(foreign_key="role.id",       primary_key=True)
    permission_id: int = Field(foreign_key="permission.id", primary_key=True)

    created_at: datetime = Field(
        default_factory=datetime.utcnow,
        sa_column_kwargs={"server_default":"now()"}
    )
    created_by: int      = Field(foreign_key="user.id", nullable=False)
    updated_at: datetime = Field(
        default_factory=datetime.utcnow,
        sa_column_kwargs={
            "server_default":"now()",
            "onupdate": datetime.utcnow,
            "server_onupdate":"now()"
        }
    )
    updated_by: int = Field(foreign_key="user.id", nullable=False)

    role:       Role       = Relationship(back_populates="permissions")
    permission: Permission = Relationship(back_populates="role_permissions")

#Forward references
User.update_forward_refs()
UserSession.update_forward_refs()
Role.update_forward_refs()
Permission.update_forward_refs()
RolePermission.update_forward_refs()




