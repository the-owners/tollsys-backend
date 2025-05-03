from enum import Enum

class PermissionEnum(str, Enum):
    # Administración
    MANAGE_USERS = "manage_users"
    MANAGE_ROLES = "manage_roles"
    MANAGE_TOLLS = "manage_tolls"
    
    # Operaciones
    PROCESS_PAYMENT = "process_payment"
    GENERATE_REPORTS = "generate_reports"
    
    # Consultas
    VIEW_TRANSACTIONS = "view_transactions"
    VIEW_OWN_DATA = "view_own_data"