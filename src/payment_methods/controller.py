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
from ..auth.service import CurrentUser

router = APIRouter(
    prefix="/payment_methods",
    tags=["Payment Methods"]
)

@router.post("/", response_model=PaymentMethodPublic, status_code=status.HTTP_201_CREATED, responses={status.HTTP_201_CREATED: {"description": "Payment method created sucessfully.", "model": PaymentMethodPublic}})
def create_payment_method(payment_method: PaymentMethodCreate, current_user: CurrentUser, session: SessionDep):
    db_payment_method = PaymentMethod.model_validate(payment_method)
    session.add(db_payment_method)
    session.commit()
    session.refresh(db_payment_method)
    return db_payment_method
    # return JSONResponse(status_code=status.HTTP_201_CREATED, content=jsonable_encoder(db_payment_method))


@router.get("/", response_model=PaymentMethodResponse)
def read_payment_methods(
    session: SessionDep,
    current_user: CurrentUser,
    page: int = 1,
    per_page: Annotated[int, Query(le=100)] = 10,
    search: str = "",  # puedes usarlo para filtrar más adelante
):
    offset = (page - 1) * per_page

    statement = select(PaymentMethod).offset(offset).limit(per_page)
    payment_methods = session.exec(statement).all()

    total = len(payment_methods)
    total_pages = (total + per_page - 1) // per_page

    metadata = Metadata(
        page=page,
        total=total,
        per_page=per_page,
        total_pages=total_pages,
        search=search
    )

    return PaymentMethodResponse(metadata=metadata, data=payment_methods)


@router.get("/{payment_method_id}", response_model=PaymentMethodPublic)
def read_payment_method(payment_method_id: int, session: SessionDep, current_user: CurrentUser):
    payment_method = session.get(PaymentMethod, payment_method_id)
    if not payment_method:
        raise HTTPException(status_code=404, detail="Payment Method not found")
    return payment_method


@router.patch("/{payment_method_id}", response_model=PaymentMethodPublic)
def update_payment_method(payment_method_id: int, payment_method: PaymentMethodUpdate, session: SessionDep, current_user: CurrentUser):
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
def delete_payment_method(payment_method_id: int, session: SessionDep, current_user: CurrentUser):
    payment_method = session.get(PaymentMethod, payment_method_id)
    if not payment_method:
        raise HTTPException(status_code=404, detail="Payment Method not found")
    session.delete(payment_method)
    session.commit()
    return {"Payment method deleted sucessfully": True}