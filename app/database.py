from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from passlib.context import CryptContext

URL = f"postgresql://jonasz@localhost:5432/veloking"

engine = create_engine(
    URL
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Table = declarative_base()

crypt = CryptContext(schemes=["bcrypt"], deprecated="auto")
