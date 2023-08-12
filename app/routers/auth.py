from fastapi import APIRouter, Depends, status, HTTPException
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from ..models import User
from ..schemas import UserOut, UserCreate, Token
from ..database import get_db
from ..utils import verify, hash
from ..oauth2 import create_access_token


router = APIRouter(
    tags=["Authentication"]
)


@router.post("/login", response_model=Token)
async def login(user_credentials: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == user_credentials.username).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail=f"Invalid Credentials")
    if not verify(user_credentials.password, user.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail=f"Invalid Credentials")
    
    # generate JWT token
    access_token = create_access_token(data={"user_id": user.id})
    return {"access_token": access_token, "token_type": "bearer"}


@router.post("/signup", status_code=status.HTTP_201_CREATED, response_model=UserOut)
async def signup(user: UserCreate, db: Session = Depends(get_db)):
    _user = db.query(User).filter(User.email == user.email).first()
    if _user:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                            detail=f"could not create a user")
    
    hashed_password = hash(user.password)
    user.password = hashed_password
    new_user = User(**user.model_dump())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user
