from fastapi import FastAPI, status, HTTPException, Depends
from pydantic import BaseModel
from datetime import datetime as DateTime
from sqlalchemy.orm import Session
#importing local modules
#from app.database.postsdb import my_posts
from app.models.Post import Post

#the connection is established when the module is imported add remove and upadate using the cursor
# from app.database.pgdb import cursor, conn




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


    #dict() changes to model_dump()
    new_post = model.Post(**post.model_dump())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return {"message": new_post}


#one post with a specific id
@app.get("/posts/{id}")
async def get_post(id: int, db: Session = Depends(get_db)):

    #through sql query
    # cursor.execute("""SELECT * FROM posts WHERE id = %s""", (str(id),))
    # post = cursor.fetchone()
    # print(post)

    #through orm
    #it works but we can use the filter as well
    #post = db.query(model.Post).get(id)
    post = db.query(model.Post).filter(model.Post.id == id).first()
    if post:
        return {"post_detail": post}
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                        detail=f"Post with id {id} not found")



@app.delete("/posts/{id}", status_code = status.HTTP_204_NO_CONTENT)
async def delete_post(id: int, db: Session = Depends(get_db)):
    
    # cursor.execute("""DELETE FROM posts WHERE id = %s RETURNING *""", (str(id),))
    # deleted_post = cursor.fetchone()
    # conn.commit()


    #done through the pydantic and sqlalchemy class
    post = db.query(model.Post).filter(model.Post.id == id)
    print(post)
    print(post.first())
    if post.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                        detail=f"Post with id {id} not found")

    post.delete(synchronize_session=False)



@app.put("/posts/{id}")
async def update_post(id: int, post: Post, db : Session = Depends(get_db)):

    post_filter = db.query(model.Post).filter(model.Post.id == id)
    post = post_filter.first()

    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post for update is not found at {id}" )
    

    post_filter.update({"title" : "Title Updated", "content" : "Content Updated"}, synchronize_session=False)
    db.commit() 
    return {"message": "Post updated successfully", "post": post_filter}  
     


    # cursor.execute(""" UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s RETURNING *""",
    #                (post.title, post.content, post.published, str(id)))
    # updated_post = cursor.fetchone()
    # conn.commit()
    # if post_filter:
    #     return {"message": "Post updated successfully", "post": post_filter}       
    # else:
    #     raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
    #                     detail=f"Post with id {id} not found")
