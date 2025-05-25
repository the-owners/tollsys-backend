from ..database.core import SessionDep
from ..auth.service import CurrentUser
from typing import List
from . import models

def has_permission(
    user: CurrentUser,
    required_permission: models.PermissionEnum
) -> bool:
    # superuser bypass to be implemented
    # whole function yet to be implemented
    return True
