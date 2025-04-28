from typing import Annotated
from datetime import datetime
from fastapi import Depends, HTTPException, Query
from sqlmodel import Field, Session, SQLModel, create_engine, select

class PaymentMethodBase(SQLModel):
    name: str = Field(index=True)
    active: bool = Field(default=True)

class PaymentMethod(PaymentMethodBase, table=True):
    id: int | None = Field(default=None, primary_key=True)

class PaymentMethodPublic(PaymentMethodBase):
    id: int

class PaymentMethodCreate(PaymentMethodBase):
    name: str
    active: bool

# nullable to allow for partial update, but
# here we ignore sum shit cuz mypy gets obnoxious otherwise
class PaymentMethodUpdate(PaymentMethodBase):
    name: str | None = None # type: ignore[assignment]
    active: bool | None = None # type: ignore[assignment]
