from uuid import UUID
from pydantic import BaseModel, EmailStr
from sqlmodel import SQLModel

class Token(SQLModel):
    access_token: str
    token_type: str
    
class TokenData(SQLModel):
    user_id: int | None = None
