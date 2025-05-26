# src/role_permissions/controller.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session
from ..database.core import SessionDep
from ..auth.service import CurrentUser
from . import service
from .models import RolePermission

router = APIRouter(
    prefix="/role-permissions",
    tags=["RolePermissions"]
)

@router.post("/", response_model=RolePermission, status_code=status.HTTP_201_CREATED)
def assign_permission_to_role(
    role_id: int,
    permission_id: int,
    current_user: CurrentUser,
    session: SessionDep
):
    return service.create_role_permission(role_id, permission_id, current_user, session)

@router.get("/by-role/{role_id}", response_model=list[RolePermission])
def get_permissions_by_role(
    role_id: int,
    current_user: CurrentUser,
    session: SessionDep
):
    return service.get_permissions_by_role(role_id, session)

@router.delete("/", status_code=status.HTTP_204_NO_CONTENT)
def remove_permission_from_role(
    role_id: int,
    permission_id: int,
    current_user: CurrentUser,
    session: SessionDep
):
    service.delete_role_permission(role_id, permission_id, session)
