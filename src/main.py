from fastapi import FastAPI
from .database.core import create_db_and_tables, initialize_first_data, SessionDep
from .api import register_routes
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
def on_startup():
    create_db_and_tables()
    initialize_first_data() # and tbh, we should use a migration script or sum

register_routes(app)
