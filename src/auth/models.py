from sqlmodel import SQLModel

from src.users.models import UserPublic


class Token(SQLModel):
    access_token: str
    token_type: str


class TokenData(SQLModel):
    user_id: int | None = None
    role_id: int | None = None
    username: str | None = None


class LoginResponse(SQLModel):
    access_token: str
    token_type: str
    user: UserPublic
