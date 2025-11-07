from fastapi import FastAPI, status, HTTPException, Depends
from pydantic import BaseModel
from datetime import datetime as DateTime
from sqlalchemy.orm import Session
#importing local modules
from app.database.postsdb import my_posts
from app.models.Post import Post

#the connection is established when the module is imported add remove and upadate using the cursor
from app.database.pgdb import cursor, conn




#working with python classes as sql importing the model and database
from app.database.database import engine, get_db
from app.models import model

model.Base.metadata.create_all(bind = engine)


app = FastAPI()



#just for testing purpose
@app.get("/sqlalchemy")
def test_one(db: Session = Depends(get_db)):
    posts = db.query(model.Post).all()
    return {"Status" : posts}



@app.get("/posts")
async def posts(db: Session = Depends(get_db)):

    #working when no class for sql I mean without sqlalchemy
    # cursor.execute("""SELECT * FROM posts""")
    # posts = cursor.fetchall()

    #with sqlalchemy model
    posts = db.query(model.Post).all()
    return {"data" : posts}


@app.post("/posts", status_code= status.HTTP_201_CREATED)
async def posts(post: Post, db: Session = Depends(get_db)):
    # cursor.execute("""INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING *""",
    #                (post.title, post.content, post.published))
    # new_post = cursor.fetchone()
    # conn.commit()


    new_post = model.Post(title = post.title, content = post.content, published = post.published)
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return {"message": new_post}


#one post with a specific id
@app.get("/posts/{id}")
async def get_post(id: int):
    cursor.execute("""SELECT * FROM posts WHERE id = %s""", (str(id),))
    post = cursor.fetchone()
    print(post)
    if post:
        return {"post_detail": post}
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                        detail=f"Post with id {id} not found")



@app.delete("/posts/{id}", status_code = status.HTTP_204_NO_CONTENT)
async def delete_post(id: int):
    cursor.execute("""DELETE FROM posts WHERE id = %s RETURNING *""", (str(id),))
    deleted_post = cursor.fetchone()
    conn.commit()

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                        detail=f"Post with id {id} not found")




@app.put("/posts/{id}")
async def update_post(id: int, post: Post):

    cursor.execute(""" UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s RETURNING *""",
                   (post.title, post.content, post.published, str(id)))
    
    updated_post = cursor.fetchone()
    conn.commit()

    if updated_post:
        return {"message": "Post updated successfully", "post": updated_post}       
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                        detail=f"Post with id {id} not found")
