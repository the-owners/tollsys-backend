from sqlmodel import Session, select
from .models import Permission, PermissionCreate, PermissionUpdate

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

def update_permission(session: Session, permission_id: int, permission: PermissionUpdate):
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