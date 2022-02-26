from pydantic import BaseModel, validator, ValidationError, Field
from datetime import datetime
from datetime import date
from typing import Optional, Text, List

from pydantic.networks import EmailStr
from pydantic.types import constr, conint


class UserBase(BaseModel):
    name: constr(min_length=1)
    email: EmailStr
    phone: constr(min_length=10, max_length=10)


class UserOut(BaseModel):
    id: int
    name: constr(min_length=1)
    email: EmailStr
    phone: constr(min_length=10, max_length=10)
    created_at: date
    status: bool

    class Config:
        orm_mode = True


class UserOutSchema(BaseModel):
    status: bool
    data: UserOut
    message: str


class ListUser(BaseModel):
    status: bool
    data: List[UserOut]
    message: str


class VehicleAdd(BaseModel):
    vehicle_type: str
    total: int

    class Config:
        orm_mode = True


class VehicleOut(BaseModel):
    status: bool
    data: VehicleAdd
    message: str


class RentVehicle(BaseModel):
    user_id: int
    inv_id: int
    rental_date: date
    return_date: date
