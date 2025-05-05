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
    prefix="/vehicle_types",
    tags=["Vehicle Types"]
)

@router.post("/", response_model=VehicleTypePublic, status_code=status.HTTP_201_CREATED, responses={status.HTTP_201_CREATED: {"description": "Vehicle type created sucessfully.", "model": VehicleTypePublic}})
def create_payment_method(vehicle_type: VehicleTypeCreate, session: SessionDep):
    db_vehicle_type = VehicleType.model_validate(vehicle_type)
    session.add(db_vehicle_type)
    session.commit()
    session.refresh(db_vehicle_type)
    return db_vehicle_type
    # return JSONResponse(status_code=status.HTTP_201_CREATED, content=jsonable_encoder(db_vehicle_type))


@router.get("/", response_model=list[VehicleTypePublic])
def read_vehicle_types(
    session: SessionDep,
    offset: int = 0,
    limit: Annotated[int, Query(le=100)] = 100,
):
    vehicle_types = session.exec(select(VehicleType).offset(offset).limit(limit)).all()
    return vehicle_types


@router.get("/{vehicle_type_id}", response_model=VehicleTypePublic)
def read_vehicle_type(vehicle_type_id: int, session: SessionDep):
    vehicle_type = session.get(VehicleType, vehicle_type)
    if not vehicle_type:
        raise HTTPException(status_code=404, detail="Payment Method not found")
    return vehicle_type


@router.patch("/{vehicle_type_id}", response_model=VehicleTypePublic)
def update_vehicle_type(vehicle_type_id: int, vehicle_type: VehicleTypeUpdate, session: SessionDep):
    db_vehicle_type = session.get(VehicleType, vehicle_type_id)
    if not db_vehicle_type:
        raise HTTPException(status_code=404, detail="Vehicle type not found")
    vehicle_type_data = vehicle_type.model_dump(exclude_unset=True)
    db_vehicle_type.sqlmodel_update(vehicle_type_data)
    session.add(db_vehicle_type)
    session.commit()
    session.refresh(db_vehicle_type)
    return db_vehicle_type


@router.delete("/{vehicle_type_id}")
def delete_payment_method(vehicle_type_id: int, session: SessionDep):
    vehicle_type = session.get(VehicleType, vehicle_type_id)
    if not vehicle_type:
        raise HTTPException(status_code=404, detail="Vehicle type not found")
    session.delete(vehicle_type)
    session.commit()
    return {"Vehicle type deleted sucessfully": True}