from sqlalchemy import select
from sqlalchemy.orm import Session
from app.data.tables import TABLES, engine_creator


class DataManager():
    def __init__(self):
        self.engine = engine_creator()

    def get_json(self, tablename):
        try:
            table = TABLES[tablename]
        except:
            return "incorrect table name"

        dictionary = {}
        with Session(self.engine) as session:
            for item in session.query(table).all():
                dictionary[item.__dict__["id"]] = item.__dict__
        return dictionary

    def get_rental(self, id):
        with Session(self.engine) as session:
            rental = session.execute(select(TABLES["rentals"]).where(User.id == id)).scalar_one()
        return rental

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


