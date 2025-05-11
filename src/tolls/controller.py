from typing import Annotated
from datetime import datetime
from fastapi import Body, Depends, HTTPException, Query, APIRouter, status
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from sqlmodel import Field, Session, SQLModel, create_engine, select
from ..database.core import SessionDep
from . import  models
from . import service
from .models import *

router = APIRouter(
    prefix="/toll",
    tags=["Tolls"]
)

@router.post("/", response_model=TollPublic, status_code=status.HTTP_201_CREATED, responses={status.HTTP_201_CREATED: {"description": "Toll created sucessfully.", "model": TollPublic}})
def create_toll(toll: TollCreate, session: SessionDep):
    db_toll = Toll.model_validate(toll)
    session.add(db_toll)
    session.commit()
    session.refresh(db_toll)
    return db_toll
    # return JSONResponse(status_code=status.HTTP_201_CREATED, content=jsonable_encoder(db_toll))


@router.get("/", response_model=list[TollPublic])
def read_tolls(
    session: SessionDep,
    offset: int = 0,
    limit: Annotated[int, Query(le=100)] = 100,
):
    tolls = session.exec(select(Toll).offset(offset).limit(limit)).all()
    return tolls


@router.get("/{toll_id}", response_model=TollPublic)
def read_toll(toll_id: int, session: SessionDep):
    toll = session.get(Toll, toll_id)
    if not toll:
        raise HTTPException(status_code=404, detail="Toll not found")
    return toll


@router.patch("/{toll_id}", response_model=TollPublic)
def update_toll(toll_id: int, toll: TollUpdate, session: SessionDep):
    db_toll = session.get(Toll, toll_id)
    if not db_toll:
        raise HTTPException(status_code=404, detail="Toll not found")
    toll_data = toll.model_dump(exclude_unset=True)
    db_toll.sqlmodel_update(toll_data)
    session.add(db_toll)
    session.commit()
    session.refresh(db_toll)
    return db_toll


@router.delete("/{toll_id}")
def delete_toll(toll_id: int, session: SessionDep):
    toll = session.get(Toll, toll_id)
    if not toll:
        raise HTTPException(status_code=404, detail="Toll not found")
    session.delete(toll)
    session.commit()
    return {"Toll deleted sucessfully": True}