from pydantic import BaseModel
from sqlmodel import Field, SQLModel

from src.core.models import MetadataMixin, TimestampMixin


class PaymentMethodBase(SQLModel):
    name: str
    icon: str
    active: bool
    description: str
    exonerated: bool


class PaymentMethod(TimestampMixin, PaymentMethodBase, table=True):
    __tablename__: str = "PaymentMethod"  # type: ignore
    id: int | None = Field(default=None, primary_key=True)


class PaymentMethodPublic(PaymentMethodBase):
    id: int


class PaymentMethodCreate(PaymentMethodBase):
    pass


class PaymentMethodUpdate(PaymentMethodBase):
    name: str | None = None
    icon: str | None = None
    active: bool | None = None
    description: str | None = None
    exonerated: bool | None = None


class PaymentMethodResponse(BaseModel):
    metadata: MetadataMixin
    data: list[PaymentMethodPublic]
