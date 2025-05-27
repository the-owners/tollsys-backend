from typing import Annotated
from fastapi import Body, Depends, HTTPException, Query, APIRouter, status
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from sqlmodel import Field, Session, SQLModel, create_engine, select
from ..database.core import SessionDep
from . import  models
from . import service
from .models import *
from ..auth.service import CurrentUser
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from src.exceptions import UserNotFoundError

router = APIRouter(
    prefix="/toll_payments",
    tags=["Toll Payments"]
)

@router.post("/", status_code=status.HTTP_201_CREATED, responses={status.HTTP_201_CREATED: {"description": "Toll payment created sucessfully."}})
def change_password(session: SessionDep, current_user: CurrentUser, change_password_request: ChangePasswordRequest):
    service.change_password(session, current_user.id, change_password_request)
    return {"msg": "Password changed sucessfully"}
