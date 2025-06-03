from typing import Callable

from fastapi import HTTPException, status
from sqlalchemy.orm import selectinload
from sqlmodel import Session, select

from src.auth.service import CurrentUser
from src.database.core import SessionDep
from src.permissions.models import Permission, PermissionCreate, PermissionUpdate
from src.role_permissions.models import RolePermission
from src.roles.models import Role


def create_permission(session: Session, permission: PermissionCreate) -> Permission:
    db_permission = Permission.model_validate(permission)
    session.add(db_permission)
    session.commit()
    session.refresh(db_permission)
    return db_permission


def get_permissions(session: Session):
    return session.exec(select(Permission)).all()


def get_permission(session: Session, permission_id: int):
    return session.get(Permission, permission_id)


def update_permission(
    session: Session, permission_id: int, permission: PermissionUpdate
):
    db_permission = session.get(Permission, permission_id)
    if not db_permission:
        return None
    update_data = permission.model_dump(exclude_unset=True)
    db_permission.sqlmodel_update(update_data)
    session.add(db_permission)
    session.commit()
    session.refresh(db_permission)
    return db_permission


def delete_permission(session: Session, permission_id: int):
    db_permission = session.get(Permission, permission_id)
    if not db_permission:
        return False
    session.delete(db_permission)
    session.commit()
    return True


def has_permission(permission_name: str) -> Callable:
    """
    FastAPI dependency factory to check if the current user has a specific permission.
    Returns a dependency function.
    """

    async def permission_checker(
        session: SessionDep,
        current_user: CurrentUser,
    ):
        if not current_user.role_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="User has no assigned role.",
            )

        # Correct way to eagerly load the permissions associated with the user's role
        user_role = session.exec(
            select(Role)
            .where(Role.id == current_user.role_id)
            .options(
                # Use selectinload for efficient loading of the many-to-many relationship
                # It will load RolePermission objects, and then for each RolePermission,
                # it will load the associated Permission object.
                selectinload(Role.role_permissions).selectinload(
                    RolePermission.permission
                )
            )
        ).first()

        if not user_role:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN, detail="User's role not found."
            )

        # Extract permission names from the loaded role_permissions
        role_permission_names = {
            rp.permission.name
            for rp in user_role.role_permissions
            if rp.permission  # Ensure permission object is not None
        }

        if permission_name not in role_permission_names:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Not enough permissions. Required: '{permission_name}'",
            )
        return True

    return permission_checker
