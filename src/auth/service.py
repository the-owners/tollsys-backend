import logging
import os
from datetime import datetime, timedelta, timezone
from typing import Annotated

import jwt
import passlib.context

# Carga .env
from dotenv import load_dotenv
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jwt import ExpiredSignatureError, PyJWTError
from sqlmodel import select

from src.auth import models
from src.database.core import SessionDep
from src.exceptions import AuthenticationError
from src.permissions.models import Permission
from src.role_permissions.models import RolePermission
from src.roles.models import Role
from src.tolls.models import Toll
from src.users.models import User, UserCreate, UserPublic

load_dotenv()

# Configuración de JWT
SECRET_KEY = os.getenv("SECRET_KEY", "NoSecretKeySet")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_HOURS: float = float(os.getenv("ACCESS_TOKEN_EXPIRE_HOURS", 12))

# Contexto de cifrado de contraseñas
bcrypt_context = passlib.context.CryptContext(schemes=["bcrypt"], deprecated="auto")
# Dependencia OAuth2 para Swagger y rutas protegidas
oauth2_bearer = OAuth2PasswordBearer(tokenUrl="auth/login", scheme_name="JWT")

# --- Funciones de autenticación básica ---


def verify_password(plain_password: str, hashed_password: str) -> bool:
    try:
        return bcrypt_context.verify(plain_password, hashed_password)
    except passlib.exc.UnknownHashError:
        logging.error("Invalid password hash format")
        return False


def get_password_hash(password: str) -> str:
    return bcrypt_context.hash(password)


def authenticate_user(username: str, password: str, session: SessionDep) -> User | None:
    user = session.exec(select(User).where(User.username == username)).first()
    if not user or not verify_password(password, user.password):
        return None
    return user


# --- Generación de JWT ---


def create_access_token(
    username: str, user_id: int, role_id: int, expires_delta: timedelta | None = None
) -> str:
    expire = datetime.now(timezone.utc) + (
        expires_delta or timedelta(hours=ACCESS_TOKEN_EXPIRE_HOURS)
    )
    to_encode = {
        "username": username,
        "user_id": user_id,
        "role_id": role_id,
        "exp": expire,
    }
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


# --- Registro y login ---


def register_user(session: SessionDep, req: UserCreate) -> User:
    hashed = get_password_hash(req.password)
    user = User(
        username=req.username,
        name=req.name,
        role_id=req.role_id,
        toll_id=req.toll_id,
        password=hashed,
    )
    session.add(user)
    session.commit()
    return user


def login(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()], session: SessionDep
) -> models.LoginResponse:
    user = authenticate_user(form_data.username, form_data.password, session)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials"
        )

    token = create_access_token(
        username=user.username, user_id=user.id, role_id=user.role_id
    )
    return models.LoginResponse(
        access_token=token,
        token_type="bearer",
        user=UserPublic(
            id=user.id,
            name=user.name,
            username=user.username,
            role_id=user.role_id,
            toll_id=user.toll_id,
            role=session.get(Role, user.role_id),
            toll=session.get(Toll, user.toll_id),
        ),
    )


# --- Dependencia para extraer el usuario actual desde JWT ---


def get_current_active_user(
    token: Annotated[str, Depends(oauth2_bearer)], session: SessionDep
) -> User:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: int = payload.get("user_id")
        if user_id is None:
            raise AuthenticationError()
    except ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Token has expired"
        )
    except PyJWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token"
        )

    user = session.get(User, user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found"
        )
    return user


CurrentUser = Annotated[User, Depends(get_current_active_user)]


def logout(
    current_user: CurrentUser, reason: str, observations: str, session: SessionDep
):
    # Implementar lógica de logout si es necesario
    pass


# --- Inspección manual de un JWT cualquiera ---


def inspect_token_data_raw(token: str, session: SessionDep):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id = payload.get("user_id")
        role_id = payload.get("role_id")
        username = payload.get("username")
        if not user_id or not role_id:
            raise HTTPException(status_code=400, detail="Token payload missing fields")

        # Obtener permisos asociados al role_id
        stmt = (
            select(Permission.name)
            .join(RolePermission, Permission.id == RolePermission.permission_id)
            .where(RolePermission.role_id == role_id)
        )
        permissions = session.exec(stmt).all()

        return {
            "user_id": user_id,
            "username": username,
            "role_id": role_id,
            "permissions": permissions,
        }
    except ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Token has expired"
        )
    except PyJWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token"
        )


def get_my_info(current_user: CurrentUser, db: SessionDep):
    # Información del usuario autenticado
    role = db.get(Role, current_user.role_id)
    if not role:
        raise HTTPException(status_code=404, detail="Role not found")

    # Obtiene permisos del rol
    rps = db.query(RolePermission).filter(RolePermission.role_id == role.id).all()
    perm_ids = [rp.permission_id for rp in rps]
    perms = db.query(Permission).filter(Permission.id.in_(perm_ids)).all()
    perm_names = [p.name for p in perms]

    return {
        "user_id": current_user.id,
        "username": current_user.username,
        "role": role.name,
        "permissions": perm_names,
    }
