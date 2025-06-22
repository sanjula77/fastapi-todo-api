from fastapi import FastAPI, HTTPException, status, Depends, APIRouter

from sqlalchemy.orm import Session
from .. import model, schemas, utils
from ..database import engine, get_db

router = APIRouter()

@router.post("/users", status_code=status.HTTP_201_CREATED, response_model=schemas.UserResponse)
def UserCreate(payload: schemas.UserCreate, db: Session = Depends(get_db)):
    # Hash the password
    hashed_password = utils.hash_password(payload.password)
    payload.password = hashed_password
    # Create the user
    new_user = model.User(**payload.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@router.get("/users/{id}", response_model=schemas.UserResponse)
def get_user(id: int, db: Session = Depends(get_db)):
    user = db.query(model.User).filter(model.User.id == id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with id {id} not found")
    return user