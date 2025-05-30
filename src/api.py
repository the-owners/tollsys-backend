from fastapi import FastAPI
from src.payment_methods.controller import router as payment_methods_router
from src.users.controller import router as users_router
from src.auth.controller import router as auth_router
from src.vehicle_types.controller import router as vehicle_types
from src.tolls.controller import router as tolls
from src.permissions.controller import router as permissions_router
from src.role_permissions.controller import router as role_permissions_router
from src.roles.controller import router as roles_router
from src.booths.controller import router as booths_router
from src.toll_payments.controller import router as toll_payments_router


def register_routes(app: FastAPI):
    app.include_router(payment_methods_router)
    app.include_router(users_router)
    app.include_router(auth_router)
    app.include_router(vehicle_types)
    app.include_router(tolls)
    app.include_router(permissions_router)
    app.include_router(role_permissions_router)
    app.include_router(roles_router)
    app.include_router(booths_router)
    app.include_router(toll_payments_router)
