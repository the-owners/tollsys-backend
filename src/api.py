from fastapi import FastAPI
from src.payment_methods.controller import router as payment_methods_router
from src.users.controller import router as users_router
from src.auth.controller import router as auth_router
from src.vehicle_types.controller import router as vehicle_types
from src.tolls.controller import router as tolls
from src.booths.controller import router as booths
from src.toll_payments.controller import router as toll_payment

def register_routes(app: FastAPI):
    app.include_router(users_router)
    app.include_router(payment_methods_router)
    app.include_router(users_router)
    app.include_router(auth_router)
    app.include_router(vehicle_types)
    app.include_router(tolls)
    app.include_router(booths)
    app.include_router(toll_payment)
