import datetime
import decimal
from typing import Optional
from sqlmodel import Field, SQLModel
from enum import Enum
import sqlalchemy as sa
from sqlalchemy.sql import func
from sqlalchemy import Index


class BoothStatus(str, Enum):

    AVAILABLE = 'AVAILABLE'
    CLOSED = 'CLOSED'
    MAINTENANCE = 'MAINTENANCE'
    OCCUPIED = 'OCCUPIED'
class Booth(SQLModel, table=True):

    __tablename__ = 'Booth'

    id: Optional[int] = Field(default=None, primary_key=True)
    name: Optional[str]
    active: Optional[bool]
    status: Optional[BoothStatus] = Field(sa_type=sa.Enum(BoothStatus))
    toll_id: Optional[int] = Field(foreign_key='Toll.id')
    created_at: Optional[datetime.datetime]
    created_by: Optional[int] = Field(foreign_key='User.id')
    updated_at: Optional[datetime.datetime]
    updated_by: Optional[int] = Field(foreign_key='User.id')

    __table_args__ = (
                
    Index('idx_booth_toll_id', 'toll_id'),
    Index('idx_booth_created_by', 'created_by'),
    Index('idx_booth_updated_by', 'updated_by'),
            )



class BoothCashSession(SQLModel, table=True):

    __tablename__ = 'BoothCashSession'

    id: Optional[int] = Field(default=None, primary_key=True)
    booth_id: int = Field(foreign_key='Booth.id')
    user_id: int = Field(foreign_key='User.id')
    opened_at: datetime.datetime
    initial_amount: Optional[decimal.Decimal] = Field(sa_type=sa.Numeric())
    closing_amount: Optional[decimal.Decimal] = Field(sa_type=sa.Numeric())
    closing_reason: Optional[str]
    closing_observations: Optional[str] = Field(sa_type=sa.Text())
    closed_at: Optional[datetime.datetime]
    created_at: Optional[datetime.datetime] = Field(sa_column_kwargs={'server_default': func.now()})
    created_by: Optional[int] = Field(foreign_key='User.id')
    updated_at: Optional[datetime.datetime]
    updated_by: Optional[int] = Field(foreign_key='User.id')

    __table_args__ = (
                
    Index('idx_booth_cash_session_booth_id', 'booth_id'),
    Index('idx_booth_cash_session_user_id', 'user_id'),
    Index('idx_booth_cash_session_created_by', 'created_by'),
    Index('idx_booth_cash_session_updated_by', 'updated_by'),
            )