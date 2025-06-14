from fastapi import FastAPI, HTTPException
from fastapi import Body
from pydantic import BaseModel
from typing import Optional
from random import randrange

app = FastAPI()

class Post(BaseModel):
    title: str
    content: str
    published: bool = True
    rating: Optional[int] = None

my_posts = [
    {"id": 1, "title": "First Post", "content": "This is the content of the first post."},
    {"id": 2, "title": "Second Post", "content": "This is the content of the second post."},
    {"id": 3, "title": "Third Post", "content": "This is the content of the third post."},
    {"id": 4, "title": "Fourth Post", "content": "This is the content of the fourth post."}
]

@app.get("/posts")
def get_posts():
    return {"data": my_posts}

@app.post("/posts")
def create_post(payload: Post):
    posts_dict = payload.dict()
    posts_dict['id'] = randrange(0, 1000000)
    my_posts.append(posts_dict)
    return {"data": posts_dict}

@app.get("/posts/latest")
def get_latest_post():
    if not my_posts:
        raise HTTPException(status_code=404, detail="No posts available")
    latest_post = my_posts[-1]
    return {"data": latest_post}

def find_post(id: int):
    for post in my_posts:
        if post['id'] == id:
            return post
    return None

@app.get("/posts/{id}")
def get_post(id: int):
    post = find_post(id)
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    return {"data": post}

