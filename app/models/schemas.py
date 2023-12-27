from pydantic import BaseModel
from typing import Optional


class LoginSchema(BaseModel):
    username: str
    password: str

    class Config:
        json_schema_extra = {
            "example": {
                "username": "admin",
                "password": "admin",
            }
        }


class VehicleSchema(BaseModel):
    rented: bool = False
    superior_category: str
    sub_category: str
    tag: str


class UserSchema(BaseModel):
    username: str
    password: str
    fullname: str
    disabled: bool = True
    role: str

    class Config:
        from_attributes = True


class PointSchema(BaseModel):
    key: str
    name: str
    users: list[UserSchema] = []
    vehicles: list[VehicleSchema] = []

    class Config:
        from_attributes = True


class PriceSchema(BaseModel):
    category: str | list
    day: int
    first_hour: Optional[int] = None
    half_hour: Optional[int] = None
    hour: int
    per_24_hours: int

    class Config:
        from_attributes = True


class PrepaymentSchema(BaseModel):
    tags: list
    day: Optional[bool]
    first_hour: Optional[bool]
    half_hour: Optional[bool]
    hour: Optional[int]
    per_24_hours: Optional[int]

    class Config:
        from_attributes = True

