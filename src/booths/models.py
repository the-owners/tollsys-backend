import datetime
import decimal
from pydantic import BaseModel
from sqlmodel import Column, DateTime, Field, SQLModel
from enum import Enum
import sqlalchemy as sa
from sqlalchemy.sql import func
from sqlalchemy import Index


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


class Booth(BoothBase, table=True):

    __tablename__ = "Booth"

    id: int | None = Field(default=None, primary_key=True)
    name: str | None
    active: bool | None
    status: BoothStatus | None = Field(sa_type=sa.Enum(BoothStatus))
    toll_id: int | None = Field(foreign_key="Toll.id")
    created_at: datetime.datetime | None = Field(default_factory=lambda: datetime.now())
    created_by: int | None = Field(default=None, foreign_key="User.id")
    updated_at: datetime.datetime | None = Field(
        default=None, sa_column=Column(DateTime(), onupdate=func.now())
    )
    updated_by: int | None = Field(default=None, foreign_key="User.id")

    __table_args__ = (
        Index("idx_booth_toll_id", "toll_id"),
        Index("idx_booth_created_by", "created_by"),
        Index("idx_booth_updated_by", "updated_by"),
    )


class BoothPublic(BoothBase):
    id: int


class BoothCreate(BoothBase):
    pass


class BoothUpdate(BoothBase):
    id: int


class Metadata(SQLModel):
    page: int
    total: int
    per_page: int
    total_pages: int
    search: str


class BoothResponse(BaseModel):
    metadata: Metadata
    data: list[BoothPublic]
    description: str | None = None


class BoothCashSession(SQLModel, table=True):

    __tablename__ = "BoothCashSession"

    id: int | None = Field(default=None, primary_key=True)
    booth_id: int = Field(foreign_key="Booth.id")
    user_id: int = Field(foreign_key="User.id")
    opened_at: datetime.datetime
    initial_amount: decimal.Decimal | None = Field(sa_type=sa.Numeric())
    closing_amount: decimal.Decimal | None = Field(sa_type=sa.Numeric())
    closing_reason: str | None
    closing_observations: str | None = Field(sa_type=sa.Text())
    closed_at: datetime.datetime | None
    created_at: datetime.datetime | None = Field(default_factory=lambda: datetime.now())
    created_by: int | None = Field(default=None, foreign_key="User.id")
    updated_at: datetime.datetime | None = Field(
        default=None, sa_column=Column(DateTime(), onupdate=func.now())
    )
    updated_by: int | None = Field(default=None, foreign_key="User.id")

    __table_args__ = (
        Index("idx_booth_cash_session_booth_id", "booth_id"),
        Index("idx_booth_cash_session_user_id", "user_id"),
        Index("idx_booth_cash_session_created_by", "created_by"),
        Index("idx_booth_cash_session_updated_by", "updated_by"),
    )
