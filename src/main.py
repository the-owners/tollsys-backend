from fastapi import FastAPI
from .database.core import create_db_and_tables, initialize_first_data, SessionDep
from .api import register_routes

app = FastAPI()

@app.on_event("startup")
def on_startup():
    create_db_and_tables()
    initialize_first_data() # and tbh, we should use a migration script or sum

register_routes(app)
