from typing import Annotated
from fastapi import Body, Depends, HTTPException, Query, APIRouter, status
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from sqlmodel import Field, Session, SQLModel, create_engine, select
from ..database.core import SessionDep
from . import  models
from . import service
from .models import *
from ..auth.service import CurrentUser
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from src.exceptions import UserNotFoundError

router = APIRouter(
    prefix="/users",
    tags=["Users"]
)

@router.post("/me/change_password", status_code=status.HTTP_200_OK, responses={status.HTTP_200_OK: {"description": "Password changed sucessfully."}})
def change_password(session: SessionDep, current_user: CurrentUser, change_password_request: ChangePasswordRequest):
    service.change_password(session, current_user.id, change_password_request)
    return {"msg": "Password changed sucessfully"}


@router.get("/me", response_model=UserPublic)
def read_users_me(current_user: CurrentUser):
    return current_user

@router.post("/", response_model=UserPublic, status_code=status.HTTP_201_CREATED, responses={status.HTTP_201_CREATED: {"description": "User created sucessfully.", "model": UserPublic}})
def create_user(user: UserCreate, session: SessionDep):
    db_user = User.model_validate(user)
    session.add(db_user)
    session.commit()
    session.refresh(db_user)
    return db_user

@router.get("/", response_model=list[UserPublic])
def read_users(
    session: SessionDep,
    offset: int = 0,
    limit: Annotated[int, Query(le=100)] = 100,
):
    users = session.exec(select(User).offset(offset).limit(limit)).all()
    return users


@router.get("/{user_id}", response_model=UserPublic)
def read_user(user_id: int, session: SessionDep):
    user = session.get(User, user_id)
    if not user:
        raise UserNotFoundError(user_id)
    return user


@router.patch("/{user_id}", response_model=UserPublic)
def update_user(user_id: int, user: UserUpdate, session: SessionDep):
    db_user = session.get(User, user_id)
    if not db_user:
        raise UserNotFoundError(user_id)
    user_data = user.model_dump(exclude_unset=True)
    db_user.sqlmodel_update(user_data)
    session.add(db_user)
    session.commit()
    session.refresh(db_user)
    return db_user


@router.delete("/{user_id}")
def delete_user(user_id: int, session: SessionDep):
    user = session.get(User, user_id)
    if not user:
        raise UserNotFoundError(user_id)
    session.delete(user)
    session.commit()
    return {"User deleted sucessfully": True}
