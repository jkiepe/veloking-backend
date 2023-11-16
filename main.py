import pandas as pd
from pydantic import BaseModel
from fastapi import FastAPI
from datetime import datetime, timedelta


class Rental(BaseModel):
    equipment: list
    start_time: datetime
    end_time: datetime
    forward_payment: float


def calculate_duration(start, end):
    datetime.DeltaTime()


price_list = pd.read_json("price.json")


app = FastAPI()


@app.post('/calc/price')
async def price_calc(rental: Rental):
    return rental

