from pydantic import BaseModel


class UserSchema(BaseModel):
    username: str
    password: str
    role: str

    class Config:
        orm_mode = True

        json_schema_extra = {
            "example": {
                "username": "admin",
                "password": "admin",
                "role": "admin",
            }
        }


class RentalPointSchema(BaseModel):
    key: str
    name: str
    users: list[UserSchema] = []

    class Config:
        orm_mode = True


class UserLoginSchema(BaseModel):
    username: str
    password: str

    class Config:
        json_schema_extra = {
            "example": {
                "username": "admin",
                "password": "admin",
            }
        }
