from auth.dependencies import require_permission
from permissions import PermissionEnum

@router.get("/",
    dependencies=[Depends(require_permission(PermissionEnum.MANAGE_USERS))]
)
def list_users():
    # Solo accesible por admin
    pass

@router.post("/payments",
    dependencies=[Depends(require_permission(PermissionEnum.PROCESS_PAYMENT))]
)
def create_payment():
    # Accesible por taquilleros y admin
    pass