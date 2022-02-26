from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter, UploadFile, File
from sqlalchemy.orm.session import Session
from . import models
from . import schemas
from typing import Optional, List
from .database import get_db
from . import oauth2

router = APIRouter(
    prefix="/rent",
    tags=['rent']
)


@router.post('/')
def rent_vehicle(newrent: schemas.RentVehicle, db: Session = Depends(get_db),
                 emp_id: int = Depends(oauth2.get_current_user)):
    usernotfound = db.query(models.User).filter(newrent.user_id == models.User.id)
    vehiclenotfound = db.query(models.Inventory).filter(newrent.inv_id == models.Inventory.id)

    if usernotfound.first() is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="no such user found")
    if vehiclenotfound.first() is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="no such vehicle in our inventory")

    if newrent.return_date < newrent.rental_date:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="date must be greater then current date")

    if vehiclenotfound.first().remaining == 0:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="this vehicle is out of stock.")
    usernotfound.update({'status': True}, synchronize_session=False)
    db.commit()

    updated_total = vehiclenotfound.first().remaining - 1
    if vehiclenotfound.first().allocated is None:
        updated_allocated = 1
    else:
        updated_allocated = vehiclenotfound.first().allocated + 1
    vehiclenotfound.update({'remaining': updated_total, 'allocated': updated_allocated}, synchronize_session=False)
    rent_new = models.Rent(**newrent.dict())

    db.add(rent_new)
    db.commit()
    db.refresh(rent_new)

    return {"status": True, "data": rent_new, "message": "vehicle added successfully"}


@router.get('getdetail/', response_model=schemas.GetRentDetail)
def get_rent_detail(db: Session = Depends(get_db), emp_id: int = Depends(oauth2.get_current_user)):
    get_detail = db.query(models.Rent).all()
    return {"status": True, "data": get_detail, "message": "detail fetched successfully"}
