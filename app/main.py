from typing import Optional
from random import randrange
from fastapi import FastAPI
from fastapi.params import Body
from pydantic import BaseModel
from fastapi import Response, status, HTTPException

app = FastAPI()


class Post(BaseModel):
    title: str
    content: str
    published: bool = True
    rating: Optional[int] = None


my_posts = [{"title": "title of post 1", "content": "content of post 1", "id": 1},
            {"title": "favorite food", "content": "I like pizza", "id": 2}]


def find_post(id):
    for p in my_posts:
        if p["id"] == id:
            return p


def find_index_post(id):
    for i, p in enumerate(my_posts):
        if p['id'] == id:
            return i


@app.get("/")
async def welcome_note():
    return {"message": "Hello Tendayi, Welcome to FASTAPI - The best site to host your APIs'"}


@app.get("/posts")
def get_posts():
    return {"data": my_posts}


@app.post("/createposts", status_code=status.HTTP_201_CREATED)
async def create_new_posts(new_post: Post):
    print(new_post)
    print(new_post.dict())
    new_post_dict = new_post.dict()
    new_post_dict['id'] = randrange(0, 100000)

    my_posts.append(new_post_dict)
    return {"": new_post_dict}


@app.get("/posts/{id}")
async def get_post(id: int, response: Response):
    post = find_post(int(id))
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} was not found")
        # response.status_code = status.HTTP_404_NOT_FOUND
        # return {'message': f"post with id: {id} was not found"}
    return {"post details": post}


@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_post(id: int):
    index = find_index_post(id)
    if index is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'post with id: {id} does not exist')
    my_posts.pop(index)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@app.put("/posts/{id}", status_code=status.HTTP_201_CREATED)
async def update_post(id: int, post: Post):
    index = find_index_post(id)
    if index is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'post with id: {id} does not exist')
    post_dict = post.dict()
    post_dict['id'] = id
    my_posts[index] = post_dict
    return {'data': post_dict}
