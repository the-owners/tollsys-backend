from fastapi import APIRouter, Depends, HTTPException, status
from ..database.core import SessionDep
from . import service
from .models import PermissionCreate, PermissionUpdate, PermissionPublic
from ..auth.service import CurrentUser

router = APIRouter(prefix="/permissions", tags=["Permissions"])

@router.post("/", response_model=PermissionPublic, status_code=status.HTTP_201_CREATED)
def create_permission(current_user: CurrentUser, permission: PermissionCreate, session: SessionDep):
    return service.create_permission(session, permission)

@router.get("/", response_model=list[PermissionPublic])
def list_permissions(current_user: CurrentUser, session: SessionDep):
    return service.get_permissions(session)

@router.get("/{permission_id}", response_model=PermissionPublic)
def get_permission(current_user: CurrentUser, permission_id: int, session: SessionDep):
    db_permission = service.get_permission(session, permission_id)
    if not db_permission:
        raise HTTPException(status_code=404, detail="Permission not found")
    return db_permission

@router.patch("/{permission_id}", response_model=PermissionPublic)
def update_permission(current_user: CurrentUser, permission_id: int, permission: PermissionUpdate, session: SessionDep):
    db_permission = service.update_permission(session, permission_id, permission)
    if not db_permission:
        raise HTTPException(status_code=404, detail="Permission not found")
    return db_permission

@router.delete("/{permission_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_permission(current_user: CurrentUser, permission_id: int, session: SessionDep):
    success = service.delete_permission(session, permission_id)
    if not success:
        raise HTTPException(status_code=404, detail="Permission not found")
    return None
