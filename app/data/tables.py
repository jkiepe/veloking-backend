from datetime import datetime
from typing import List, Optional
from sqlalchemy import ForeignKey, create_engine
from sqlalchemy.orm import DeclarativeBase, Mapped
from sqlalchemy.orm import mapped_column, relationship

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
    addressSelected: Mapped[bool]
    country: Mapped[str]
    countryCode: Mapped[str]
    current: Mapped[int]
    days: Mapped[int]
    email: Mapped[str]
    firstName: Mapped[str]
    hours: Mapped[str]
    idNumber: Mapped[str]
    interval: Mapped[str]
    lastName: Mapped[str]
    liabilities: Mapped[List["Liability"]] = relationship(back_populates="rental")
    liabilty: Mapped[float]
    location: Mapped[str]
    payments: Mapped[List["Payment"]] = relationship(back_populates="rental")
    pesel: Mapped[str]
    peselSelected: Mapped[bool]
    phone: Mapped[str]
    postcode: Mapped[str]
    rentalpoint: Mapped[str]
    rented: Mapped[bool]
    startRentalTime: Mapped[str]
    streetAndNumber: Mapped[str]
    vehicles: Mapped[List["Equipment"]] = relationship(back_populates="rental")


class Liability(Base):
    __tablename__ = "liability"

    id: Mapped[int] = mapped_column(primary_key=True)
    rentalId = mapped_column(ForeignKey("rentals.id"))
    amount: Mapped[int]
    rentailpoint: Mapped[str]
    type: Mapped[str]

    rental: Mapped[Rental] = relationship(back_populates="liabilities")


class Payment(Base):
    __tablename__ = "payment"

    id: Mapped[int] = mapped_column(primary_key=True)
    rentalId = mapped_column(ForeignKey("rentals.id"))
    amount: Mapped[int]
    paymentTimestamp: Mapped[str]
    rentalpoint: Mapped[str]
    type: Mapped[str]

    rental: Mapped[Rental] = relationship(back_populates="payments")


class Equipment(Base):
    __tablename__ = "equipment"

    id: Mapped[int] = mapped_column(primary_key=True)
    rentalId = mapped_column(ForeignKey("rentals.id"))
    endDateTime = Mapped[str]
    returned = Mapped[bool]
    startDateTime = Mapped[str]
    vehicleId = Mapped[str]

    rental: Mapped[Rental] = relationship(back_populates="vehicles")


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


TABLES = {
    "prices": Price,
    "rentalpoints": RentalPoint,
    "vehicles": Vehicle,
    "users": User,
    "defectvehicles": DefectVehicle,
    "rentals": Rental,
    "staff": Staff,
    "turnover": TurnOver,
}

engine = engine_creator()

Base.metadata.create_all(engine)

