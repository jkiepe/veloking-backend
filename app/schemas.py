from pydantic import BaseModel


class UserSchema(BaseModel):
    username: str
    password: str
    role: str

    class Config:
        from_attributes = True

        json_schema_extra = {
            "example": {
                "username": "admin",
                "password": "admin",
                "role": "admin",
            }
        }


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


class PointSchema(BaseModel):
    key: str
    name: str
    users: list[UserSchema] = []

    class Config:
        from_attributes = True

        json_schema_extra = {
            "example": {
                "key": "baza",
                "name": "Baza",
                }
            }
