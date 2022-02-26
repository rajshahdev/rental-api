from jose import JWTError, jwt
from . import schemas
from fastapi import FastAPI, Response, status, HTTPException, Depends
from datetime import datetime, timedelta
from fastapi.security import OAuth2PasswordBearer
from .database import get_db
from sqlalchemy.orm import Session
from . import models
from dotenv import load_dotenv
import os
load_dotenv()

# secret key
# algorithm
# expiration time


SECRET_KEY = os.getenv('SECRET_KEY')
ALGORITHM = os.getenv('ALGORITHM')
ACCESS_TOKEN_EXPIRE_MINUTES = os.getenv('ACCESS_TOKEN_EXPIRE_MINUTES')
oauth2scheme = OAuth2PasswordBearer(tokenUrl='login')


def create_access_token(data: dict):
    to_encode = data.copy()

    expires = datetime.utcnow() + timedelta(minutes=int(ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expires})

    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, ALGORITHM)

    return encoded_jwt


def verify_access_token(token: str, credentials_exception):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        id: str = payload.get('user_id')
        if id is None:
            raise credentials_exception

        token_data = schemas.Tokendata(id=id)
    except JWTError:
        raise credentials_exception

    return token_data


def get_current_user(token: str = Depends(oauth2scheme), db: Session = Depends(get_db)):
    credentials_exception = HTTPException(

        status_code=status.HTTP_401_UNAUTHORIZED,
        detail=f"could not validate credentials",
        headers={'WWW-Authorization': 'Bearer'}

    )

    token = verify_access_token(token, credentials_exception)

    # remember the below statement gives all the information --> if we return user
    # user = db.query(models.User).filter(models.User.id == token.id).first()

    return token