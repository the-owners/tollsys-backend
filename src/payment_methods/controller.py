from typing import Annotated

from fastapi import APIRouter, HTTPException, Query, status
from sqlmodel import select

from src.auth.service import CurrentUser
from src.core.models import MetadataMixin
from src.database.core import SessionDep
from src.payment_methods.models import (
    PaymentMethod,
    PaymentMethodCreate,
    PaymentMethodPublic,
    PaymentMethodResponse,
    PaymentMethodUpdate,
)

router = APIRouter(prefix="/payment_methods", tags=["Payment Methods"])


@router.post(
    "/",
    response_model=PaymentMethodPublic,
    status_code=status.HTTP_201_CREATED,
    responses={
        status.HTTP_201_CREATED: {
            "description": "Payment method created sucessfully.",
            "model": PaymentMethodPublic,
        }
    },
)
def create_payment_method(
    payment_method: PaymentMethodCreate, current_user: CurrentUser, session: SessionDep
):
    db_payment_method = PaymentMethod.model_validate(payment_method)
    session.add(db_payment_method)
    session.commit()
    session.refresh(db_payment_method)
    return db_payment_method


@router.get("/", response_model=PaymentMethodResponse)
def read_payment_methods(
    session: SessionDep,
    current_user: CurrentUser,
    page: int = 1,
    per_page: Annotated[int, Query(le=100)] = 10,
    search: str = "",  # puedes usarlo para filtrar más adelante
):
    offset = (page - 1) * per_page

    # Filtro opcional por nombre o descripción
    base_query = select(PaymentMethod)
    if search:
        base_query = base_query.where(PaymentMethod.name.ilike(f"%{search}%"))

    # Obtener total filtrado
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

    return PaymentMethodResponse(metadata=metadata, data=results)


@router.get("/active", response_model=list[PaymentMethodPublic])
def read_active_payment_methods(
    session: SessionDep,
    current_user: CurrentUser,
):
    query = select(PaymentMethod).where(PaymentMethod.active)
    results = session.exec(query).all()
    return results


@router.get("/{payment_method_id}", response_model=PaymentMethodPublic)
def read_payment_method(
    payment_method_id: int, session: SessionDep, current_user: CurrentUser
):
    payment_method = session.get(PaymentMethod, payment_method_id)
    if not payment_method:
        raise HTTPException(status_code=404, detail="Payment Method not found")
    return payment_method


@router.patch("/{payment_method_id}", response_model=PaymentMethodPublic)
def update_payment_method(
    payment_method_id: int,
    payment_method: PaymentMethodUpdate,
    session: SessionDep,
    current_user: CurrentUser,
):
    db_payment_method = session.get(PaymentMethod, payment_method_id)
    if not db_payment_method:
        raise HTTPException(status_code=404, detail="Payment Method not found")
    payment_method_data = payment_method.model_dump(exclude_unset=True)
    db_payment_method.sqlmodel_update(payment_method_data)
    session.add(db_payment_method)
    session.commit()
    session.refresh(db_payment_method)
    return db_payment_method


@router.delete("/{payment_method_id}")
def delete_payment_method(
    payment_method_id: int, session: SessionDep, current_user: CurrentUser
):
    payment_method = session.get(PaymentMethod, payment_method_id)
    if not payment_method:
        raise HTTPException(status_code=404, detail="Payment Method not found")
    session.delete(payment_method)
    session.commit()
    return {"Payment method deleted sucessfully": True}
