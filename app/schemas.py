from pydantic import BaseModel, EmailStr

class Post(BaseModel):
    title: str
    content: str
    published: bool = True

class PostCreate(Post):
    pass

class PostResponse(Post):
    
    class Config:
        orm_mode = True  # This allows Pydantic to read data from SQLAlchemy models

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