from typing import Annotated
from fastapi import APIRouter, Depends, Request, Body, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from ..database.core import SessionDep
from . import service, models
from .service import oauth2_bearer
from ..users.models import UserCreate
from ..roles.models import Role
from ..permissions.models import Permission
from ..role_permissions.models import RolePermission

router = APIRouter(
    prefix="/auth",
    tags=["auth"]
)


@router.post("/login", response_model=models.LoginResponse)
async def login(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    db: SessionDep
):
    return service.login(form_data, db)

@router.post("/logout")
async def logout(
    current_user: service.CurrentUser,
    reason: str,
    observations: str,
    db: SessionDep
):
    service.logout(current_user, reason, observations, db)
    return {"message": "Successfully logged out"}

@router.get("/me", response_model=dict, dependencies=[Depends(oauth2_bearer)])
def get_my_info(
    current_user: service.CurrentUser,
    db: SessionDep
):
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
        "permissions": perm_names
    }

@router.post(
    "/inspect-token",
    summary="Inspect any JWT",
    response_model=dict
)
def inspect_token_endpoint(
    db: SessionDep,
    token: str = Body(..., embed=True, description="JWT token to be inspected")
):
    """
    Recibe un token JWT en el body y devuelve user_id, username, role_id y permisos.
    """
    return service.inspect_token_data_raw(token, db)
