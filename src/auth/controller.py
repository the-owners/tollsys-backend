from typing import Annotated
from fastapi import APIRouter, Depends, Request
from starlette import status
from . import  models
from . import service
from ..users.models import UserCreate
from fastapi.security import OAuth2PasswordRequestForm
from ..database.core import SessionDep
from .service import oauth2_bearer # para probar el token en Swagger

router = APIRouter(
    prefix='/auth',
    tags=['auth']
)

# rn, i have a dilemma, as i feel this should be part of /users instead
@router.post("/", status_code=status.HTTP_201_CREATED)
async def register_user(request: Request, db: SessionDep,
                      register_user_request: UserCreate):
    service.register_user(db, register_user_request)

@router.post("/login", response_model=models.LoginResponse)
async def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
                                 db: SessionDep):
    return service.login(form_data, db)


@router.post("/logout")
async def logout(
    current_user: service.CurrentUser, reason: str, observations: str, db: SessionDep
):
    service.logout(current_user, reason, observations, db)
    return {"message": "Successfully logged out"}



@router.get("/me", dependencies=[Depends(oauth2_bearer)])
def me_protected():
    """
    Ruta dummy para que Swagger genere el esquema OAuth2.
    No hace falta que devuelva nada real.
    """
    return {"ok": True}