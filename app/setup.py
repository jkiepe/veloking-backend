from sqlalchemy import create_engine, select
from sqlalchemy.orm import Session
from sqlalchemy.exc import NoResultFound
from passlib.context import CryptContext
from app.database import engine
from app import tables

crypt = CryptContext(schemes=["bcrypt"], deprecated="auto")
tables.Table.metadata.create_all(bind=engine)

waiting_room = tables.Point(
    key = "waiting",
    name = "Waiting Room"
    )

admin = tables.User(
    username = "admin",
    password = crypt.hash("admin"),
    role = "admin"
)

waiting_room.users.append(admin)

URI = "postgresql://jonasz@localhost:5432/veloking"
engine = create_engine(URI)


def setup_database():
    with Session(engine) as session:
        try:
            session.execute(select(tables.Point).filter_by(id=1)).scalar_one()
        except NoResultFound:
            session.add(waiting_room)
            session.commit()
