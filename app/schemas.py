from pydantic import BaseModel, EmailStr
from typing import Optional


class UserCreate(BaseModel):
    email: EmailStr
    password: str

class UserResponse(BaseModel):
    id: int
    email: EmailStr

    class Config:
        orm_mode = True  # This allows Pydantic to read data from SQLAlchemy models

class UserLogin(BaseModel):
    email: EmailStr
    password: str
class Post(BaseModel):
    title: str
    content: str
    published: bool
    owner: UserResponse

class PostCreate(Post):
    pass

class PostResponse(Post):
    
    class Config:
        orm_mode = True  # This allows Pydantic to read data from SQLAlchemy models

class Token(BaseModel):
    access_token: str
    token_type: str
    
class TokenData(BaseModel):
    id: Optional[int] = None