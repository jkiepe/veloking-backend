from sqlalchemy import select
from sqlalchemy.orm import Session
from tables import Price, RentalPoint, Vehicle, User
from tables import DefectVehicle, Rental, Staff, TurnOver
from tables import engine_creator

TABLES = [Price, RentalPoint, Vehicle, User, DefectVehicle, Rental, Staff, TurnOver]


class DataManager():
    def __init__(self):
        self.engine = engine_creator()

    def get_json(self, tablename):
        tablenames = [table.__tablename__ for table in TABLES]
        if tablename in tablenames:
            for table in TABLES:
                if table.__tablename__ == tablename:
                    chosen_table = table
        else:
            return "wrong table name"

        dictionary = {}
        with Session(self.engine) as session:
            for item in session.query(chosen_table).all():
                dictionary[item.__dict__["id"]] = item.__dict__
        return dictionary

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


