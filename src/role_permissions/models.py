from sqlmodel import Field, SQLModel

from src.core.models import TimestampMixin


class RolePermissionBase(SQLModel):
    role_id: int | None = Field(default=None, foreign_key="Role.id", index=True)
    permission_id: int | None = Field(
        default=None, foreign_key="Permission.id", index=True
    )


class RolePermission(TimestampMixin, RolePermissionBase, table=True):
    __tablename__: str = "RolePermission"

    id: int | None = Field(default=None, primary_key=True)


class RolePermissionCreate(RolePermissionBase):
    role_id: int
    permission_id: int


class RolePermissionUpdate(RolePermissionBase):
    pass


class RolePermissionPublic(RolePermissionBase):
    id: int
