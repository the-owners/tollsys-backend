from sqlmodel import Session, select, and_
from typing import List
from src.roles.service import RoleService
from src.permissions.service import PermissionService
from src.exceptions import AuthenticationError
from fastapi import HTTPException, status
from .models import RolePermission, RolePermissionCreate

class RolePermissionService:
    def __init__(self, session: Session):
        self.session = session
        self.role_service = RoleService(session)
        self.permission_service = PermissionService(session)

    def assign_permission_to_role(self, role_permission_data: RolePermissionCreate, created_by: int) -> RolePermission:
        # Verificar que existan el rol y el permiso
        self.role_service.get_role(role_permission_data.role_id)
        self.permission_service.get_permission(role_permission_data.permission_id)
        
        # Verificar que no exista ya esta relación
        existing = self.session.exec(
            select(RolePermission).where(
                and_(
                    RolePermission.role_id == role_permission_data.role_id,
                    RolePermission.permission_id == role_permission_data.permission_id
                )
            )
        ).first()
        
        if existing:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Permission already assigned to this role"
            )
        
        role_permission = RolePermission(
            **role_permission_data.model_dump(),
            created_by=created_by
        )
        
        self.session.add(role_permission)
        self.session.commit()
        self.session.refresh(role_permission)
        return role_permission

    def get_role_permissions(self, role_id: int) -> List[RolePermission]:
        role_permissions = self.session.exec(
            select(RolePermission).where(RolePermission.role_id == role_id)
        ).all()
        return role_permissions

    def get_permission_roles(self, permission_id: int) -> List[RolePermission]:
        role_permissions = self.session.exec(
            select(RolePermission).where(RolePermission.permission_id == permission_id)
        ).all()
        return role_permissions

    def remove_permission_from_role(self, role_id: int, permission_id: int):
        role_permission = self.session.exec(
            select(RolePermission).where(
                and_(
                    RolePermission.role_id == role_id,
                    RolePermission.permission_id == permission_id
                )
            )
        ).first()
        
        if not role_permission:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Permission not assigned to this role"
            )
        
        self.session.delete(role_permission)
        self.session.commit()
        return {"message": "Permission removed from role successfully"}