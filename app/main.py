from fastapi import FastAPI, HTTPException, status, Depends
from fastapi import Body
from pydantic import BaseModel
from typing import Optional
from random import randrange
import psycopg2
from psycopg2.extras import RealDictCursor
import time
from sqlalchemy.orm import Session
from . import model
from . database import engine, get_db

model.Base.metadata.create_all(bind=engine)

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

@app.get("/posts/{id}")
def get_post(id: int):
    cursor.execute("SELECT * FROM post WHERE id = %s", (id,))
    post = cursor.fetchone()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id {id} not found")
    return {"data": post}

@app.delete("/posts/{id}", status_code=status.HTTP_200_OK)
def delete_post(id: int):
    cursor.execute("DELETE FROM post WHERE id = %s RETURNING *", (id,))
    deleted_post = cursor.fetchone()
    conn.commit()
    if not deleted_post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id {id} not found")
    return {"detail": "Post deleted successfully"}

@app.put("/posts/{id}")
def update_post(id: int, payload: Post):
    cursor.execute(
        "UPDATE post SET title = %s, content = %s, published = %s WHERE id = %s RETURNING *",
        (payload.title, payload.content, payload.published, id)
    )
    updated_post = cursor.fetchone()
    conn.commit()
    if not updated_post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id {id} not found")
    return {"data": updated_post}

@app.get("/sqlalchemy")
def get_test_sqlalchemy(db: Session = Depends(get_db)):
    posts = db.query(model.Post).all()
    return {"data": posts}