import os
from typing import Annotated, Any

from dotenv import load_dotenv
from fastapi import Depends
from sqlmodel import Session, SQLModel, create_engine

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///tollsys-backend.db")
connect_args: dict[str, Any] = {}

if DATABASE_URL.startswith("sqlite"):
    connect_args.setdefault("check_same_thread", False)

engine = create_engine(DATABASE_URL, connect_args=connect_args)


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)


def get_session():
    with Session(engine) as session:
        yield session


SessionDep = Annotated[Session, Depends(get_session)]
