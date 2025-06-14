from fastapi import FastAPI, HTTPException, status
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

@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_post(payload: Post):
    posts_dict = payload.dict()
    posts_dict['id'] = randrange(0, 1000000)
    my_posts.append(posts_dict)
    return {"data": posts_dict}

def find_post(id: int):
    for post in my_posts:
        if post['id'] == id:
            return post
    return None

def find_index_post(id: int):
    for i, post in enumerate(my_posts):
        if post['id'] == id:
            return i
    return None

@app.get("/posts/{id}")
def get_post(id: int):
    post = find_post(id)
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id {id} not found")
    return {"data": post}

@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int):
    index = find_index_post(id)
    if index is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id {id} not found")
    my_posts.pop(index)
    return {"message": "Post deleted successfully"}

