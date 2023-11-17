from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from ..models import model
from ..schemas import user
from ..db.config import get_db
from ..helpers import utils

router = APIRouter(
    prefix="/users",
    tags=['Users']
)


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=user.UserOut)
def create_user(user: user.UserCreate, db: Session = Depends(get_db)):

    #hash the paasword - user.password
    hashed_password = utils.hash(user.password)
    user.password = hashed_password

    new_user = model.User(**user.dict())
    # add post to our database
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user


@router.get("/{id}", response_model=user.UserOut)
def get_user(id: int, db: Session = Depends(get_db)):
    user = db.query(model.User).filter(model.User.id == id).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f"User with id: {id} does not exist")
    
    return user