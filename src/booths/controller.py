from typing import Annotated
from fastapi import HTTPException, Query, APIRouter, status
from sqlmodel import select
from src.database.core import SessionDep
from src.booths.models import *
from src.auth.service import CurrentUser

router = APIRouter(prefix="/booths", tags=["Booths"])


@router.post(
    "/",
    response_model=BoothPublic,
    status_code=status.HTTP_201_CREATED,
    responses={
        status.HTTP_201_CREATED: {
            "description": "Booth created sucessfully.",
            "model": BoothPublic,
        }
    },
)
def create_booth(booth: BoothCreate, current_user: CurrentUser, session: SessionDep):
    db_booth = Booth.model_validate(booth)
    session.add(db_booth)
    session.commit()
    session.refresh(db_booth)
    return db_booth


@router.get("/", response_model=BoothResponse)
def read_booths(
    session: SessionDep,
    current_user: CurrentUser,
    page: int = 1,
    per_page: Annotated[int, Query(le=100)] = 10,
    search: str = "",
):
    offset = (page - 1) * per_page

    # Filtro opcional por nombre o descripción
    base_query = select(Booth)
    if search:
        base_query = base_query.where(Booth.name.ilike(f"%{search}%"))  # type: ignore

    # Obtener total filtrado
    results = session.exec(base_query.offset(offset).limit(per_page)).all()
    total = len(results)
    total_pages = (total + per_page - 1) // per_page

    metadata = Metadata(
        page=page,
        total=total,
        per_page=per_page,
        total_pages=total_pages,
        search=search,
    )

    return BoothResponse(metadata=metadata, data=results)  # type: ignore


@router.get("/active", response_model=list[BoothPublic])
def read_active_booths(
    session: SessionDep,
    current_user: CurrentUser,
):
    query = select(Booth).where(Booth.active == True)
    results = session.exec(query).all()
    return results


@router.get("/{booth_id}", response_model=BoothPublic)
def read_booth(booth_id: int, session: SessionDep, current_user: CurrentUser):
    booth = session.get(Booth, booth_id)
    if not booth:
        raise HTTPException(status_code=404, detail="Booth not found")
    return booth


@router.patch("/{booth_id}", response_model=BoothPublic)
def update_booth(
    booth_id: int, booth: BoothUpdate, session: SessionDep, current_user: CurrentUser
):
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
def delete_booth(booth_id: int, session: SessionDep, current_user: CurrentUser):
    booth = session.get(Booth, booth_id)
    if not booth:
        raise HTTPException(status_code=404, detail="Booth not found")
    session.delete(booth)
    session.commit()
    return {"Booth deleted sucessfully": True}
