from typing import Annotated, Any

from fastapi import Depends
from sqlmodel import Session, create_engine

import os
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///tollsys-backend.db")
connect_args: dict[str, Any] = {}

if DATABASE_URL.startswith("sqlite"):
    connect_args.setdefault("check_same_thread", False)

engine = create_engine(DATABASE_URL, connect_args=connect_args)


def get_session():
    with Session(engine) as session:
        yield session


SessionDep = Annotated[Session, Depends(get_session)]
