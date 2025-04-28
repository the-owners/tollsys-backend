from fastapi import FastAPI
from src.payment_methods.controller import router as payment_methods_router

def register_routes(app: FastAPI):
    app.include_router(payment_methods_router)