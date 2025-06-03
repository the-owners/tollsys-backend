import decimal
import uuid
from datetime import datetime
from typing import TYPE_CHECKING

from sqlmodel import Field, Relationship, SQLModel

from src.booths.models import BoothPublic
from src.core.models import TimestampMixin
from src.payment_methods.models import PaymentMethodPublic
from src.tolls.models import TollPublic
from src.vehicle_types.models import VehicleTypePublic

if TYPE_CHECKING:
    from src.booths.models import Booth
    from src.tolls.models import Toll
    from src.vehicle_types.models import VehicleType


class TollPaymentBase(SQLModel):
    booth_id: int = Field(foreign_key="Booth.id")
    toll_id: int = Field(foreign_key="Toll.id")
    car_type_id: int = Field(foreign_key="VehicleType.id")


# Just to be clear:
# These PaymentMethodTP classes are what we call TollPaymentMethod in the spec
# Should be moved to toll_payment_methods , but won't do as there's a huge
#  rework/rename of major classes pending
# ~Derwins


class PaymentMethodTP(SQLModel, table=True):
    __tablename__: str = "PaymentMethodTP"
    id: int | None = Field(default=None, primary_key=True)
    toll_payment_id: int = Field(foreign_key="TollPayment.id")
    payment_method_id: int = Field(foreign_key="PaymentMethod.id")
    amount: decimal.Decimal = Field(default=0)

    toll_payment: "TollPayment" = Relationship(back_populates="amounts")


class PaymentMethodTPCreate(SQLModel):
    payment_method_id: int
    value: decimal.Decimal


class PaymentMethodTPWrapper(SQLModel):
    """
    Wraps a PaymentMethodPublic object under the 'payment_method' key
    for the desired API response format.
    """

    payment_method: PaymentMethodPublic
    amount: decimal.Decimal


class TollPayment(TimestampMixin, TollPaymentBase, table=True):
    __tablename__: str = "TollPayment"
    id: int | None = Field(default=None, primary_key=True)
    receipt_nro: str | None = Field(
        unique=True, default_factory=lambda: str(uuid.uuid4())
    )
    booth: "Booth" = Relationship(back_populates="toll_payments")  # type: ignore
    toll: "Toll" = Relationship(back_populates="toll_payments")  # type: ignore
    car_type: "VehicleType" = Relationship(back_populates="toll_payments")  # type: ignore
    amounts: list[PaymentMethodTP] = Relationship(back_populates="toll_payment")


class TollPaymentCreate(SQLModel):
    car_type_id: int
    multiple_payment_methods: bool
    amounts: list[
        PaymentMethodTPCreate
    ]  # List of dictionaries with payment_method_id and amount


class TollPaymentPublic(SQLModel):
    id: int
    receipt_nro: str
    toll: "TollPublic"
    booth: "BoothPublic"
    car_type: "VehicleTypePublic"
    amounts: list[PaymentMethodTPWrapper]
    created_at: datetime
