from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional

app = FastAPI()

# Mock data for posts
class Post(BaseModel):
    title: str
    content: str
    author: str

posts = []

@app.post("/posts/", response_model=Post)
def create_post(post: Post):
    posts.append(post)
    return post

@app.get("/posts/", response_model=List[Post])
def read_posts(skip: int = 0, limit: int = 10):
    return posts[skip : skip + limit]

@app.get("/posts/{post_id}", response_model=Post)
def read_post(post_id: int):
    if post_id < 0 or post_id >= len(posts):
        raise HTTPException(status_code=404, detail="Post not found")
    return posts[post_id]

@app.delete("/posts/{post_id}", response_model=Post)
def delete_post(post_id: int):
    if post_id < 0 or post_id >= len(posts):
        raise HTTPException(status_code=404, detail="Post not found")
    deleted_post = posts.pop(post_id)
    return deleted_post
