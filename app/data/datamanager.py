from sqlalchemy import select
from sqlalchemy.orm import Session
from passlib.context import CryptContext

from app.data.tables import Price, RentalPoint, Vehicle, User, DefectVehicle
from app.data.tables import Rental, Staff, TurnOver

URI = "postgresql://jonasz@localhost:5432/veloking"

TABLES = {
    "prices": Price,
    "rentalpoints": RentalPoint,
    "vehicles": Vehicle,
    "users": User,
    "defectvehicles": DefectVehicle,
    "rentals": Rental,
    "staff": Staff,
    "turnover": TurnOver,
}

password_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def engine_creator(want_echo=False):
    engine = create_engine(URI, echo=want_echo)
    return engine


class DataManager():
    def __init__(self):
        self.engine = engine_creator()

    def add_data(self, data):
        with Session(self.engine) as session:
            session.add(data)
            session.commit()

    def get_data(self, tablename):
        try:
            table = TABLES[tablename]
        except:
            return "incorrect table name"

        dictionary = {}
        with Session(self.engine) as session:
            for item in session.query(table).all():
                dictionary[item.__dict__["id"]] = item.__dict__
        return dictionary

    def check_credentials(self, data):
        users: UserSchema = self.get_data("users")
        for (number, user) in users.items():
            if user["email"] == data.email:
                matching = password_context.verify(data.password, user["password"])
                return matching
        return True

    def add_user(self, user):
        user["password"] = password_context.hash(user["password"])
        new_user = User(**user)
        self.add_data(new_user)

    def add_rental(self, rental):
        return rental
        

# def get_rental(self, id: int):
#     with Session(self.engine) as session:
#         rental = session.execute(select(TABLES["rentals"]).where(User.id == id)).scalar_one()
#     return rental

# with Session(engine) as session:
#     squidward = session.execute(select(User).filter_by(name="squidward")).scalar_one()
#     squidward.fullname = "Very mad"
#     squidward_fullname = session.execute(select(User.fullname).where(User.id == 1)).scalar_one()

# with Session(engine) as session:
#     baza = session.execute(select(RentalPoint).filter_by(key="baza")).scalar_one()
#     session.delete(baza)
#     session.commit()
    # baza = session.execute(select(RentalPoint).filter_by(key="baza")).scalar_one()
    # print(baza.name)


