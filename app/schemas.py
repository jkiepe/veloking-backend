from pydantic import BaseModel


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


class RentalSchema(BaseModel):
    current: int
    days: int
    hours: str
    interval: int
    liability: float
    rented: bool
    start_time: str

    class Config:
        from_attributes = True


class UserSchema(BaseModel):
    username: str
    password: str
    fullname: str
    role: str
    
    rentals: list[RentalSchema] = []

    class Config:
        from_attributes = True

        json_schema_extra = {
            "example": {
                "username": "admin",
                "fullname": "adminadmin",
                "password": "admin",
                "role": "admin",
            }
        }


class PointSchema(BaseModel):
    key: str
    name: str
    users: list[UserSchema] = []
    rentals: list[RentalSchema] = []

    class Config:
        from_attributes = True

        json_schema_extra = {
            "example": {
                "key": "baza",
                "name": "Baza",
                }
            }
