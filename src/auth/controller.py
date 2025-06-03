from typing import Annotated

from fastapi import APIRouter, Body, Depends
from fastapi.security import OAuth2PasswordRequestForm

from src.auth import models, service
from src.database.core import SessionDep

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/login", response_model=models.LoginResponse)
def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()], db: SessionDep):
    return service.login(form_data, db)


@router.post("/logout")
def logout(
    current_user: service.CurrentUser, reason: str, observations: str, db: SessionDep
):
    service.logout(current_user, reason, observations, db)
    return {"message": "Successfully logged out"}


@router.post("/inspect-token", summary="Inspect any JWT", response_model=dict)
def inspect_token_endpoint(
    db: SessionDep,
    token: str = Body(..., embed=True, description="JWT token to be inspected"),
):
    """
    Recibe un token JWT en el body y devuelve user_id, username, role_id y permisos.
    """
    return service.inspect_token_data_raw(token, db)
