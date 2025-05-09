from typing import Annotated
from fastapi import Body, Depends, HTTPException, Query, APIRouter, status
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from sqlmodel import Field, Session, SQLModel, create_engine, select
from ..database.core import SessionDep
from . import  models
from . import service
from .models import *

router = APIRouter(
    prefix="/booth",
    tags=["Booths"]
)

@router.post("/", response_model=BoothPublic, status_code=status.HTTP_201_CREATED, responses={status.HTTP_201_CREATED: {"description": "Booth created sucessfully.", "model": BoothPublic}})
def create_booth(booth: BoothCreate, session: SessionDep):
    db_booth = Booth.model_validate(booth)
    session.add(db_booth)
    session.commit()
    session.refresh(db_booth)
    return db_booth

@router.get("/", response_model=list[BoothPublic])
def read_booths(
    session: SessionDep,
    offset: int = 0,
    limit: Annotated[int, Query(le=100)] = 100,
):
    booths = session.exec(select(Booth).offset(offset).limit(limit)).all()
    return booths


@router.get("/{booth_id}", response_model=BoothPublic)
def read_booth(booth_id: int, session: SessionDep):
    booth = session.get(Booth, booth_id)
    if not booth:
        raise HTTPException(status_code=404, detail="Booth not found")
    return booth


@router.patch("/{booth_id}", response_model=BoothPublic)
def update_booth(booth_id: int, booth: BoothUpdate, session: SessionDep):
    db_booth = session.get(Booth, booth_id)
    if not db_booth:
        raise HTTPException(status_code=404, detail="Booth not found")
    booth_data = booth.model_dump(exclude_unset=True)
    db_booth.sqlmodel_update(booth_data)
    session.add(db_booth)
    session.commit()
    session.refresh(db_booth)
    return db_booth


@router.delete("/{booth_id}")
def delete_booth(booth_id: int, session: SessionDep):
    booth = session.get(Booth, booth_id)
    if not booth:
        raise HTTPException(status_code=404, detail="Booth not found")
    session.delete(booth)
    session.commit()
    return {"Booth deleted sucessfully": True}
