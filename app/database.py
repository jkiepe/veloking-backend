from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from passlib.context import CryptContext
from decouple import config

USER = config("user")
PASSWORD = config("password")
DATABASE = config("database")
PORT = config("port")
HOST = config("host")

URL = f"postgresql+psycopg2://{USER}:{PASSWORD}@{HOST}:{PORT}/{DATABASE}"

engine = create_engine(
    URL
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Table = declarative_base()

crypt = CryptContext(schemes=["bcrypt"], deprecated="auto")
