from fastapi import FastAPI, HTTPException, status, Depends
from fastapi import Body
from pydantic import BaseModel
from typing import Optional
from random import randrange
import psycopg2
from psycopg2.extras import RealDictCursor
import time
from sqlalchemy.orm import Session
from . import model, schemas
from . database import engine, get_db

model.Base.metadata.create_all(bind=engine)

app = FastAPI()

@app.get("/sqlalchemy")
def get_test_sqlalchemy(db: Session = Depends(get_db)):
    posts = db.query(model.Post).all()
    return {"data": posts}

@app.get("/posts")
def get_posts(db: Session = Depends(get_db)):
    posts = db.query(model.Post).all()
    return {"data": posts}

@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_post(payload: schemas.Post, db: Session = Depends(get_db)):
    new_post = model.Post(**payload.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return {"data": new_post}

@app.get("/posts/{id}")
def get_post(id: int, db: Session = Depends(get_db)):
    post = db.query(model.Post).filter(model.Post.id == id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id {id} not found")
    return {"data": post}

@app.delete("/posts/{id}", status_code=status.HTTP_200_OK)
def delete_post(id: int, db: Session = Depends(get_db)):
    post = db.query(model.Post).filter(model.Post.id == id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id {id} not found")
    db.delete(post)
    db.commit()
    return {"detail": "Post deleted successfully"}
   
@app.put("/posts/{id}")
def update_post(id: int, payload: schemas.Post, db: Session = Depends(get_db)):
    post_query = db.query(model.Post).filter(model.Post.id == id)
    post = post_query.first()
    
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id {id} not found")
    
    post_query.update(payload.dict(), synchronize_session=False)
    db.commit()
    
    return {"data": post_query.first()}