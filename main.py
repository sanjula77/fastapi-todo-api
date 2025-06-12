from fastapi import FastAPI, HTTPException
from fastapi import Body
from pydantic import BaseModel

app = FastAPI()

class Post(BaseModel):
    title: str
    content: str

@app.get("/posts")
def get_posts():
    return [
        {"id": 1, "title": "First Post", "content": "This is the content of the first post."},
        {"id": 2, "title": "Second Post", "content": "This is the content of the second post."}
    ]

@app.post("/createpost")
def create_post(payload: Post):
    print(payload)
    return {
        "message": "Post created successfully",
        "post": payload
    }
    
    