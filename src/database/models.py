from sqlmodel import SQLModel
from src.auth.models import *
from src.booths.models import *
from src.payment_methods.models import *
#from src.permissions.models import *
from src.receipt_payments.models import *
from src.receipts.models import *
#from src.role_permissions.models import *
from src.roles.models import *
#from src.toll_payments.models import *
from src.tolls.models import *
from src.users.models import *
from src.vehicle_types.models import *

__all__ = ["SQLModel"] 
