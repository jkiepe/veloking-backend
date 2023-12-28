from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from passlib.context import CryptContext
from decouple import config
import pandas

from app import crud
from app.models import tables, schemas

TABLES = ["points", "users", "prices", "vehicles"]
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
                    point = schemas.PointSchema(point_key = item["point_key"], name = item["name"])
                    crud.point_create(point, db)

                if table == "users":
                    user = schemas.UserSchema(
                        username = item["username"],
                        password = item["password"],
                        fullname = item["fullname"],
                    role = item["role"]
                    )
                    crud.user_create(user, db)

                if table == "prices":
                    if item["superior_category"] == "bike":
                        price = schemas.PriceSchema(
                            superior_category = item["superior_category"],
                            day = item["day"],
                            first_hour = item["first_hour"],
                            hour = item["hour"],
                            per_24_hours = item["per_24_hours"],
                        )
                    else:
                        price = schemas.PriceSchema(
                            superior_category = item["superior_category"],
                            day = item["day"],
                            half_hour = item["half_hour"],
                            hour = item["hour"],
                            per_24_hours = item["per_24_hours"],
                        )
                    crud.price_create(price, db)
                if table == "vehicles":
                    vehicle = schemas.VehicleSchema(
                            superior_category = item["superior_category"],
                            sub_category = item["sub_category"],
                            vehicle_key = item["vehicle_key"],
                        )
                    crud.vehicle_create(vehicle, db)

    db.close()

