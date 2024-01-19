from sqlalchemy.orm import Session

from app.database import crypt
from app.models import schemas, tables


def user_verify(password, hash_password):
    return crypt.verify(password, hash_password)


def user_create(user: schemas.UserSchema, database: Session):
    if user.role == "admin":
        user.disabled = False
    user.password = crypt.hash(user.password)
    user = tables.User(**user.dict())
    database.add(user)
    database.commit()


def user_get_all(database: Session):
    return database.query(tables.User).all()


def user_get_by_username(username: str, database: Session):
    return database.query(tables.User).filter(tables.User.username == username).first()


def user_move_to_point(user: tables.User, point: tables.Point, database: Session):
    user.current_rental_id = point.id
    database.add(user)
    database.commit()


def price_create(price: tables.Price, database: Session):
    new_price = tables.Price(**price.dict())
    database.add(new_price)
    database.commit()


def point_create(point: schemas.PointSchema, database: Session):
    new_point = tables.Point(**point.dict())
    database.add(new_point)
    database.commit()


def point_get_all(database: Session):
    return database.query(tables.Point).all()


def point_get_by_key(point_key: str, database: Session):
    return (
        database.query(tables.Point).filter(tables.Point.point_key == point_key).first()
    )


def vehicle_create(vehicle: schemas.VehicleSchema, database: Session):
    office = (
        database.query(tables.Point).filter(tables.Point.point_key == "office").first()
    )
    new_vehicle = tables.Vehicle(**vehicle.dict(), rental_point=office)
    database.add(new_vehicle)
    database.commit()


def vehicle_get_by_key(vehicle_key: str, database: Session):
    return (
        database.query(tables.Vehicle)
        .filter(tables.Vehicle.vehicle_key == vehicle_key)
        .first()
    )


def vehicle_move(vehicle_key: str, point_key: str, database: Session):
    vehicle = vehicle_get_by_key(vehicle_key, database)
    point = point_get_by_key(point_key, database)
    vehicle.rental_point = point
    database.add(vehicle)
    database.commit()


def vehicle_get_all(database: Session):
    return database.query(tables.Vehicle).all()


# def rental_calculate_price(prepayment: schemas.PrepaymentSchema, database: Session):
#     price = 0
#     for tag in prepayment.tags:
#         superior_category = database.query(tables.Vehicle).filter(
#             tables.Vehicle.tag == tag).first().superior_category
#             price_list = database.query(tables.Price).filter(
#                     tables.Price.category == superior_category)
#         if superior_category == "bike":
#             price += prepayment.day * price_list.day
#             price += prepayment.half_hour * price_list.half_hour
#             price += prepayment.hour * price_list.hour
#             price += prepayment.per_24_hours * price_list.per_24_hours
#
#
