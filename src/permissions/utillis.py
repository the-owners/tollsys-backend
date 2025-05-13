# sistema de permisos para proteger los endpoints

from fastapi import Depends, HTTPException, status
from sqlmodel import Session
from src.database import get_session
from src.role_permissions.service import RolePermissionService
from src.permissions.service import PermissionService
from src.auth.service import get_current_user
from src.auth.models import User

def has_permission(permission_name: str):
    def permission_checker(
        current_user: User = Depends(get_current_user),
        session: Session = Depends(get_session)
    ):
        role_permission_service = RolePermissionService(session)
        role_permissions = role_permission_service.get_role_permissions(current_user.role_id)
        
        permission_service = PermissionService(session)
        permission = permission_service.get_permission_by_name(permission_name)
        
        if not permission:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Permission does not exist"
            )
            
        has_perm = any(
            rp.permission_id == permission.id 
            for rp in role_permissions
        )
        
        if not has_perm:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Insufficient permissions"
            )
        return current_user
    
    return permission_checker