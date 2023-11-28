import math
import pandas
from pydantic import BaseModel
from fastapi import FastAPI
from datetime import datetime, timedelta


class Rental(BaseModel):
    equipment: list
    forward_payment: float
    start_time: datetime
    end_time: datetime


def calculate_duration(start, end):
    half_hours = (end - start).total_seconds()/1800
    return math.ceil(half_hours)


def get_equipment(vehicles):
    vehicle_ids = [vehicle["vehicleid"].split("-")[0] for vehicle in vehicles]
    return vehicle_ids


def get_prices(items, half_hours):
    price_list = pandas.read_json('price.json')
    hours = half_hours/2
    price = 0

    for item in items:
        equipment_type = price_list[item]["type"]
        prices = price_list[item]
        hours_down = math.floor(hours)
        hours_up = math.ceil(hours)

        if equipment_type == "gokart":
            price += prices["hour"] * hours_down
            if half_hours % 2 == 1:
                price += prices["half_hour"]

        if equipment_type == "bike":
            max_hours = len(prices["hours"])

            # checking days
            if hours >= 24:
                days = math.floor(hours/24)
                hours -= 24 * days
                price += prices["days"][days - 1]
            elif hours > 16 and hours < 24:
                price += prices["days"][0]

            # checking hours|whole day
            if hours > max_hours < 16:
                price += prices["day"]
            elif hours < max_hours:
                price += prices["hours"][hours_up - 1]
    return price


app = FastAPI()


@app.post('/calc/price')
async def price_calc(rental: Rental):
    duration = calculate_duration(start=rental.start_time, end=rental.end_time)
    equipment = get_equipment(rental.equipment)
    price = get_prices(equipment, duration)
    total_price = price - rental.forward_payment
    return total_price


