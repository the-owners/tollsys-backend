import datetime
import decimal
from typing import Optional
from sqlmodel import Field, SQLModel
from enum import Enum
import sqlalchemy as sa
from sqlalchemy.sql import func
from sqlalchemy import Index
class VehicleType(SQLModel, table=True):

    __tablename__ = 'VehicleType'

    id: Optional[int] = Field(default=None, primary_key=True)
    name: Optional[str]
    icon: Optional[str]
    rate: Optional[decimal.Decimal] = Field(sa_type=sa.Numeric())
    active: Optional[bool]
    created_at: Optional[datetime.datetime]
    created_by: Optional[int] = Field(foreign_key='User.id')
    updated_at: Optional[datetime.datetime]
    updated_by: Optional[int] = Field(foreign_key='User.id')

    __table_args__ = (
                
    Index('idx_vehicle_type_name', 'name'),
    Index('idx_vehicle_type_active', 'active'),
    Index('idx_vehicle_type_created_by', 'created_by'),
    Index('idx_vehicle_type_updated_by', 'updated_by'),
            )
