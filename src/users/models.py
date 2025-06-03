from sqlmodel import Field, SQLModel

from src.core.models import TimestampMixin
from src.roles.models import RolePublic
from src.tolls.models import TollPublic


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
