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
    prefix="/payment_methods",
    tags=["Payment Methods"]
)

@router.post("/", response_model=PaymentMethodPublic, status_code=status.HTTP_201_CREATED, responses={status.HTTP_201_CREATED: {"description": "Payment method created sucessfully.", "model": PaymentMethodPublic}})
def create_payment_method(payment_method: PaymentMethodCreate, session: SessionDep):
    db_payment_method = PaymentMethod.model_validate(payment_method)
    session.add(db_payment_method)
    session.commit()
    session.refresh(db_payment_method)
    return db_payment_method
    # way too convoluted for the moment, we're just getting started no thanks.
    # return JSONResponse(status_code=status.HTTP_201_CREATED, content=jsonable_encoder(db_payment_method))


@router.get("/", response_model=list[PaymentMethodPublic])
def read_payment_methods(
    session: SessionDep,
    offset: int = 0,
    limit: Annotated[int, Query(le=100)] = 100,
):
    payment_methods = session.exec(select(PaymentMethod).offset(offset).limit(limit)).all()
    return payment_methods


@router.get("/{payment_method_id}", response_model=PaymentMethodPublic)
def read_payment_method(payment_method_id: int, session: SessionDep):
    payment_method = session.get(PaymentMethod, payment_method_id)
    if not payment_method:
        raise HTTPException(status_code=404, detail="Payment Method not found")
    return payment_method


@router.patch("/{payment_method_id}", response_model=PaymentMethodPublic)
def update_payment_method(payment_method_id: int, payment_method: PaymentMethodUpdate, session: SessionDep):
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
def delete_payment_method(payment_method_id: int, session: SessionDep):
    payment_method = session.get(PaymentMethod, payment_method_id)
    if not payment_method:
        raise HTTPException(status_code=404, detail="Payment Method not found")
    session.delete(payment_method)
    session.commit()
    return {"Payment method deleted sucessfully": True}