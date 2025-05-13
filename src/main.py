from fastapi import FastAPI
from .api import register_routes
from src.auth.service import setup_middlewares

app = FastAPI()

register_routes(app)
setup_middlewares(app)
