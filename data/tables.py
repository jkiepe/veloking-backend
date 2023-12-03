from datetime import datetime
from typing import List, Optional
from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, Mapped
from sqlalchemy.orm import mapped_column

URI = "postgresql://dr:Lucky786@localhost:5432/veloking"


class Base(DeclarativeBase):
    pass


class Price(Base):
    __tablename__ = "prices"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    category: Mapped[str]
    day: Mapped[int]
    firstHour: Mapped[int]
    hour: Mapped[int]
    p24hours: Mapped[int]


class RentalPoint(Base):
    __tablename__ = "rentalpoints"

    id: Mapped[int] = mapped_column(primary_key=True)
    key: Mapped[str]
    name: Mapped[str]


class Vehicle(Base):
    __tablename__ = "vehicles"

    id: Mapped[int] = mapped_column(primary_key=True)
    categoryId: Mapped[str]
    readyToUse: Mapped[str]
    rentarlPoint: Mapped[str]
    rented: Mapped[str]
    superiorCategory: Mapped[str]
    vehicleid: Mapped[str]


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str]
    firstName: Mapped[str]
    lastName: Mapped[str]
    rentalPoint: Mapped[str]
    role: Mapped[str]


class DefectVehicle(Base):
    __tablename__ = "defectvehicles"

    id: Mapped[int] = mapped_column(primary_key=True)
    date: Mapped[datetime]
    rentalpoint: Mapped[str]


class Rental(Base):
    __tablename__ = "rentals"

    id: Mapped[int] = mapped_column(primary_key=True)


class Staff(Base):
    __tablename__ = "staff"

    id: Mapped[int] = mapped_column(primary_key=True)
    firstName: Mapped[str]
    lastName: Mapped[str]

    
class TurnOver(Base):
    __tablename__ = "turnover"

    id: Mapped[int] = mapped_column(primary_key=True)
    date: Mapped[str]
    issuing: Mapped[str]
    rentalpoint: Mapped[str]
    turnover: Mapped[str]


def engine_creator(want_echo=False):
    engine = create_engine(URI, echo=want_echo)
    return engine

engine = engine_creator()

Base.metadata.create_all(engine)

