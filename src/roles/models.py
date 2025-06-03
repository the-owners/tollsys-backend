from sqlmodel import Field, SQLModel

from src.core.models import TimestampMixin


class Role(TimestampMixin, SQLModel, table=True):
    __tablename__: str = "Role"

    id: int | None = Field(default=None, primary_key=True)
    name: str | None = Field(index=True)


class RolePublic(SQLModel):
    id: int | None = None
    name: str | None = None


class RoleCreate(SQLModel):
    name: str
