import logging

from src.auth.service import get_password_hash, verify_password
from src.database.core import SessionDep
from src.exceptions import (
    InvalidPasswordError,
    NewPasswordIsCurrentPasswordError,
    PasswordMismatchError,
)
from src.users.models import ChangePasswordRequest, User, UserCreate


def change_password(
    session: SessionDep,
    current_user_id: int,
    change_password_request: ChangePasswordRequest,
):
    db_user = session.get(User, current_user_id)
    if not (
        change_password_request.new_password
        == change_password_request.new_password_confirm
    ):
        raise PasswordMismatchError
    if not verify_password(change_password_request.current_password, db_user.password):
        raise InvalidPasswordError
    if (
        change_password_request.current_password
        == change_password_request.new_password_confirm
    ):
        raise NewPasswordIsCurrentPasswordError
    db_user.password = get_password_hash(change_password_request.new_password)
    session.add(db_user)
    session.commit()
    session.refresh(db_user)


def register_user(session: SessionDep, register_user_request: UserCreate) -> None:
    try:
        create_user_model = User(
            username=register_user_request.username,
            name=register_user_request.name,
            role_id=register_user_request.role_id,  # temporary db crashes later otherwise
            toll_id=register_user_request.toll_id,  # temporary db crashes later otherwise
            password=get_password_hash(register_user_request.password),
        )
        session.add(create_user_model)
        session.commit()
    except Exception as e:
        logging.error(
            f"Failed to register user: {register_user_request.username}. Error: {str(e)}"
        )
        raise
