from fastapi import Depends, HTTPException, status
from .jwt import get_current_user

def require_permission(permission: PermissionEnum):
    async def checker(user: User = Depends(get_current_user)):
        if not user.role or permission not in [p.name for p in user.role.permissions]:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="No tienes permisos para esta acción"
            )
        return user
    return checker