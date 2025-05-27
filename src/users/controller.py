from typing import Annotated
from fastapi import Body, Depends, HTTPException, Query, APIRouter, status
from sqlalchemy.exc import IntegrityError
from sqlmodel import select
from ..database.core import SessionDep
from . import models, service
from .models import User, UserCreate, UserPublic, UserUpdate
from ..auth.service import CurrentUser

router = APIRouter(prefix="/users", tags=["Users"])

@router.get("/me", response_model=UserPublic)
def read_users_me(current_user: CurrentUser):
    return current_user

@router.post(
    "/",
    response_model=UserPublic,
    status_code=status.HTTP_201_CREATED,
    responses={status.HTTP_201_CREATED: {"description": "User created successfully", "model": UserPublic}}
)
def create_user(
    current_user: CurrentUser,
    user: UserCreate,
    session: SessionDep
):
    db_user = User(**user.model_dump())
    session.add(db_user)
    try:
        session.commit()
        session.refresh(db_user)
        return db_user
    except IntegrityError as e:
        session.rollback()
        msg = str(e.orig)
        if "UNIQUE constraint failed" in msg and "User.username" in msg:
            detail = "Isername already exist."
        else:
            detail = "Error in database"
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=detail)

@router.get("/", response_model=list[UserPublic])
def read_users(
    current_user: CurrentUser,
    session: SessionDep,
    offset: int = 0,
    limit: Annotated[int, Query(le=100)] = 100,
):
    users = session.exec(select(User).offset(offset).limit(limit)).all()
    return users

@router.get("/{user_id}", response_model=UserPublic)
def read_user(current_user: CurrentUser, user_id: int, session: SessionDep):
    user = session.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@router.patch("/{user_id}", response_model=UserPublic)
def update_user(current_user: CurrentUser, user_id: int, user: UserUpdate, session: SessionDep):
    db_user = session.get(User, user_id)
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    user_data = user.model_dump(exclude_unset=True)
    db_user.sqlmodel_update(user_data)
    session.add(db_user)
    session.commit()
    session.refresh(db_user)
    return db_user

@router.delete("/{user_id}")
def delete_user(current_user: CurrentUser, user_id: int, session: SessionDep):
    user = session.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    session.delete(user)
    session.commit()
    return {"User deleted successfully": True}