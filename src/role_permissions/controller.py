from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session
from .models import RolePermissionCreate, RolePermissionRead
from .service import RolePermissionService
from src.database.core import SessionDep, get_session
from typing import List
from src.auth.service import get_current_user

router = APIRouter()

@router.post("/", response_model=RolePermissionRead)
def assign_permission_to_role(
    role_permission_data: RolePermissionCreate,
    session: Session = Depends(SessionDep),  # Usa SessionDep aquí
    current_user_id: int = Depends(get_current_user)
):
    return RolePermissionService(session).assign_permission_to_role(role_permission_data, current_user_id)


@router.get("/role/{role_id}", response_model=List[RolePermissionRead])
def get_role_permissions(role_id: int, session: Session = Depends(get_session)):
    return RolePermissionService(session).get_role_permissions(role_id)

@router.get("/permission/{permission_id}", response_model=List[RolePermissionRead])
def get_permission_roles(permission_id: int, session: Session = Depends(get_session)):
    return RolePermissionService(session).get_permission_roles(permission_id)

@router.delete("/role/{role_id}/permission/{permission_id}")
def remove_permission_from_role(
    role_id: int,
    permission_id: int,
    session: Session = Depends(get_session)
):
    return RolePermissionService(session).remove_permission_from_role(role_id, permission_id)