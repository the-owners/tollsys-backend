import datetime
from typing import Optional
from sqlmodel import SQLModel, Field, Index


class RolePermissionBase(SQLModel):
    role_id: Optional[int] = Field(default=None, foreign_key='Role.id')
    permission_id: Optional[int] = Field(default=None, foreign_key='Permission.id')


class RolePermission(RolePermissionBase, table=True):
    __tablename__ = "RolePermission"

    id: Optional[int] = Field(default=None, primary_key=True)
    created_at: Optional[datetime.datetime] = Field(default_factory=datetime.datetime.utcnow)
    created_by: Optional[int] = Field(default=None, foreign_key='User.id')
    updated_at: Optional[datetime.datetime] = Field(default_factory=datetime.datetime.utcnow)
    updated_by: Optional[int] = Field(default=None, foreign_key='User.id')

    __table_args__ = (
        Index('idx_role_permission_role_id', 'role_id'),
        Index('idx_role_permission_permission_id', 'permission_id'),
        Index('idx_role_permission_created_by', 'created_by'),
        Index('idx_role_permission_updated_by', 'updated_by'),
    )


class RolePermissionCreate(RolePermissionBase):
    role_id: int
    permission_id: int


class RolePermissionUpdate(RolePermissionBase):
    pass


class RolePermissionPublic(RolePermissionBase):
    id: int
