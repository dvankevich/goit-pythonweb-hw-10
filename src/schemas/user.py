from pydantic import BaseModel, EmailStr, Field, ConfigDict
from typing import Optional

class User(BaseModel):
    id: int
    username: str
    email: EmailStr
    avatar: Optional[str] = None 
    model_config = ConfigDict(from_attributes=True)


class UserCreate(BaseModel):
    username: str = Field(min_length=3, max_length=50)
    email: EmailStr
    password: str = Field(min_length=6, max_length=100)


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"
