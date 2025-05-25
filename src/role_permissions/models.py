from typing import Optional, List
from sqlmodel import SQLModel, Field, Index
import datetime

class RolePermission(SQLModel, table=True):

    __tablename__ = 'RolePermission'

    id: Optional[int] = Field(default=None, primary_key=True)
    role_id: Optional[int] = Field(foreign_key='Role.id')
    permission_id: Optional[int] = Field(foreign_key='Permission.id')
    created_at: Optional[datetime.datetime] = Field(default=None)
    created_by: Optional[int] = Field(default=None, foreign_key='User.id')
    updated_at: Optional[datetime.datetime] = Field(default=None)
    updated_by: Optional[int] = Field(default=None, foreign_key='User.id')

    __table_args__ = (
                
    Index('idx_role_permission_role_id', 'role_id'),
    Index('idx_role_permission_permission_id', 'permission_id'),
    Index('idx_role_permission_created_by', 'created_by'),
    Index('idx_role_permission_updated_by', 'updated_by'),
            )
