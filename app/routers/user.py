from fastapi import status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session

from .. import models, schemas, utils
from ..database import get_db
from ..oauth2 import get_current_user


router = APIRouter(
    prefix="/users",
    tags=["Users"]
)


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.UserOut)
async def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    _user = db.query(models.User).filter(models.User.email == user.email).first()
    if _user:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                            detail=f"could not create a user")
    hashed_password = utils.hash(user.password)
    user.password = hashed_password
    new_user = models.User(**user.model_dump())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user


@router.get("/", status_code=status.HTTP_200_OK, response_model=schemas.UserOut)
async def get_current_user(current_user: models.User = Depends(get_current_user)):

    # if not current_user:
    #     raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
    #                         detail=f"user with id={id} does not exist")
    
    return current_user


@router.get("/{id}", status_code=status.HTTP_200_OK, response_model=schemas.UserOut)
async def get_user_by_id(id: int, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    user = db.query(models.User).filter(models.User.id == id).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"user with id={id} does not exist")
    
    return user
