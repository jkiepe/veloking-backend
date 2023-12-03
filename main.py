import sys
sys.path.append("database")

from datamanager import DataManager
from fastapi import FastAPI
from pricecalculator import Rental, PriceCalculator

app = FastAPI()
data_manager = DataManager()


@app.get("/data/{tablename}")
async def send_data(tablename: str):
    json = data_manager.get_json(tablename)
    return json


# @app.post('/calc/price')
# async def price_calc(rental: Rental):
#     price_calculator = PriceCalculator(rental)
#     return price_calculator.total_price

