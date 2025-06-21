from pydantic import BaseModel

class Post(BaseModel):
    title: str
    content: str
    published: bool = True

class PostCreate(Post):
    pass

class PostResponse(Post):
    
    class Config:
        orm_mode = True  # This allows Pydantic to read data from SQLAlchemy models