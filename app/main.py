from fastapi import FastAPI, HTTPException, status, Depends
from sqlalchemy.orm import Session
from . import model, schemas
from . import utils
from . database import engine, get_db

model.Base.metadata.create_all(bind=engine)

app = FastAPI()

@app.get("/posts", response_model=list[schemas.PostResponse])
def get_posts(db: Session = Depends(get_db)):
    posts = db.query(model.Post).all()
    return posts

@app.post("/posts", status_code=status.HTTP_201_CREATED, response_model=schemas.PostResponse)
def create_post(payload: schemas.PostCreate, db: Session = Depends(get_db)):
    new_post = model.Post(**payload.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post

@app.get("/posts/{id}", response_model=schemas.PostResponse)
def get_post(id: int, db: Session = Depends(get_db)):
    post = db.query(model.Post).filter(model.Post.id == id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id {id} not found")
    return post

@app.delete("/posts/{id}", status_code=status.HTTP_200_OK)
def delete_post(id: int, db: Session = Depends(get_db)):
    post = db.query(model.Post).filter(model.Post.id == id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id {id} not found")
    db.delete(post)
    db.commit()
    return {"detail": "Post deleted successfully"}
   
@app.put("/posts/{id}", response_model=schemas.PostResponse)
def update_post(id: int, payload: schemas.PostCreate, db: Session = Depends(get_db)):
    post_query = db.query(model.Post).filter(model.Post.id == id)
    post = post_query.first()
    
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id {id} not found")
    
    post_query.update(payload.dict(), synchronize_session=False)
    db.commit()
    
    return post_query.first()

@app.post("/users", status_code=status.HTTP_201_CREATED, response_model=schemas.UserResponse)
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