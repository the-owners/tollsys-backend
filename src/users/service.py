from src.database.core import SessionDep
from src.auth.service import CurrentUser
from src.users.models import ChangePasswordRequest, User
from src.auth.service import get_password_hash, verify_password
from src.exceptions import InvalidPasswordError, PasswordMismatchError, NewPasswordIsCurrentPasswordError

def change_password(session: SessionDep,
                    current_user_id: int,
                    change_password_request: ChangePasswordRequest):
    db_user = session.get(User, current_user_id)
    if not (change_password_request.new_password == change_password_request.new_password_confirm):
        raise PasswordMismatchError
    if not verify_password(change_password_request.current_password, db_user.password):
        raise InvalidPasswordError
    if (change_password_request.current_password == change_password_request.new_password_confirm):
        raise NewPasswordIsCurrentPasswordError
    db_user.password = get_password_hash(change_password_request.new_password)
    session.add(db_user)
    session.commit()
    session.refresh(db_user)
