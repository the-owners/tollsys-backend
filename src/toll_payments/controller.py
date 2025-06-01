from typing import Annotated, Optional
from fastapi import HTTPException, Query, APIRouter, status
from sqlmodel import select
from src.database.core import SessionDep
from src.booths.models import Booth, BoothPublic
from src.tolls.models import Toll, TollPublic
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
) -> TollPaymentPublic: # Added return type hint
    # 1. Get the current_booth_id
    statement = (
            select(Booth.id)
            .join(Toll) # Join Booth with Toll to access toll_id
            .where(Booth.toll_id == current_user.toll_id)
            .limit(1) # Select only the first one
    )
    current_booth_id: Optional[int] = session.exec(statement).first()

    if not current_booth_id:
        # Handle case where no booth is found for the current user's toll
        # In a real API, you'd raise an HTTPException (e.g., 404 Not Found)
        raise HTTPException(status_code=404, detail=f"No booth found for toll ID {current_user.toll_id}")

    # 2. Create the TollPayment ORM object (db_toll_payment)
    #    Do NOT assign `amounts` here directly from Pydantic models.
    db_toll_payment = TollPayment(
        booth_id=current_booth_id,
        toll_id=current_user.toll_id,
        car_type_id=toll_payment.car_type_id,
        created_by=current_user.id,
    )

    # 3. Add and commit the TollPayment object to get its ID
    session.add(db_toll_payment)
    session.commit()
    session.refresh(db_toll_payment) # Refresh to get the generated ID

    # 4. Convert PaymentMethodTPCreate objects to PaymentMethodTP ORM objects
    #    and associate them with the newly created db_toll_payment
    for pmtp_create in toll_payment.amounts:
        # Retrieve the PaymentMethod ORM object
        statement_pm = (
            select(PaymentMethod)
            .where(PaymentMethod.id == pmtp_create.payment_method_id)
            .limit(1)
        )
        found_pm: Optional[PaymentMethod] = session.exec(statement_pm).first()

        if not found_pm:
            raise HTTPException(status_code=404, detail=f"PaymentMethod with ID {pmtp_create.payment_method_id} not found.")

        # Create the PaymentMethodTP ORM object
        db_payment_method_tp = PaymentMethodTP(
            toll_payment_id=db_toll_payment.id, # Link to the parent TollPayment
            payment_method_id=found_pm.id,
            amount=pmtp_create.value,
        )
        # Add the ORM object to the session
        session.add(db_payment_method_tp)

    # 5. Commit the PaymentMethodTP objects
    session.commit()
    session.refresh(db_toll_payment) # Refresh db_toll_payment to load its 'amounts' relationship

    # 6. Now, construct the `wrapped_amounts` (Pydantic objects) for the API RESPONSE
    #    Iterate over the ORM objects that are now loaded in db_toll_payment.amounts
    wrapped_amounts = []
    for pmtp_orm in db_toll_payment.amounts:
        statement_pm = (
            select(PaymentMethod)
            .where(PaymentMethod.id == pmtp_create.payment_method_id)
            .limit(1)
        )
        found_pm: Optional[PaymentMethod] = session.exec(statement_pm).first()

        wrapped_amounts.append(PaymentMethodTPWrapper(
            payment_method=PaymentMethodPublic(
                id=found_pm.id,
                name=found_pm.name,
                active=found_pm.active,
                icon=found_pm.icon,
                description=found_pm.description
            ),
            amount=pmtp_orm.amount
        ))

    # 7. Construct the TollPaymentPublic response
    #    Fetch related ORM objects for full response serialization if not already loaded
    #    (e.g., if you didn't use .options(selectinload) for relationships)
    #    Assuming relationships are loaded via refresh or default eager loading for simplicity here.
    response_toll = TollPublic(
        id=db_toll_payment.toll.id,
        tax_id=db_toll_payment.toll.tax_id,
        legal_name=db_toll_payment.toll.legal_name,
        address=db_toll_payment.toll.address
    )
    response_booth = BoothPublic(
        id=db_toll_payment.booth.id,
        name=db_toll_payment.booth.name,
        active=db_toll_payment.booth.active,
        status=db_toll_payment.booth.status,
        toll_id=db_toll_payment.booth.toll_id
    )
    response_car_type = VehicleTypePublic(
        id=db_toll_payment.car_type.id,
        name=db_toll_payment.car_type.name,
        icon=db_toll_payment.car_type.icon,
        rate=db_toll_payment.car_type.rate,
        active=db_toll_payment.car_type.active
    )

    return TollPaymentPublic(
        id=db_toll_payment.id,
        receipt_nro=db_toll_payment.receipt_nro,
        toll=response_toll,
        booth=response_booth,
        car_type=response_car_type,
        amounts=wrapped_amounts, # Use the Pydantic wrapped_amounts for the response
        created_at=db_toll_payment.created_at
    )