from fastapi import FastAPI
from src.payment_methods.controller import router as payment_methods_router
from src.users.controller import router as users_router

def register_routes(app: FastAPI):
    app.include_router(payment_methods_router)
    app.include_router(users_router)