from fastapi import FastAPI
from .database.core import create_db_and_tables, SessionDep
from .api import register_routes

app = FastAPI()

@app.on_event("startup")
def on_startup():
    create_db_and_tables()

register_routes(app)
