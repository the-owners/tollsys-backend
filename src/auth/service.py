from datetime import timedelta, datetime, timezone
from typing import Annotated
from uuid import UUID, uuid4
from fastapi import Depends
import passlib
import passlib.context
import jwt
from jwt import PyJWTError
from sqlalchemy.orm import Session
from ..users.models import User, UserCreate, UserPublic
from . import models
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from ..exceptions import AuthenticationError
import logging
import os
from dotenv import load_dotenv

from datetime import datetime, timedelta, timezone
from typing import Annotated

import jwt
from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jwt.exceptions import InvalidTokenError
from passlib.context import CryptContext
from pydantic import BaseModel
from ..database.core import SessionDep

# this is an ugly hack that's required for passlib
# here until we get rid of that old dependency
import bcrypt
if not hasattr(bcrypt, '__about__'):
    bcrypt.__about__ = type('about', (object,), {'__version__': bcrypt.__version__}) # type: ignore[attr-defined]


load_dotenv()

# defaults to nosecretkey although idk how good is that, but everything for production!
SECRET_KEY = os.getenv("SECRET_KEY", "NoSecretKeySet")
ALGORITHM = 'HS256'
ACCESS_TOKEN_EXPIRE_MINUTES = 60

oauth2_bearer = OAuth2PasswordBearer(tokenUrl='auth/login')
bcrypt_context = passlib.context.CryptContext(schemes=['bcrypt'], deprecated='auto')

def verify_password(plain_password: str, hashed_password: str) -> bool:
    try:
        return bcrypt_context.verify(plain_password, hashed_password)
    except passlib.exc.UnknownHashError: # type: ignore[attr-defined]
        logging.error(f"Invalid password hash format for user")
        return False


def get_password_hash(password: str) -> str:
    return bcrypt_context.hash(password)


def authenticate_user(username: str, password: str, db: Session) -> User | bool:
    user = db.query(User).filter(User.username == username).first() # type: ignore[arg-type]
    if not user or not verify_password(password, user.password): # type: ignore[arg-type]
        logging.warning(f"Failed authentication attempt for username: {username}")
        return False
    return user


def create_access_token(username: str, user_id: UUID, expires_delta: timedelta) -> str:
    encode = {
        'sub': username,
        'id': str(user_id),
        'exp': datetime.now(timezone.utc) + expires_delta
    }
    return jwt.encode(encode, SECRET_KEY, algorithm=ALGORITHM)


def verify_token(token: str) -> models.TokenData:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: str = payload.get('id')
        return models.TokenData(user_id=user_id)
    except PyJWTError as e:
        logging.warning(f"Token verification failed: {str(e)}")
        raise AuthenticationError()


def register_user(db: Session, register_user_request: UserCreate) -> None:
    try:
        create_user_model = User(
            username=register_user_request.username,
            name=register_user_request.name,
            role_id=register_user_request.role_id, # temporary db crashes later otherwise
            toll_id=register_user_request.toll_id, # temporary db crashes later otherwise
            password=get_password_hash(register_user_request.password)
        )
        db.add(create_user_model)
        db.commit()
    except Exception as e:
        logging.error(f"Failed to register user: {register_user_request.username}. Error: {str(e)}")
        raise
    
    
def get_current_user_token(token: Annotated[str, Depends(oauth2_bearer)]) -> models.TokenData:
    return verify_token(token)

CurrentUser = Annotated[models.TokenData, Depends(get_current_user_token)]


def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
                                 db: Session) -> models.Token:
    user = authenticate_user(form_data.username, form_data.password, db)
    if not user:
        raise AuthenticationError()
    token = create_access_token(user.username, user.id, timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)) # type: ignore[union-attr, arg-type]
    return models.Token(access_token=token, token_type='bearer')

def get_current_active_user(token: Annotated[str, Depends(oauth2_bearer)], session: SessionDep):
    credentials_exception = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Could not validate credentials",
    headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id = payload.get("id")
        if user_id is None:
            raise credentials_exception
        token_data = models.TokenData(user_id=int(user_id))
    except InvalidTokenError:
        raise credentials_exception
    user = session.get(User, token_data.user_id) # this should be handled by users i think
    if user is None:
        raise credentials_exception
    return user