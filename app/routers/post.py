from fastapi import FastAPI, HTTPException, status, Depends, APIRouter
from typing import Optional

from sqlalchemy import func
from sqlalchemy.orm import Session
from .. import model, schemas, auth2
from ..database import engine, get_db
from .. import auth2

router = APIRouter(
    prefix="/posts",  
)

@router.get("/", response_model=list[schemas.PostResponse])
def get_posts(db: Session = Depends(get_db), current_user: int = Depends(auth2.get_current_user), limit: int = 10, skip: int = 0, search: Optional[str] = ""):
    posts = db.query(model.Post).filter(model.Post.title.contains(search)).limit(limit).offset(skip).all()
    posts_with_votes = (
        db.query(
            model.Post,
            func.count(model.Vote.post_id).label("votes_count")
        )
        .outerjoin(model.Vote, model.Post.id == model.Vote.post_id)
        .filter(model.Post.title.contains(search))
        .group_by(model.Post.id)
        .limit(limit)
        .offset(skip)
        .all()
    )
    if not posts_with_votes:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No posts found for the current user")
    # Convert to list of PostResponse with votes_count
    return [
        schemas.PostResponse(
            **post.__dict__,
            votes_count=votes_count
        )
        for post, votes_count in posts_with_votes
    ]
    return posts

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
def create_post(payload: schemas.PostCreate, db: Session = Depends(get_db), current_user: int = Depends(auth2.get_current_user)):
    new_post = model.Post(ovener_id = current_user.id, **payload.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post

@router.get("/{id}", response_model=schemas.PostResponse)
def get_post(id: int, db: Session = Depends(get_db), current_user: int = Depends(auth2.get_current_user)):
    post = db.query(model.Post).filter(model.Post.id == id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id {id} not found")
    # if post.ovener_id != current_user.id:
    #     raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to view this post")
    return post

@router.delete("/{id}", status_code=status.HTTP_200_OK)
def delete_post(id: int, db: Session = Depends(get_db), current_user: int = Depends(auth2.get_current_user)):
    post = db.query(model.Post).filter(model.Post.id == id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id {id} not found")
    
    if post.ovener_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to delete this post")
    
    db.delete(post)
    db.commit()
    return {"detail": "Post deleted successfully"}
   
@router.put("/{id}", response_model=schemas.PostResponse)
def update_post(id: int, payload: schemas.PostCreate, db: Session = Depends(get_db), current_user: int = Depends(auth2.get_current_user)):
    post_query = db.query(model.Post).filter(model.Post.id == id)
    post = post_query.first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id {id} not found")
    if post.ovener_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to update this post")
    post_query.update(payload.dict(), synchronize_session=False)
    db.commit()
    return post_query.first()