from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter, UploadFile, File
from sqlalchemy.orm.session import Session
from . import models
from . import schemas
from . import oauth2
from .database import get_db

router = APIRouter(
    prefix="/inventory",
    tags=['inventory']
)


@router.post('create/', response_model=schemas.VehicleOut)
def add_vehicle(vehicle: schemas.VehicleAdd, db: Session = Depends(get_db),
                emp_id: int = Depends(oauth2.get_current_user)):
    if db.query(models.Inventory).filter(models.Inventory.vehicle_type == vehicle.vehicle_type).first() is not None:
        if vehicle.vehicle_type == db.query(models.Inventory).filter(
                models.Inventory.vehicle_type == vehicle.vehicle_type).first().vehicle_type:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="vehicle already exists")
    new_vehicle = models.Inventory(**vehicle.dict())
    db.add(new_vehicle)
    db.commit()
    db.refresh(new_vehicle)

    return {"status": True, "data": new_vehicle, "message": "vehicle added successfully"}


@router.get('vehicles/')
def get_vehicle_details(db: Session = Depends(get_db), emp_id: int = Depends(oauth2.get_current_user)):
    get_all_vehicles = db.query(models.Inventory).all()

    return {"status": True, "data": get_all_vehicles, "message": "vehicle added successfully"}
