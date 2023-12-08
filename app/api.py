from fastapi import FastAPI, Body, Depends

from app.model import Rental, UserSchema, UserLoginSchema
from app.auth.auth_bearer import JWTBearer
from app.auth.auth_handler import signJWT
from app.pricecalculator import PriceCalculator
from app.data.datamanager import DataManager

app = FastAPI()
data_manager = DataManager()

users = []
# from passlib.context import CryptContext
# password_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
# matching = password_context.verify(plain_password, hashed_password)
# hashed_password = password_context.hash(password)


@app.get("/", tags=["root"])
async def read_root() -> dict:
    return {"message": "Welcome to veloking API"}


@app.get("/data/{tablename}", dependencies=[Depends(JWTBearer())], tags=["data"])
async def retrieve_data(tablename: str):
    data = data_manager.get_json(tablename)
    return data


@app.post("/user/signup", dependencies=[Depends(JWTBearer())], tags=["user"])
async def create_user(user: UserSchema = Body(...)):
    # data_manager.add_user
    users.append(user) # hash password using passlib
    return signJWT(user.email)


def check_user(data: UserLoginSchema):
    for user in users:
        if user.email == data.email and user.password == data.password:
            return True
    return False


@app.post("/user/login", tags=["user"])
async def user_login(user: UserLoginSchema = Body(...)):
    if check_user(user):
        return signJWT(user.email)
    return {
        "error": "Wrong login details!"
    }

# @app.post('/calculate/price', tags=["calculation"])
# async def calculate_price(rental: Rental):
#     price_calculator = PriceCalculator(rental)
#     return price_calculator.total_price

