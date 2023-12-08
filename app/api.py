from fastapi import FastAPI, Body, Depends

from app.model import Rental, UserSchema, UserLoginSchema
from app.auth.auth_bearer import JWTBearer
from app.auth.auth_handler import signJWT
from app.pricecalculator import PriceCalculator
from app.data.datamanager import DataManager

app = FastAPI()
data_manager = DataManager()

@app.get("/", tags=["root"])
async def read_root() -> dict:
    return {"message": "Welcome to veloking API"}


@app.post("/user/signup", dependencies=[Depends(JWTBearer())], tags=["user"])
async def create_user(user: UserSchema = Body(...)):
    data_manager.add_user(user.model_dump())
    return signJWT(user.email)


@app.post("/user/login", tags=["user"])
async def user_login(user: UserLoginSchema = Body(...)):
    if data_manager.check_credentials(user):
        return signJWT(user.email)
    return {
        "error": "Wrong login details!"
    }


@app.get("/data/{tablename}", dependencies=[Depends(JWTBearer())], tags=["data"])
async def retrieve_data(tablename: str):
    data = data_manager.get_data(tablename)
    return data


# @app.post('/calculate/price', tags=["calculation"])
# async def calculate_price(rental: Rental):
#     price_calculator = PriceCalculator(rental)
#     return price_calculator.total_price

