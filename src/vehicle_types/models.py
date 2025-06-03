from typing import TYPE_CHECKING

from pydantic import BaseModel
from sqlmodel import (
    Field,
    Relationship,
    SQLModel,
)

from src.core.models import MetadataMixin, TimestampMixin

if TYPE_CHECKING:
    from src.toll_payments.models import TollPayment


class VehicleTypeBase(SQLModel):
    name: str
    icon: str
    rate: float
    active: bool


class VehicleType(TimestampMixin, VehicleTypeBase, table=True):
    __tablename__: str = "VehicleType"
    id: int | None = Field(default=None, primary_key=True)
    toll_payments: list["TollPayment"] = Relationship(back_populates="car_type")


class VehicleTypePublic(VehicleTypeBase):
    id: int


class VehicleTypeCreate(VehicleTypeBase):
    pass


class VehicleTypeUpdate(VehicleTypeBase):
    name: str | None = None
    icon: str | None = None
    rate: float | None = None
    active: bool | None = None


class VehicleTypeResponse(BaseModel):
    metadata: MetadataMixin
    data: list[VehicleTypePublic]
