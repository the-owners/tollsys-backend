from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session
from .models import RoleCreate, RoleRead, RoleUpdate
from .service import RoleService
from src.database.core import get_session
from typing import List
from src.auth.service import get_current_user 

router = APIRouter()

@router.post("/", response_model=RoleRead)
def create_role(
    role_data: RoleCreate,
    session: Session = Depends(get_session),
    current_user_id: int = Depends(get_current_user)
):
    return RoleService(session).create_role(role_data, current_user_id)

@router.get("/", response_model=List[RoleRead])
def read_roles(session: Session = Depends(get_session)):
    return RoleService(session).get_roles()

@router.get("/{role_id}", response_model=RoleRead)
def read_role(role_id: int, session: Session = Depends(get_session)):
    return RoleService(session).get_role(role_id)

@router.put("/{role_id}", response_model=RoleRead)
def update_role(
    role_id: int,
    role_data: RoleUpdate,
    session: Session = Depends(get_session),
    current_user_id: int = Depends(get_current_user)
):
    return RoleService(session).update_role(role_id, role_data, current_user_id)

@router.delete("/{role_id}")
def delete_role(role_id: int, session: Session = Depends(get_session)):
    return RoleService(session).delete_role(role_id)