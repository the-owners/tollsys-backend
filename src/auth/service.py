from typing import Annotated, Optional
from datetime import timedelta, datetime, timezone

import passlib
import passlib.context

import jwt
from jwt import PyJWTError
from jwt.exceptions import InvalidTokenError

from fastapi import Depends, FastAPI, HTTPException, status
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer

from . import models
from ..exceptions import AuthenticationError
from ..users.models import User, UserCreate, UserPublic
from ..roles.models import RolePublic, Role
from ..tolls.models import TollPublic, Toll
from ..database.core import SessionDep

import os
from dotenv import load_dotenv

import logging

# this is an ugly hack that's required for passlib
# here until we get rid of that old dependency
import bcrypt

if not hasattr(bcrypt, "__about__"):
    bcrypt.__about__ = type("about", (object,), {"__version__": bcrypt.__version__})  # type: ignore[attr-defined]

load_dotenv()

# defaults to nosecretkey although idk how good is that, but everything for production!
SECRET_KEY = os.getenv("SECRET_KEY", "NoSecretKeySet")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60

oauth2_bearer = OAuth2PasswordBearer(tokenUrl="auth/login")
bcrypt_context = passlib.context.CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    try:
        return bcrypt_context.verify(plain_password, hashed_password)
    except passlib.exc.UnknownHashError:  # type: ignore[attr-defined]
        logging.error(f"Invalid password hash format for user")
        return False


def get_password_hash(password: str) -> str:
    return bcrypt_context.hash(password)


def authenticate_user(username: str, password: str, session: SessionDep) -> User | bool:
    user = session.query(User).filter(User.username == username).first()  # type: ignore[arg-type]
    if not user or not verify_password(password, user.password):  # type: ignore[arg-type]
        logging.warning(f"Failed authentication attempt for username: {username}")
        return False
    return user


def create_access_token(
    username: str, 
    user_id: int, 
    role_id: int,
    expires_delta: timedelta,
    additional_claims: Optional[dict] = None
) -> str:
    """Crea un token JWT con claims adicionales para permisos"""
    encode = {
        "sub": str(user_id),
        "username": username,
        "user_id": user_id,
        "role_id": role_id,
        "exp": datetime.now(timezone.utc) + expires_delta,
    }
    
    if additional_claims:
        encode.update(additional_claims)
    
    return jwt.encode(encode, SECRET_KEY, algorithm=ALGORITHM)


def verify_token(token: str) -> models.TokenData:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: str = payload.get("user_id")
        return models.TokenData(user_id=user_id)
    except PyJWTError as e:
        logging.warning(f"Token verification failed: {str(e)}")
        raise AuthenticationError()


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


def login(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()], session: SessionDep
) -> models.LoginResponse:
    user = authenticate_user(form_data.username, form_data.password, session)
    if not user:
        raise AuthenticationError()

    token = create_access_token(
        username=user.username, # type: ignore[union-attr]
        user_id=user.id, # type: ignore[union-attr, arg-type]
        role_id=user.role_id, # type: ignore[union-attr, arg-type]
        expires_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES),
    )

    return models.LoginResponse(
        access_token=token, # we could be using models.Token here probably
        user=UserPublic(
            id=user.id, # type: ignore[union-attr]
            name=user.name, # type: ignore[union-attr]
            username=user.username, # type: ignore[union-attr]
            role_id=user.role_id, # type: ignore[union-attr]
            toll_id=user.toll_id, # type: ignore[union-attr]
            role=session.get(Role, user.role_id), # type: ignore[union-attr]
            toll=session.get(Toll, user.toll_id) # type: ignore[union-attr]
        ),
    )


def get_current_active_user(
    token: Annotated[str, Depends(oauth2_bearer)], session: SessionDep
):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id = payload.get("user_id")
        if user_id is None:
            raise AuthenticationError
        token_data = models.TokenData(user_id=user_id)
    except InvalidTokenError:
        raise AuthenticationError
    user = session.get(
        User, token_data.user_id
    )  # this should be handled by users i think
    if user is None:
        raise AuthenticationError
    return user


CurrentUser = Annotated[User, Depends(get_current_active_user)]


def logout(
    current_user: CurrentUser, reason: str, observations: str, session: SessionDep
):
    # here we would add reason to BoothCashSession.closing_reason
    # here we would add observations to BoothCashSession.closing_observations
    # and call it a day I think. it is unclear in the api spec atm
    # also, i don't feel like implementing a session-tracking mechanism
    # for expiring tokens so, we'll probably manage it using cookies down the road
    pass


async def get_current_user(
    token: Annotated[str, Depends(oauth2_bearer)], 
    session: SessionDep
) -> User:
    """Obtiene el usuario actual basado en el token JWT"""
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id = payload.get("user_id")
        if user_id is None:
            raise AuthenticationError()
        
        user = session.get(User, user_id)
        if user is None:
            raise AuthenticationError()
            
        return user
    except (InvalidTokenError, PyJWTError) as e:
        logging.warning(f"Token verification failed: {str(e)}")
        raise AuthenticationError()
    

    async def get_user_permissions(user: User, session: SessionDep) -> list[str]:
        """Obtiene todos los permisos del usuario basado en su rol"""
        if not user.role_id:
            return []
        
        permissions = session.exec(
            select(Permission.name).join(RolePermission).where(
                RolePermission.role_id == user.role_id
            )
        ).all()
        
        return permissions

def has_permission(permission_name: str):
    """Factory para dependencias que verifican permisos"""
    async def permission_checker(
        user: CurrentUser,
        session: SessionDep
    ):
        permissions = await get_user_permissions(user, session)
        if permission_name not in permissions:
            raise PermissionDeniedError(
                detail=f"Requires permission: {permission_name}"
            )
        return user
    
    return permission_checker

# Middleware para verificación de tokens en todas las rutas
class AuthenticationMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        # Excluir rutas públicas (login, docs, etc.)
        public_routes = ["/auth/login", "/docs", "/openapi.json"]
        if request.url.path in public_routes:
            return await call_next(request)
            
        # Verificar token en el header Authorization
        auth_header = request.headers.get("Authorization")
        if not auth_header or not auth_header.startswith("Bearer "):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Missing or invalid authorization header"
            )
            
        token = auth_header.split(" ")[1]
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            request.state.user_id = payload.get("user_id")
            request.state.role_id = payload.get("role_id")
        except (InvalidTokenError, PyJWTError):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token"
            )
            
        response = await call_next(request)
        return response

class AuditLoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        logging.info(f"Request: {request.method} {request.url.path}")
        
        response = await call_next(request)
        
        if hasattr(request.state, 'user_id'):
            logging.info(
                f"User {request.state.user_id} accessed {request.url.path} "
                f"with status {response.status_code}"
            )
            
        return response

def setup_middlewares(app: FastAPI):
    app.add_middleware(AuthenticationMiddleware)
    app.add_middleware(AuditLoggingMiddleware)