from sqlalchemy import select
from sqlalchemy.orm import Session
from tables import Price, RentalPoint, Vehicle, User
from tables import DefectVehicle, Rental, Staff, TurnOver
from tables import engine_creator()

# squidward = User(name="squidward", fullname="Squidward Tentacles")
# krabs = User(name="ehkrabs", fullname="Eugene H. Krabs")

# with Session(engine) as session:
#     session.add(squidward)
#     session.add(krabs)
#     session.commit()

# with Session(engine) as session:
#     squidward = session.execute(select(User).filter_by(name="squidward")).scalar_one()
#     squidward.fullname = "Very mad"
#     squidward_fullname = session.execute(select(User.fullname).where(User.id == 1)).scalar_one()


class DataManager():
    def __init__(self):
        self.engine = engine_creator()
