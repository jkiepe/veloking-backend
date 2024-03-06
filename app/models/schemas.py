from pydantic import BaseModel
from typing import Optional


class LoginSchema(BaseModel):
    email: str
    password: str

    class Config:
        json_schema_extra = {
            "example": {
                "email": "admin@gmail.com",
                "password": "admin",
            }
        }


class VehicleSchema(BaseModel):
    rented: bool = False
    superior_category: str
    sub_category: str
    vehicle_key: str


class UserSchema(BaseModel):
    username: str
    email: str
    password: str
    fullname: str
    disabled: bool = True
    role: str

    class Config:
        from_attributes = True


class PointSchema(BaseModel):
    point_key: str
    name: str
    users: list[UserSchema] = []
    vehicles: list[VehicleSchema] = []

    class Config:
        from_attributes = True


class PriceSchema(BaseModel):
    superior_category: str | list
    day: int
    first_hour: Optional[int] = None
    half_hour: Optional[int] = None
    hour: int
    per_24_hours: int

    class Config:
        from_attributes = True


class PrepaymentSchema(BaseModel):
    vehicle_keys: list
    day: Optional[bool]
    first_hour: Optional[bool]
    half_hour: Optional[bool]
    hour: Optional[int]
    per_24_hours: Optional[int]

    class Config:
        from_attributes = True

