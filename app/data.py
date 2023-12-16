from sqlalchemy.orm import Session
from sqlalchemy import select
from passlib.context import CryptContext

from app import tables, schemas

crypt = CryptContext(schemes=["bcrypt"], deprecated="auto")


def add_user(user):
    user.password = self.crypt.hash(user.password)
    with Session(engine) as session:
        waiting_room = session.execute(select(tables.RentalPoint).where(RentalPoint.id == 1)).scalar_one()
        new_user = User(**user, current_rental_point=waiting_room)
        session.add(new_user)
        session.commit()


def user_create(user: schemas.UserSchema, database: Session):
    user.password = crypt.hash(user.password)
    new_user = tables.User(**user.dict(), rental_point_id=1)
    database.add(new_user)
    database.commit()


def user_get_username(username: str, database: Session):
    return database.query(tables.User).filter(tables.User.username == username).first()


def user_check_credentials(user: tables.User, password: str, database: Session):
    return crypt.verify(user.password, password)
