from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from .. import database, schemas, model, utils

router = APIRouter(tags=["authentication"])

@router.post("/login")
def login(user_credentials: schemas.UserLogin, db: Session = Depends(database.get_db)):
    user = db.query(model.User).filter(model.User.email == user_credentials.email).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    if not utils.verify_password(user_credentials.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Incorrect password"
        )
    
    return {"message": "Login successful"}