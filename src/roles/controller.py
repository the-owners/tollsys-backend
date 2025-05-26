from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlmodel import Session, select
from ..database.core import SessionDep
from .models import Role, RolePublic, RoleCreate
from ..auth.service import CurrentUser
from datetime import datetime

router = APIRouter(
    prefix="/roles",
    tags=["Roles"]
)

@router.post("/", response_model=RolePublic, status_code=status.HTTP_201_CREATED)
def create_role(role: RoleCreate, session: SessionDep, current_user: CurrentUser):
    new_role = Role(
        name=role.name,
        created_at=datetime.utcnow(),
        created_by=current_user.id,
        updated_at=datetime.utcnow(),
        updated_by=current_user.id
    )
    session.add(new_role)
    session.commit()
    session.refresh(new_role)
    return new_role

@router.get("/", response_model=list[RolePublic])
def get_roles(
    session: SessionDep,
    current_user: CurrentUser,
    offset: int = 0,
    limit: Annotated[int, Query(le=100)] = 100
):
    roles = session.exec(select(Role).offset(offset).limit(limit)).all()
    return roles

@router.get("/{role_id}", response_model=RolePublic)
def get_role(role_id: int, session: SessionDep, current_user: CurrentUser):
    role = session.get(Role, role_id)
    if not role:
        raise HTTPException(status_code=404, detail="Role not found")
    return role

@router.patch("/{role_id}", response_model=RolePublic)
def update_role(role_id: int, updated_data: RoleCreate, session: SessionDep, current_user: CurrentUser):
    db_role = session.get(Role, role_id)
    if not db_role:
        raise HTTPException(status_code=404, detail="Role not found")
    db_role.name = updated_data.name
    db_role.updated_at = datetime.utcnow()
    db_role.updated_by = current_user.id
    session.add(db_role)
    session.commit()
    session.refresh(db_role)
    return db_role

@router.delete("/{role_id}")
def delete_role(role_id: int, session: SessionDep, current_user: CurrentUser):
    db_role = session.get(Role, role_id)
    if not db_role:
        raise HTTPException(status_code=404, detail="Role not found")
    session.delete(db_role)
    session.commit()
    return {"message": "Role deleted successfully"}
