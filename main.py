from typing import Optional
from random import randrange
from fastapi import FastAPI
from fastapi.params import Body
from pydantic import BaseModel
from fastapi import Response, status, HTTPException
import psycopg2
from psycopg2.extras import RealDictCursor
import time


app = FastAPI()




class Post(BaseModel):
    title: str
    content: str
    published: bool = True


while True:

    try:
        conn = psycopg2.connect(host='localhost', database='FastAPI', user='postgres', password='12345678',
                                cursor_factory=RealDictCursor)
        cursor = conn.cursor()
        print("Database connection was "
              "successful!")
        break
    except Exception as error:
        print("Connection to database failed")
        print("Error: ", error)
        time.sleep(2)


@app.get("/")
async def welcome_note():
    return {"message": "Hello Tendayi, Welcome to FASTAPI - The best site to host your APIs'"}


@app.get("/posts")
def get_posts():
    cursor.execute("""SELECT * FROM posts""")
    posts = cursor.fetchall()
    print(posts)
    return {"data": posts}


@app.post("/createposts", status_code=status.HTTP_201_CREATED)
async def create_new_posts(new_post: Post):
    cursor.execute("""INSERT INTO posts
    (title, content, published)
    VALUES
    (%s, %s, %s) RETURNING * """,(new_post.title, new_post.content, new_post.published))
    new_post = cursor.fetchone()
    conn.commit()
    return {"data": new_post}


@app.get("/posts/{id}")
async def get_post(id: int, response: Response):
    cursor.execute("""SELECT * FROM posts WHERE id = %s """, (str(id)))
    post = cursor.fetchone()
    print(post)
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} was not found")
        # response.status_code = status.HTTP_404_NOT_FOUND
        # return {'message': f"post with id: {id} was not found"}
    return {"post details": post}


@app.delete("/deletepost/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_post(id: int):
    cursor.execute(""" DELETE FROM posts WHERE id = %s RETURNING *""", (str(id)))
    deleted_post = cursor.fetchone()
    conn.commit()
    if deleted_post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'post with id: {id} does not exist')

    return Response(status_code=status.HTTP_204_NO_CONTENT)


@app.put("/updatepost/{id}", status_code=status.HTTP_201_CREATED)
async def update_post(id: int, new_post: Post):
    cursor.execute(""" UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s RETURNING *""", (new_post.title, new_post.content, new_post.published, str(id)))
    updated_post = cursor.fetchone()
    conn.commit()

    if updated_post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'post with id: {id} does not exist')

    return {'data': updated_post}
