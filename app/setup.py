from sqlalchemy import create_engine, select
from sqlalchemy.orm import Session
from sqlalchemy.exc import NoResultFound
from passlib.context import CryptContext
from app.database import engine
from app import tables

crypt = CryptContext(schemes=["bcrypt"], deprecated="auto")
tables.Table.metadata.create_all(bind=engine)

unassigned = tables.Point(
    key = "unassigned",
    name = "No Point assigned"
)

office = tables.Point(
    key = "office",
    name = "Office"
)

workshop = tables.Point(
    key = "workshop",
    name = "Workshop"
)

piastowska = tables.Point(
    key = "piastowska",
    name = "Piastowska"
)

chinese_hotel = tables.Point(
    key = "chinese_hotel",
    name = "Chinese Hotel"
)

grand_hotel = tables.Point(
    key = "grand_hotel",
    name = "Grand Hotel"
)

admin = tables.User(
    username = "admin",
    password = crypt.hash("admin"),
    fullname = "adminadmin",
    disabled = False,
    role = "admin",
)

unassigned.users.append(admin)

def setup_database():
    with Session(engine) as session:
        try:
            session.execute(select(tables.Point).filter_by(key="unassigned")).scalar_one()
        except NoResultFound:
            session.add(unassigned)
            session.add(office)
            session.add(workshop)
            session.add(piastowska)
            session.add(chinese_hotel)
            session.add(grand_hotel)
            session.commit()
