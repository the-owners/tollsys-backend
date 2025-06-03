from sqlmodel import Field, Relationship, SQLModel

from src.core.models import TimestampMixin
from src.permissions.models import Permission
from src.roles.models import Role


class RolePermissionBase(SQLModel):
    role_id: int | None = Field(default=None, foreign_key="Role.id", index=True)
    permission_id: int | None = Field(
        default=None, foreign_key="Permission.id", index=True
    )


class RolePermission(TimestampMixin, RolePermissionBase, table=True):
    __tablename__: str = "RolePermission"

    # Define the Relationship to the Role model
    # This creates the 'role' property on RolePermission instances
    role: Role = Relationship(back_populates="role_permissions")

    # Define the Relationship to the Permission model
    # This creates the 'permission' property on RolePermission instances
    permission: Permission = Relationship(back_populates="role_permissions")

    id: int | None = Field(default=None, primary_key=True)


class RolePermissionCreate(RolePermissionBase):
    role_id: int
    permission_id: int


class RolePermissionUpdate(RolePermissionBase):
    pass


class RolePermissionPublic(RolePermissionBase):
    id: int
