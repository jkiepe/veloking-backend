from sqlalchemy.orm import Session
from sqlalchemy import select
from passlib.context import CryptContext

from app import tables, schemas

crypt = CryptContext(schemes=["bcrypt"], deprecated="auto")


# USER
def user_create(user: schemas.UserSchema, database: Session):
    user.password = crypt.hash(user.password)
    new_user = tables.User(**user.dict(), rental_point_id=1)
    database.add(new_user)
    database.commit()


def user_get_all(database: Session):
    return database.query(tables.User)


def user_get_by_username(username: str, database: Session):
    return database.query(tables.User).filter(tables.User.username == username).first()


def user_check_credentials(user: tables.User, password: str, database: Session):
    return crypt.verify(user.password, password)


def user_move_to_point(user: tables.User, point: tables.Point, database: Session):
    user.current_rental_id = point.id
    database.add(user)
    database.commit()
    

# POINT
def point_create(point: schemas.PointSchema, database: Session):
    new_point = tables.Point(**point.dict())
    database.add(new_point)
    database.commit()

def point_get_by_key(key: str, database: Session):
    return database.query(tables.Point).filter(tables.Point.key == key).first()
