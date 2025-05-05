from typing import Annotated, Union, Any

from fastapi import Depends, FastAPI, HTTPException, Query
from sqlmodel import Field, Session, SQLModel, create_engine, select

import os
from dotenv import load_dotenv

from ..tolls.models import *
from ..users.models import *
from ..roles.models import *
import datetime

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

# this is, not ideal, but it's the best workaround I could find for now
# it's shitty, at best. that db is screaming for a refactor honestly.

def initialize_first_data():
    with Session(engine) as session:
        existing_user = session.exec(select(User)).first()
        if existing_user:
            return  # data already initialized, do nothing.
        
        toll = Toll(
            tax_id="INITIAL001",
            legal_name="Main Toll Plaza",
            address="Initial Address",
            created_at=datetime.datetime.now(datetime.timezone.utc),
            created_by=None # who's going to create this? god?
        )
        session.add(toll)
        
        role = Role(
            name="Admin",
            created_at=datetime.datetime.now(datetime.timezone.utc),
            created_by=None # no one exists yet!
        )
        session.add(role)
        
        session.commit()
        
        user = User(
            name="System Admin",
            username="admin",
            password="securepassword",
            role_id=role.id,
            toll_id=toll.id,
            created_at=datetime.datetime.now(datetime.timezone.utc),
            created_by=None # duh
        )
        session.add(user)
        session.commit()
        
        # mess solved, phew
        toll.created_by = user.id
        role.created_by = user.id
        session.add(toll)
        session.add(role)
        session.commit()
