from fastapi import FastAPI
from . import model
from . database import engine, get_db
from .routers import post, user

model.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(post.router)
app.include_router(user.router)



