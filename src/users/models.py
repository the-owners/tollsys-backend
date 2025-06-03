from typing import TYPE_CHECKING

from sqlmodel import Field, Relationship, SQLModel

from src.core.models import TimestampMixin
from src.roles.models import RolePublic
from src.tolls.models import TollPublic

if TYPE_CHECKING:
    from src.roles.models import Role


class UserBase(SQLModel):
    name: str
    username: str
    role_id: int | None = Field(default=None, foreign_key="Role.id", index=True)
    toll_id: int | None = Field(default=None, foreign_key="Toll.id", index=True)


class User(TimestampMixin, UserBase, table=True):
    __tablename__: str = "User"

    id: int | None = Field(default=None, primary_key=True)
    name: str | None = Field(default=None, unique=True)
    password: str | None

    # Define the relationship to Role
    # This lets you do user.role to get the associated Role object
    role: "Role" = Relationship(
        back_populates="users",
        sa_relationship_kwargs={
            "foreign_keys": "User.role_id"  # This tells SQLAlchemy which column is the FK
            # If you were importing User into this file (circular import issue)
            # you might need to use a lambda or string for the column object.
            # Example for SQLAlchemy: "foreign_keys": [lambda: User.role_id]
            # But for SQLModel, the string 'User.role_id' generally works.
        },
    )


class UserCreate(UserBase):
    password: str


class UserUpdate(SQLModel):
    name: str | None = None
    username: str | None = None
    password: str | None = None
    role_id: int | None = None
    toll_id: int | None = None


class UserPublic(UserBase):
    id: int
    role: RolePublic | None = None
    toll: TollPublic | None = None


class ChangePasswordRequest(SQLModel):
    current_password: str
    new_password: str
    new_password_confirm: str
