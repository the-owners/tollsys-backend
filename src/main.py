from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.api import register_routes
from src.database.core import create_db_and_tables
from src.database.initialize_data import initialize_first_data

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
    initialize_first_data()


register_routes(app)
