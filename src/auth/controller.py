from typing import Annotated
from fastapi import APIRouter, Depends, Request
from starlette import status
from . import  models
from . import service
from ..users.models import UserCreate
from fastapi.security import OAuth2PasswordRequestForm
from ..database.core import SessionDep
router = APIRouter(
    prefix='/auth',
    tags=['auth']
)

# rn, i have a dilemma, as i feel this should be part of /users instead
@router.post("/", status_code=status.HTTP_201_CREATED)
async def register_user(request: Request, db: SessionDep,
                      register_user_request: UserCreate):
    service.register_user(db, register_user_request)

@router.post("/login", response_model=models.Token)
async def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
                                 db: SessionDep):
    return service.login(form_data, db)
