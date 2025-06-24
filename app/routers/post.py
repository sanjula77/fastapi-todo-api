from fastapi import FastAPI, HTTPException, status, Depends, APIRouter

from sqlalchemy.orm import Session
from .. import model, schemas, auth2
from ..database import engine, get_db
from .. import auth2

router = APIRouter(
    prefix="/posts",
)

@router.get("/", response_model=list[schemas.PostResponse])
def get_posts(db: Session = Depends(get_db), get_current_user: int = Depends(auth2.get_current_user)):
    posts = db.query(model.Post).all()
    return posts

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.PostResponse)
def create_post(payload: schemas.PostCreate, db: Session = Depends(get_db), user_id: int = Depends(auth2.get_current_user)):
    new_post = model.Post(**payload.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post

@router.get("/{id}", response_model=schemas.PostResponse)
def get_post(id: int, db: Session = Depends(get_db)):
    post = db.query(model.Post).filter(model.Post.id == id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id {id} not found")
    return post

@router.delete("/{id}", status_code=status.HTTP_200_OK)
def delete_post(id: int, db: Session = Depends(get_db)):
    post = db.query(model.Post).filter(model.Post.id == id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id {id} not found")
    db.delete(post)
    db.commit()
    return {"detail": "Post deleted successfully"}
   
@router.put("/{id}", response_model=schemas.PostResponse)
def update_post(id: int, payload: schemas.PostCreate, db: Session = Depends(get_db)):
    post_query = db.query(model.Post).filter(model.Post.id == id)
    post = post_query.first()
    
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id {id} not found")
    
    post_query.update(payload.dict(), synchronize_session=False)
    db.commit()
    
    return post_query.first()