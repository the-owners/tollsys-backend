from fastapi import APIRouter, HTTPException, status
from sqlmodel import select

from src.auth.service import CurrentUser
from src.booths.models import Booth, BoothPublic
from src.database.core import SessionDep
from src.payment_methods.models import PaymentMethod, PaymentMethodPublic
from src.toll_payments.models import (
    PaymentMethodTP,
    PaymentMethodTPWrapper,
    TollPayment,
    TollPaymentCreate,
    TollPaymentPublic,
)
from src.tolls.models import Toll, TollPublic
from src.vehicle_types.models import VehicleTypePublic

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
) -> TollPaymentPublic:
    statement = (
        select(Booth.id)
        .join(Toll)
        .where(Booth.toll_id == current_user.toll_id)
        .limit(1)
    )
    current_booth_id: int | None = session.exec(statement).first()

    if not current_booth_id:
        raise HTTPException(
            status_code=404, detail=f"No booth found for toll ID {current_user.toll_id}"
        )

    db_toll_payment = TollPayment(
        booth_id=current_booth_id,
        toll_id=current_user.toll_id,  # type: ignore
        car_type_id=toll_payment.car_type_id,
        created_by=current_user.id,
    )

    session.add(db_toll_payment)
    session.commit()
    session.refresh(db_toll_payment)  # refresh to get id

    # Convert PaymentMethodTPCreate objects to PaymentMethodTP ORM objects
    #    and associate them with the newly created db_toll_payment
    for pmtp_create in toll_payment.amounts:
        statement_pm = (
            select(PaymentMethod)
            .where(PaymentMethod.id == pmtp_create.payment_method_id)
            .limit(1)
        )
        found_pm: PaymentMethod | None = session.exec(statement_pm).first()

        if not found_pm:
            raise HTTPException(
                status_code=404,
                detail=f"PaymentMethod with ID {pmtp_create.payment_method_id} not found.",
            )

        # Create the PaymentMethodTP ORM object
        db_payment_method_tp = PaymentMethodTP(
            toll_payment_id=db_toll_payment.id,  # Link to the parent TollPayment # type: ignore
            payment_method_id=found_pm.id,  # type: ignore
            amount=pmtp_create.value,
        )
        # Add the ORM object to the session
        session.add(db_payment_method_tp)

    session.commit()
    session.refresh(
        db_toll_payment
    )  # Refresh db_toll_payment to load its 'amounts' relationship

    # Now, construct the `wrapped_amounts` (Pydantic objects) for the API RESPONSE
    wrapped_amounts = []
    for pmtp_orm in db_toll_payment.amounts:
        statement_pm = (
            select(PaymentMethod)
            .where(PaymentMethod.id == pmtp_create.payment_method_id)
            .limit(1)
        )
        found_pm: PaymentMethod | None = session.exec(statement_pm).first()

        wrapped_amounts.append(
            PaymentMethodTPWrapper(
                payment_method=PaymentMethodPublic(
                    id=found_pm.id,  # type: ignore
                    name=found_pm.name,  # type: ignore
                    active=found_pm.active,  # type: ignore
                    icon=found_pm.icon,  # type: ignore
                    description=found_pm.description,  # type: ignore
                ),
                amount=pmtp_orm.amount,
            )
        )

    response_toll = TollPublic(
        id=db_toll_payment.toll.id,
        tax_id=db_toll_payment.toll.tax_id,
        legal_name=db_toll_payment.toll.legal_name,
        address=db_toll_payment.toll.address,
    )
    response_booth = BoothPublic(
        id=db_toll_payment.booth.id,
        name=db_toll_payment.booth.name,
        active=db_toll_payment.booth.active,
        status=db_toll_payment.booth.status,
        toll_id=db_toll_payment.booth.toll_id,
    )
    response_car_type = VehicleTypePublic(
        id=db_toll_payment.car_type.id,
        name=db_toll_payment.car_type.name,
        icon=db_toll_payment.car_type.icon,
        rate=db_toll_payment.car_type.rate,
        active=db_toll_payment.car_type.active,
    )

    return TollPaymentPublic(
        id=db_toll_payment.id,  # type: ignore
        receipt_nro=db_toll_payment.receipt_nro,  # type: ignore
        toll=response_toll,
        booth=response_booth,
        car_type=response_car_type,
        amounts=wrapped_amounts,
        created_at=db_toll_payment.created_at,  # type: ignore
    )
