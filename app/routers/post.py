from typing import List, Optional
from fastapi import status, HTTPException, Depends, APIRouter, Response
from sqlalchemy import func
from sqlalchemy.orm import Session

from .. import models, schemas
from ..database import get_db
from ..oauth2 import get_current_user


router = APIRouter(
    prefix="/posts",
    tags=["Posts"]
)


@router.get("/", response_model=List[schemas.PostOut])
# @router.get("/")
async def get_posts(db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user), 
                    limit: int = 10, skip: int = 0, search: Optional[str] = ""):
    # cursor.execute("""SELECT * FROM posts;""")
    # posts = cursor.fetchall()
    # posts = db.query(models.Post).filter(models.Post.owner_id == current_user.id).all()
    results = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(models.Vote, 
                                         models.Post.id == models.Vote.post_id, 
                                         isouter=True).group_by(models.Post.id)\
                                            .filter(models.Post.title.contains(search))\
                                                .limit(limit)\
                                                    .offset(skip)\
                                                        .all()
    return results
    # posts = db.query(models.Post).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()
    # return posts


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
async def create_post(post: schemas.PostCreate, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    # cursor.execute("""INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING *""", 
    #                (post.title, post.content, post.published))
    # new_post = cursor.fetchone()
    # conn.commit()
    new_post = models.Post(owner_id=current_user.id, **post.model_dump())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post


@router.get("/{id}", response_model=schemas.PostOut)
async def get_post(id: int, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    # cursor.execute("""SELECT * FROM posts WHERE id = %s""", (str(id), ))
    # post = cursor.fetchone()
    # post = db.query(models.Post).filter(models.Post.id == id).first()
    post = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(models.Vote, 
                                         models.Post.id == models.Vote.post_id, 
                                         isouter=True).group_by(models.Post.id)\
                                            .filter(models.Post.id == id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f"post with id={id} was not found")
    # if post.owner_id != current_user.id:
    #     raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
    #                         detail=f"you are not authorized to get this post")
    return post


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_post(id: int, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    # cursor.execute("""DELETE FROM posts WHERE id = %s RETURNING *""", (str(id), ))
    # post = cursor.fetchone()
    # conn.commit()
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()

    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id={id} was not found")
    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail=f"you are not allowed to delete this post")
    
    post_query.delete(synchronize_session=False)
    db.commit()
    # can be commented out as well
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.put("/{id}", response_model=schemas.Post)
async def update_post(id: int, post: schemas.PostCreate, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    # cursor.execute("""UPDATE posts SET title=%s, content=%s, published=%s WHERE id = %s RETURNING *""",
    #                (post.title, post.content, post.published, str(id)))
    # post = cursor.fetchone()
    # conn.commit()
    post_query = db.query(models.Post).filter(models.Post.id == id)
    updated_post = post_query.first()
    if not updated_post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id={id} was not found")
    if updated_post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail=f"you are not allowed to update this post")
    
    post_query.update(post.model_dump(), synchronize_session=False)
    db.commit()

    return post_query.first()
