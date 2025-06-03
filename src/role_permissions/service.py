from fastapi import HTTPException
from sqlmodel import Session, select

from src.auth.service import CurrentUser
from src.role_permissions.models import RolePermission


def create_role_permission(
    role_id: int, permission_id: int, current_user: CurrentUser, session: Session
):
    existing = session.exec(
        select(RolePermission).where(
            RolePermission.role_id == role_id,
            RolePermission.permission_id == permission_id,
        )
    ).first()
    if existing:
        raise HTTPException(
            status_code=400, detail="Permission already assigned to role"
        )

    rp = RolePermission(
        role_id=role_id,
        permission_id=permission_id,
        created_by=current_user.id,
        updated_by=current_user.id,
    )
    session.add(rp)
    session.commit()
    session.refresh(rp)
    return rp


def get_permissions_by_role(role_id: int, session: Session):
    return session.exec(
        select(RolePermission).where(RolePermission.role_id == role_id)
    ).all()


def delete_role_permission(role_id: int, permission_id: int, session: Session):
    rp = session.exec(
        select(RolePermission).where(
            RolePermission.role_id == role_id,
            RolePermission.permission_id == permission_id,
        )
    ).first()
    if not rp:
        raise HTTPException(status_code=404, detail="RolePermission not found")

    session.delete(rp)
    session.commit()
    return {"ok": True}
