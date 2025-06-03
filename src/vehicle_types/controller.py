from typing import Annotated

from fastapi import APIRouter, HTTPException, Query, status
from sqlmodel import select

from src.auth.service import CurrentUser
from src.core.models import MetadataMixin
from src.database.core import SessionDep
from src.vehicle_types.models import (
    VehicleType,
    VehicleTypeCreate,
    VehicleTypePublic,
    VehicleTypeResponse,
    VehicleTypeUpdate,
)

router = APIRouter(prefix="/vehicle_types", tags=["Vehicle Types"])


@router.post(
    "/",
    response_model=VehicleTypePublic,
    status_code=status.HTTP_201_CREATED,
    responses={
        status.HTTP_201_CREATED: {
            "description": "Vehicle type created sucessfully.",
            "model": VehicleTypePublic,
        }
    },
)
def create_vehicle_type(
    current_user: CurrentUser, vehicle_type: VehicleTypeCreate, session: SessionDep
):
    db_vehicle_type = VehicleType.model_validate(vehicle_type)
    session.add(db_vehicle_type)
    session.commit()
    session.refresh(db_vehicle_type)
    return db_vehicle_type


@router.get("/active", response_model=list[VehicleTypePublic])
def read_active_vehicle_types(
    session: SessionDep,
    current_user: CurrentUser,
):
    query = select(VehicleType).where(VehicleType.active)
    results = session.exec(query).all()
    return results


@router.get("/", response_model=VehicleTypeResponse)
def read_vehicle_types(
    session: SessionDep,
    current_user: CurrentUser,
    page: int = 1,
    per_page: Annotated[int, Query(le=100)] = 10,
    search: str = "",  # puedes usarlo para filtrar más adelante
):
    offset = (page - 1) * per_page
    base_query = select(VehicleType)
    if search:
        base_query = base_query.where(VehicleType.name.ilike(f"%{search}%"))

    results = session.exec(base_query.offset(offset).limit(per_page)).all()
    total = len(results)
    total_pages = (total + per_page - 1) // per_page

    metadata = MetadataMixin(
        page=page,
        total=total,
        per_page=per_page,
        total_pages=total_pages,
        search=search,
    )

    return VehicleTypeResponse(metadata=metadata, data=results)


@router.get("/{vehicle_type_id}", response_model=VehicleTypePublic)
def read_vehicle_type(
    current_user: CurrentUser, vehicle_type_id: int, session: SessionDep
):
    vehicle_type = session.get(VehicleType, vehicle_type_id)
    if not vehicle_type:
        raise HTTPException(status_code=404, detail="Vehicle Type not found")
    return vehicle_type


@router.patch("/{vehicle_type_id}", response_model=VehicleTypePublic)
def update_vehicle_type(
    current_user: CurrentUser,
    vehicle_type_id: int,
    vehicle_type: VehicleTypeUpdate,
    session: SessionDep,
):
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
def delete_vehicle_type(
    current_user: CurrentUser, vehicle_type_id: int, session: SessionDep
):
    vehicle_type = session.get(VehicleType, vehicle_type_id)
    if not vehicle_type:
        raise HTTPException(status_code=404, detail="Vehicle type not found")
    session.delete(vehicle_type)
    session.commit()
    return {"Vehicle type deleted sucessfully": True}
