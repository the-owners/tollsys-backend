from typing import Optional
from sqlmodel import SQLModel
from ..users.models import UserPublic

class Token(SQLModel):
    access_token: str
    token_type: str

class TokenData(SQLModel):
    user_id: Optional[int] = None
    role_id: Optional[int] = None
    username: Optional[str] = None

class LoginResponse(SQLModel):
    access_token: str
    token_type: str
    user: UserPublic
