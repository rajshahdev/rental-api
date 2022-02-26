from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter, UploadFile, File
from sqlalchemy.orm.session import Session
from . import models
from . import schemas
from typing import Optional, List
from .database import get_db

router = APIRouter(
    prefix="/rent",
    tags=['Rent']
)


@router.post('/')
def rent_vehicle(newrent: schemas.RentVehicle, db: Session = Depends(get_db)):
    usernotfound = db.query(models.User).filter(newrent.user_id == models.User.id)
    vehiclenotfound = db.query(models.Inventory).filter(newrent.inv_id == models.Inventory.id)

    if usernotfound.first() is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="no such user found")
    if vehiclenotfound.first() is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="no such vehicle in our inventory")

    usernotfound.update({'status':True},synchronize_session=False)
    db.commit()

    updated_total = vehiclenotfound.first().total - 1
    if vehiclenotfound.first().allocated is None:
        updated_allocated = 1
    else:
        updated_allocated = vehiclenotfound.first().allocated + 1
    vehiclenotfound.update({'total':updated_total,'allocated':updated_allocated},synchronize_session=False)
    rent_new = models.Rent(**newrent.dict())

    db.add(rent_new)
    db.commit()
    db.refresh(rent_new)

    return {"status": True, "data": rent_new, "message": "vehicle added successfully"}