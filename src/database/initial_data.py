def create_initial_roles_and_permissions(session):
    # Crear permisos
    permissions = {
        perm: Permission(name=perm, description=...)
        for perm in PermissionEnum
    }
    
    # Crear roles con sus permisos
    roles = {
        SystemRoles.ADMIN: [
            PermissionEnum.MANAGE_USERS,
            PermissionEnum.MANAGE_ROLES,
            # Todos los permisos...
        ],
        SystemRoles.CASHIER: [
            PermissionEnum.PROCESS_PAYMENT,
            PermissionEnum.VIEW_TRANSACTIONS,
        ],
        SystemRoles.USER: [
            PermissionEnum.VIEW_OWN_DATA,
        ]
    }
    
    for role_name, perm_names in roles.items():
        role = Role(name=role_name, description=f"Rol de {role_name.value}")
        role.permissions = [permissions[perm] for perm in perm_names]
        session.add(role)
    
    session.commit()