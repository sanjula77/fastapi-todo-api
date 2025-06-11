from fastapi import FastAPI, HTTPException

app = FastAPI()

@app.get("/posts")
def get_posts():
    return [
        {"id": 1, "title": "First Post", "content": "This is the content of the first post."},
        {"id": 2, "title": "Second Post", "content": "This is the content of the second post."}
    ]

@app.post("/createpost")
def create_post():
    return {"message": "Post created successfully", "status_code": 201}
    