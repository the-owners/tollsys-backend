from typing import TYPE_CHECKING

from sqlmodel import Field, Relationship, SQLModel

from src.core.models import TimestampMixin

if TYPE_CHECKING:
    from src.role_permissions.models import RolePermission
    from src.users.models import User


class Role(TimestampMixin, SQLModel, table=True):
    __tablename__: str = "Role"

    id: int | None = Field(default=None, primary_key=True)
    name: str | None = Field(index=True)
    # Define relationship to User (one-to-many: one role can have many users)
    users: list["User"] = Relationship(
        back_populates="role",
        sa_relationship_kwargs={"foreign_keys": "User.role_id"},
    )

    # Define relationship to RolePermission (one-to-many: one role can have many RolePermissions)
    role_permissions: list["RolePermission"] = Relationship(back_populates="role")


class RolePublic(SQLModel):
    id: int | None = None
    name: str | None = None


class RoleCreate(SQLModel):
    name: str
