from fastapi import APIRouter, Depends, status, Response, HTTPException
from .database import get_db
from sqlalchemy.orm.session import Session
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from . import schemas
from . import models
from . import oauth2
from .utils import verify_password

router = APIRouter(
    tags=['Authentication'],
)


@router.post('/login')
def login(user_credentials: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):

    user = db.query(models.Emp).filter(models.Emp.email == user_credentials.username).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Invalid username or password")

    if not verify_password(user_credentials.password, user.password):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"the password is wrong")

    # create token
    access_token = oauth2.create_access_token(data={"emp_id": user.id})
    return {"access_token": access_token, "token_type": "bearer"}