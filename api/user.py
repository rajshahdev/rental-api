from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter, UploadFile, File
from sqlalchemy.orm.session import Session
from . import models
from . import schemas
from typing import Optional, List
from .database import get_db
router = APIRouter(
    prefix="/users",
    tags=['users']
)


@router.post('create/', response_model=schemas.UserOutSchema)
def user_create(users:schemas.UserBase, db:Session = Depends(get_db)):
    if db.query(models.User).filter(models.User.email == users.email).first() is not None:
        if users.email == db.query(models.User).filter(models.User.email == users.email).first().email:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="email already exist")

    new_user = models.User(**users.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return {"status": True, "data": new_user, "message": "User Created Successfully"}


@router.get('/',response_model=schemas.ListUser)
def get_users(db:Session = Depends(get_db)):
    list_users = db.query(models.User).all()

    return {"status": True, "data": list_users, "message": "User Created Successfully"}



