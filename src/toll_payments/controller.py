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
    prefix="/toll_payment",
    tags=["Toll Payments"]
)

@router.post("/", response_model=TollPaymentPublic, status_code=status.HTTP_201_CREATED, responses={status.HTTP_201_CREATED: {"description": "Toll Payment created sucessfully.", "model": TollPaymentPublic}})
def create_toll_payment(toll_payment: TollPaymentCreate, session: SessionDep):
    db_toll_payment = TollPayment.model_validate(toll_payment)
    session.add(db_toll_payment)
    session.commit()
    session.refresh(db_toll_payment)
    return db_toll_payment

@router.get("/", response_model=list[TollPaymentPublic])
def read_toll_payments(
    session: SessionDep,
    offset: int = 0,
    limit: Annotated[int, Query(le=100)] = 100,
):
    toll_payments = session.exec(select(TollPayment).offset(offset).limit(limit)).all()
    return toll_payments


@router.get("/{toll_payment_id}", response_model=TollPaymentPublic)
def read_toll_payment(toll_payment_id: int, session: SessionDep):
    toll_payment = session.get(TollPayment, toll_payment_id)
    if not toll_payment:
        raise HTTPException(status_code=404, detail="Toll Payment not found")
    return toll_payment


@router.patch("/{toll_payment_id}", response_model=TollPaymentPublic)
def update_toll_payment(toll_payment_id: int, toll_payment: TollPaymentUpdate, session: SessionDep):
    db_toll_payment = session.get(TollPayment, toll_payment_id)
    if not db_toll_payment:
        raise HTTPException(status_code=404, detail="Toll Payment not found")
    toll_payment_data = toll_payment.model_dump(exclude_unset=True)
    db_toll_payment.sqlmodel_update(toll_payment_data)
    session.add(db_toll_payment)
    session.commit()
    session.refresh(db_toll_payment)
    return db_toll_payment


@router.delete("/{toll_payment_id}")
def delete_toll_payment(toll_payment_id: int, session: SessionDep):
    toll_payment = session.get(TollPayment, toll_payment_id)
    if not toll_payment:
        raise HTTPException(status_code=404, detail="Toll Payment not found")
    session.delete(toll_payment)
    session.commit()
    return {"Toll Payment deleted sucessfully": True}
