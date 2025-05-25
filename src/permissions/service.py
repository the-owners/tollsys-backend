from sqlmodel import Session, select
from .models import Permission, PermissionCreate, PermissionUpdate
from typing import List
from fastapi import HTTPException
from datetime import datetime

class PermissionService:
    def __init__(self, session: Session):
        self.session = session

    def create_permission(self, permission_data: PermissionCreate) -> Permission:
        permission = Permission(**permission_data.model_dump())
        self.session.add(permission)
        self.session.commit()
        self.session.refresh(permission)
        return permission

    def get_permission(self, permission_id: int) -> Permission:
        permission = self.session.get(Permission, permission_id)
        if not permission:
            raise HTTPException(status_code=404, detail="Permission not found")
        return permission

    def get_permissions(self) -> List[Permission]:
        permissions = self.session.exec(select(Permission)).all()
        return permissions

    def update_permission(self, permission_id: int, permission_data: PermissionUpdate) -> Permission:
        permission = self.get_permission(permission_id)
        permission_data_dict = permission_data.model_dump(exclude_unset=True)
        
        for key, value in permission_data_dict.items():
            setattr(permission, key, value)
            
        permission.updated_at = datetime.utcnow()
        
        self.session.add(permission)
        self.session.commit()
        self.session.refresh(permission)
        return permission

    def delete_permission(self, permission_id: int):
        permission = self.get_permission(permission_id)
        self.session.delete(permission)
        self.session.commit()
        return {"message": "Permission deleted successfully"}
    
    def get_permission_by_name(self, name: str) -> Permission:
        permission = self.session.exec(
            select(Permission).where(Permission.name == name)
        ).first()
        return permission