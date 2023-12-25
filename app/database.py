from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from passlib.context import CryptContext
from decouple import config
import pandas as pd

from . import tables

TABLES = ["points"]
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
    df = pd.read_json(json)
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
                    db.add(tables.Point(key = item["key"], name = item["name"]))
        db.commit()
    db.close()

