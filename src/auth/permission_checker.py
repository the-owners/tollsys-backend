def has_permission(user: User, permission: str) -> bool:
    # Verificar permisos directos
    if permission in [p.name for p in user.role.permissions]:
        return True
        
    # Lógica de herencia (ej: admin tiene todos los permisos)
    if user.role.name == SystemRoles.ADMIN:
        return True
        
    # Puedes añadir más reglas de herencia aquí
    return False