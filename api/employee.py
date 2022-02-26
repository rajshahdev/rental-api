from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter, UploadFile, File
from sqlalchemy.orm.session import Session
from . import models
from . import schemas
from typing import Optional, List
from .utils import hash
from .database import get_db
router = APIRouter(
    prefix="/emp",
    tags=['employee']
)


@router.post('create/', response_model=schemas.EmpOutSchema)
def employee_create(emp: schemas.EmpBase, db: Session = Depends(get_db)):
    # print(db.query(models.User).filter(models.User.username == users.username).first().username)
    if db.query(models.Emp).filter(models.Emp.email == emp.email).first() is not None:
        if emp.email == db.query(models.Emp).filter(models.Emp.email == emp.email).first().email:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="email already exist")

    emp.password = hash(emp.password)
    new_user = models.Emp(**emp.dict())

    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return {"status": True, "data": new_user, "message": "User Created Successfully"}

