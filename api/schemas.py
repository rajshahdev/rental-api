from pydantic import BaseModel, validator, ValidationError, Field
from datetime import datetime
from datetime import date
from typing import Optional, Text, List

from pydantic.networks import EmailStr
from pydantic.types import constr, conint


class RentVehicle(BaseModel):
    user_id: int
    inv_id: int
    rental_date: date
    return_date: date


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
    remaining: int

    class Config:
        orm_mode = True


class VehicleOut(BaseModel):
    status: bool
    data: VehicleAdd
    message: str


class RentOutVehicle(BaseModel):
    id: int
    user_id: int
    inv_id: int
    rental_date: date
    return_date: date

    class Config:
        orm_mode = True


class GetRentDetail(BaseModel):
    status: bool
    data: List[RentOutVehicle]
    message: str


class EmpBase(UserBase):
    password: str


class EmpOut(BaseModel):
    id: int
    name: constr(min_length=1)
    email: EmailStr
    phone: constr(min_length=10, max_length=10)
    created_at: date

    class Config:
        orm_mode = True


class EmpOutSchema(BaseModel):
    status: bool
    data: EmpOut
    message: str


class Token(BaseModel):
    access_token: str
    token_type: str


class Tokendata(BaseModel):
    id: Optional[str] = None
