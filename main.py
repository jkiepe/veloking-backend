from fastapi import FastAPI
from price_calculator import Rental, PriceCalculator

app = FastAPI()


@app.get("/data/{data_name}")
async def send_data(data_name: str):
    return "Work in progress."


# @app.post('/calc/price')
# async def price_calc(rental: Rental):
#     price_calculator = PriceCalculator(rental)
#     return price_calculator.total_price

