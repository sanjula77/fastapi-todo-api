from fastapi import FastAPI, HTTPException, status
from fastapi import Body
from pydantic import BaseModel
from typing import Optional
from random import randrange
import psycopg2
from psycopg2.extras import RealDictCursor
import time

app = FastAPI()

class Post(BaseModel):
    title: str
    content: str
    published: bool = True

# Database connection with retry logic
while True:
    try:
        conn = psycopg2.connect(
            host='localhost',
            database='fastApiDb',
            user='postgres',
            password='4858@',
            cursor_factory=RealDictCursor
        )
        cursor = conn.cursor()
        print("Database connection successful")
        break
    except Exception as e:
        print("Database connection failed. Retrying in 5 seconds...")
        print(f"Error: {e}")
        time.sleep(5)

my_posts = [
    {"id": 1, "title": "First Post", "content": "This is the content of the first post."},
    {"id": 2, "title": "Second Post", "content": "This is the content of the second post."},
    {"id": 3, "title": "Third Post", "content": "This is the content of the third post."},
    {"id": 4, "title": "Fourth Post", "content": "This is the content of the fourth post."}
]

@app.get("/posts")
def get_posts():
    cursor.execute("SELECT * FROM post")
    posts = cursor.fetchall()
    if not posts:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No posts found")
    return {"data": posts}

@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_post(payload: Post):
    cursor.execute(
        "INSERT INTO post (title, content, published) VALUES (%s, %s, %s) RETURNING *",
        (payload.title, payload.content, payload.published)
    )
    new_post = cursor.fetchone()
    conn.commit()
    if not new_post:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Failed to create post")
    return {"data": new_post}

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

@app.put("/posts/{id}")
def update_post(id: int, payload: Post):
    index = find_index_post(id)
    if index is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id {id} not found")
    
    my_posts[index].update(payload.dict())
    return {"data": my_posts[index]}