from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session
from .models import PermissionCreate, PermissionRead, PermissionUpdate
from .service import PermissionService
from src.database.core import get_session
from typing import List

router = APIRouter()

@router.post("/", response_model=PermissionRead)
def create_permission(
    permission_data: PermissionCreate,
    session: Session = Depends(get_session)
):
    return PermissionService(session).create_permission(permission_data)

@router.get("/", response_model=List[PermissionRead])
def read_permissions(session: Session = Depends(get_session)):
    return PermissionService(session).get_permissions()

@router.get("/{permission_id}", response_model=PermissionRead)
def read_permission(permission_id: int, session: Session = Depends(get_session)):
    return PermissionService(session).get_permission(permission_id)

@router.put("/{permission_id}", response_model=PermissionRead)
def update_permission(
    permission_id: int,
    permission_data: PermissionUpdate,
    session: Session = Depends(get_session)
):
    return PermissionService(session).update_permission(permission_id, permission_data)

@router.delete("/{permission_id}")
def delete_permission(permission_id: int, session: Session = Depends(get_session)):
    return PermissionService(session).delete_permission(permission_id)