import datetime
import decimal
from enum import Enum
from typing import TYPE_CHECKING, Sequence

import sqlalchemy as sa
from pydantic import BaseModel
from sqlmodel import Field, Relationship, SQLModel

from src.core.models import MetadataMixin, TimestampMixin

if TYPE_CHECKING:
    from src.toll_payments.models import TollPayment


class BoothStatus(str, Enum):
    AVAILABLE = "AVAILABLE"
    CLOSED = "CLOSED"
    MAINTENANCE = "MAINTENANCE"
    OCCUPIED = "OCCUPIED"


class BoothBase(SQLModel):
    name: str
    active: bool
    status: BoothStatus
    toll_id: int


class Booth(TimestampMixin, BoothBase, table=True):
    __tablename__: str = "Booth"

    id: int | None = Field(default=None, primary_key=True)
    name: str | None
    active: bool | None
    status: BoothStatus | None = Field(sa_type=sa.Enum(BoothStatus))  # type: ignore
    toll_id: int | None = Field(foreign_key="Toll.id", index=True)
    toll_payments: list["TollPayment"] = Relationship(back_populates="booth")


class BoothPublic(BoothBase):
    id: int


class BoothCreate(BoothBase):
    pass


class BoothUpdate(BoothBase):
    id: int


class BoothResponse(BaseModel):
    metadata: MetadataMixin
    data: Sequence[BoothPublic]
    description: str | None = None


class BoothCashSession(TimestampMixin, SQLModel, table=True):
    __tablename__: str = "BoothCashSession"  # type: ignore

    id: int | None = Field(default=None, primary_key=True)
    booth_id: int = Field(foreign_key="Booth.id", index=True)
    user_id: int = Field(foreign_key="User.id", index=True)
    opened_at: datetime.datetime
    initial_amount: decimal.Decimal | None = Field(sa_type=sa.Numeric())  # type: ignore
    closing_amount: decimal.Decimal | None = Field(sa_type=sa.Numeric())  # type: ignore
    closing_reason: str | None
    closing_observations: str | None = Field(sa_type=sa.Text())  # type: ignore
    closed_at: datetime.datetime | None
