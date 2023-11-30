from price_calculator import Rental, PriceCalculator
from data_manager import read_data
from fastapi import FastAPI

app = FastAPI()


@app.get("/data/{data_name}")
async def send_data(data_name: str):
    json_data = read_data(data_name)
    return json_data


@app.post('/calc/price')
async def price_calc(rental: Rental):
    price_calculator = PriceCalculator(rental)
    return price_calculator.total_price
