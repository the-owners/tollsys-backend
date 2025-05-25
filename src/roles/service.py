from sqlmodel import Session, select
from .models import Role, RoleCreate, RoleUpdate
from typing import List
from fastapi import HTTPException
from datetime import datetime

class RoleService:
    def __init__(self, session: Session):
        self.session = session

    def create_role(self, role_data: RoleCreate, created_by: int) -> Role:
        role = Role(**role_data.model_dump(), created_by=created_by)
        self.session.add(role)
        self.session.commit()
        self.session.refresh(role)
        return role

    def get_role(self, role_id: int) -> Role:
        role = self.session.get(Role, role_id)
        if not role:
            raise HTTPException(status_code=404, detail="Role not found")
        return role

    def get_roles(self) -> List[Role]:
        roles = self.session.exec(select(Role)).all()
        return roles

    def update_role(self, role_id: int, role_data: RoleUpdate, updated_by: int) -> Role:
        role = self.get_role(role_id)
        role_data_dict = role_data.model_dump(exclude_unset=True)
        
        for key, value in role_data_dict.items():
            setattr(role, key, value)
            
        role.updated_at = datetime.utcnow()
        role.updated_by = updated_by
        
        self.session.add(role)
        self.session.commit()
        self.session.refresh(role)
        return role

    def delete_role(self, role_id: int):
        role = self.get_role(role_id)
        self.session.delete(role)
        self.session.commit()
        return {"message": "Role deleted successfully"}