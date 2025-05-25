from fastapi import FastAPI
from src.payment_methods.controller import router as payment_methods_router
from src.users.controller import router as users_router
from src.auth.controller import router as auth_router
from src.vehicle_types.controller import router as vehicle_types_router
from src.tolls.controller import router as tolls_router
from src.booths.controller import router as booths_router
from src.toll_payments.controller import router as toll_payment_router
from src.role_permissions.controller import router as role_permissions_router
from src.roles.controller import router as roles_router
from src.permissions.controller import router as permissions_router

def register_routes(app: FastAPI):

    app.include_router(users_router)
    app.include_router(payment_methods_router)
    app.include_router(auth_router)
    app.include_router(vehicle_types_router)
    app.include_router(tolls_router)
    app.include_router(booths_router)
    app.include_router(toll_payment_router)
    
    # para el RBAC
    app.include_router(roles_router, prefix="/api/v1/roles", tags=["Roles"])
    app.include_router(permissions_router, prefix="/api/v1/permissions", tags=["Permissions"])
    app.include_router(role_permissions_router, prefix="/api/v1/role-permissions", tags=["Role-Permissions"])
