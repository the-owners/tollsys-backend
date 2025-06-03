from typing import TYPE_CHECKING

from sqlmodel import (
    Field,
    Relationship,
    SQLModel,
)

from src.core.models import TimestampMixin

if TYPE_CHECKING:
    from src.toll_payments.models import TollPayment


class TollBase(SQLModel):
    tax_id: str
    legal_name: str
    address: str


class Toll(TimestampMixin, TollBase, table=True):
    __tablename__: str = "Toll"
    id: int | None = Field(default=None, primary_key=True)
    tax_id: str = Field(index=True)
    toll_payments: list["TollPayment"] = Relationship(back_populates="toll")


class TollPublic(TollBase):
    id: int


class TollCreate(TollBase):
    pass


class TollUpdate(TollBase):
    tax_id: str | None = None
    legal_name: str | None = None
    address: str | None = None
