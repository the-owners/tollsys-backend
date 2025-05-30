from typing import Annotated
from fastapi import HTTPException, Query, APIRouter, status
from sqlmodel import select
from src.database.core import SessionDep
from src.booths.models import BoothPublic
from src.tolls.models import TollPublic
from src.toll_payments.models import *
from src.auth.service import CurrentUser

router = APIRouter(prefix="/toll_payments", tags=["Toll Payments"])

@router.post(
    "/",
    response_model=TollPaymentPublic,
    status_code=status.HTTP_201_CREATED,
    responses={
        status.HTTP_201_CREATED: {
            "description": "Toll Payment created successfully.",
            "model": TollPaymentPublic,
        }
    },
)
def create_toll_payment(
    toll_payment: TollPaymentCreate, current_user: CurrentUser, session: SessionDep
):
    # Create the TollPayment object
    db_toll_payment = TollPayment(
        booth_id=toll_payment.booth_id,
        toll_id=toll_payment.toll_id,
        car_type_id=toll_payment.car_type_id,
        receipt_nro=toll_payment.receipt_nro,
        created_by=current_user.id,
    )

    # Convert PaymentMethodTPCreate objects to PaymentMethodTP objects
    for payment_method in toll_payment.amounts:
        db_payment_method = PaymentMethodTP(
            payment_method_id=payment_method.payment_method_id,
            amount=payment_method.value,
        )
        db_toll_payment.amounts.append(db_payment_method)

    # Add and commit the TollPayment object
    session.add(db_toll_payment)
    session.commit()
    session.refresh(db_toll_payment)

    return db_toll_payment