from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from ..database import get_db
from .. import model, schemas, utils

router = APIRouter(
    prefix="/votes",
    tags=["Votes"]
)

@router.post("/", status_code=status.HTTP_201_CREATED)
def create_vote(vote: schemas.Vote, db: Session = Depends(get_db), current_user: int = Depends(utils.get_current_user)):
    # Check if the post exists
    post = db.query(model.Post).filter(model.Post.id == vote.post_id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")

    # Check if the user has already voted for this post
    existing_vote = db.query(model.Vote).filter(
        model.Vote.post_id == vote.post_id,
        model.Vote.user_id == current_user.id
    ).first()
    
    if existing_vote:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="User has already voted for this post")

    new_vote = model.Vote(post_id=vote.post_id, user_id=current_user.id)
    db.add(new_vote)
    db.commit()
    db.refresh(new_vote)
    
    return new_vote
   