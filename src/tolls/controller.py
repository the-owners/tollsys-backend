from typing import Annotated

from fastapi import APIRouter, HTTPException, Query, status
from sqlmodel import select

from src.database.core import SessionDep
from src.tolls.models import Toll, TollCreate, TollPublic, TollUpdate

router = APIRouter(prefix="/toll", tags=["Tolls"])


@router.post(
    "/",
    response_model=TollPublic,
    status_code=status.HTTP_201_CREATED,
    responses={
        status.HTTP_201_CREATED: {
            "description": "Toll created sucessfully.",
            "model": TollPublic,
        }
    },
)
def create_toll(toll: TollCreate, session: SessionDep):
    db_toll = Toll.model_validate(toll)
    session.add(db_toll)
    session.commit()
    session.refresh(db_toll)
    return db_toll


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
