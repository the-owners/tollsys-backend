import datetime

from sqlmodel import Session, select

from src.database.core import engine
from src.permissions.models import Permission
from src.role_permissions.models import RolePermission
from src.roles.models import Role
from src.tolls.models import Toll
from src.users.models import User


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
            created_by=None,
        )
        session.add(toll)

        role = Role(
            name="Admin",
            created_at=datetime.datetime.now(datetime.timezone.utc),
            created_by=None,
        )
        session.add(role)

        session.commit()

        user = User(
            name="Superuser",
            username="root",
            password="$2b$12$AIR2ZnzYAWfWoS/gp39aHO9/A7LhbEP/K0AJFTWVSAfzxi//J/VNa",  # toor
            role_id=role.id,
            toll_id=toll.id,
            created_at=datetime.datetime.now(datetime.timezone.utc),
            created_by=None,
        )

        session.add(user)
        session.commit()

        toll.created_by = user.id
        role.created_by = user.id
        session.add(toll)
        session.add(role)
        session.commit()

        permissions = [
            Permission(name="manage_users"),  # id 1
            Permission(name="process_payments"),  # id 2
        ]
        session.add_all(permissions)
        session.commit()

        admin_role_permissions = [
            RolePermission(role_id=1, permission_id=1),
            RolePermission(role_id=1, permission_id=2),
        ]
        session.add_all(admin_role_permissions)
        session.commit()
