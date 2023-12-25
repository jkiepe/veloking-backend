from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from passlib.context import CryptContext
from decouple import config
import pandas

from app import crud
from app.models import tables, schemas

TABLES = ["points", "users"]
USER = config("user")
PASSWORD = config("password")
DATABASE = config("database")
PORT = config("port")
HOST = config("host")
URL = f"postgresql+psycopg2://{USER}:{PASSWORD}@{HOST}:{PORT}/{DATABASE}"

engine = create_engine(URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
crypt = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_json(table):
    json = f"app/constants/{table}.json"
    df = pandas.read_json(json)
    data_dict = df.to_dict()
    return data_dict


def setup():
    tables.Table.metadata.create_all(bind=engine)
    db = SessionLocal()
    if not db.query(tables.Point).filter(tables.Point.id == 1).first():
        for table in TABLES:
            data = get_json(table)
            for (number, item) in data[table].items():
                if table == "points":
                    point = schemas.PointSchema(key = item["key"], name = item["name"])
                    crud.point_create(point, db)

                if table == "users":
                    user = schemas.UserSchema(
                        username = item["username"],
                        password = item["password"],
                        fullname = item["fullname"],
                        role = item["role"]
                    )
                    crud.user_create(user, db)
    db.close()

