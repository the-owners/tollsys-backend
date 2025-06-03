from typing import Annotated

from fastapi import APIRouter, Query, status
from sqlmodel import select

from src import auth
from src.auth.service import CurrentUser
from src.database.core import SessionDep
from src.exceptions import UserNotFoundError
from src.users import service
from src.users.models import (
    ChangePasswordRequest,
    User,
    UserCreate,
    UserPublic,
    UserUpdate,
)

router = APIRouter(prefix="/users", tags=["Users"])


@router.post(
    "/me/change_password",
    status_code=status.HTTP_200_OK,
    responses={status.HTTP_200_OK: {"description": "Password changed sucessfully."}},
)
def change_password(
    session: SessionDep,
    current_user: CurrentUser,
    change_password_request: ChangePasswordRequest,
):
    service.change_password(session, current_user.id, change_password_request)
    return {"msg": "Password changed sucessfully"}


@router.get("/me", response_model=dict)
def read_users_me(current_user: CurrentUser, session: SessionDep):
    return auth.service.get_my_info(current_user, session)


@router.post(
    "/",
    response_model=UserPublic,
    status_code=status.HTTP_201_CREATED,
    responses={
        status.HTTP_201_CREATED: {
            "description": "User created sucessfully.",
            "model": UserPublic,
        }
    },
)
def create_user(user: UserCreate, session: SessionDep):
    created_user = auth.service.register_user(session, user)
    return created_user


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
        raise UserNotFoundError(user_id)
    return user


@router.patch("/{user_id}", response_model=UserPublic)
def update_user(
    current_user: CurrentUser, user_id: int, user: UserUpdate, session: SessionDep
):
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
def delete_user(current_user: CurrentUser, user_id: int, session: SessionDep):
    user = session.get(User, user_id)
    if not user:
        raise UserNotFoundError(user_id)
    session.delete(user)
    session.commit()
    return {"User deleted sucessfully": True}
