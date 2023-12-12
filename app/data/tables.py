from datetime import datetime
from typing import List, Optional
from sqlalchemy import ForeignKey, create_engine
from sqlalchemy.orm import DeclarativeBase, Mapped
from sqlalchemy.orm import mapped_column, relationship

from app.data.tables import engine_creator


class Base(DeclarativeBase):
    pass


class Price(Base):
    __tablename__ = "prices"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    category: Mapped[str]
    day: Mapped[int]
    first_hour: Mapped[int]
    hour: Mapped[int]
    p24hours: Mapped[int]


class RentalPoint(Base):
    __tablename__ = "rental_points"

    id: Mapped[int] = mapped_column(primary_key=True)
    key: Mapped[str]
    name: Mapped[str]

    rentals: Mapped[List["Rental"]] = relationship(back_populates="rental_point")
    users: Mapped[List["User"]] = relationship(back_populates="current_rental_point")
    vehicles: Mapped[List["Vehicle"]] = relationship(back_populates="rental_point")
    defect_vehicles: Mapped[List["DefectVehicle"]] = relationship(back_populates="rental_point")


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str]
    first_name: Mapped[str]
    full_name: Mapped[str]
    password: Mapped[str]
    role: Mapped[str]

    current_rental_point: Mapped[RentalPoint] = relationship(back_populates="user")


class Vehicle(Base):
    __tablename__ = "vehicles"

    id: Mapped[int] = mapped_column(primary_key=True)
    rental_point_id = mapped_column(ForeignKey("rentals.id"))
    ready_to_use: Mapped[bool]
    rented: Mapped[bool]
    superior_category: Mapped[str]
    sub_category: Mapped[str]
    vehicle_tag: Mapped[str]

    fault: Mapped["DefectVehicle"] = relationship(back_populates="vehicle")
    rental_point: Mapped[RentalPoint] = relationship(back_populates="vehicles")


class DefectVehicle(Base):
    __tablename__ = "defect_vehicles"

    id: Mapped[int] = mapped_column(primary_key=True)
    rental_point_id = mapped_column(ForeignKey("rentals.id"))
    vehicle_id = mapped_column(ForeignKey("vehicles.id"))
    date: Mapped[datetime]
    description: Mapped[str]

    vehicle: Mapped[Vehicle] = relationship(back_populates="fault") 
    rentalpoint: Mapped[RentalPoint] = relationship(back_populates="defect_vehicles")


class Rental(Base):
    __tablename__ = "rentals"

    id: Mapped[int] = mapped_column(primary_key=True)
    phone: Mapped[str]
    postcode: Mapped[str]
    lastName: Mapped[str]
    firstName: Mapped[str]
    pesel: Mapped[str]
    peselSelected: Mapped[bool]
    streetAndNumber: Mapped[str]
    idNumber: Mapped[str]
    addressSelected: Mapped[bool]
    email: Mapped[str]
    country: Mapped[str]
    countryCode: Mapped[str]

    current: Mapped[int]
    days: Mapped[int]
    hours: Mapped[str]
    interval: Mapped[str]
    liabilty: Mapped[float]
    location: Mapped[str]
    rented: Mapped[bool]
    startRentalTime: Mapped[str]

    rental_point: Mapped[RentalPoint] = relationship(back_populates="rentals")
    payments: Mapped[List["Payment"]] = relationship(back_populates="rental")
    liabilities: Mapped[List["Liability"]] = relationship(back_populates="rental")
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


class TurnOver(Base):
    __tablename__ = "turnover"

    id: Mapped[int] = mapped_column(primary_key=True)
    date: Mapped[str]
    issuing: Mapped[str]
    rentalpoint: Mapped[str]
    turnover: Mapped[str]


engine = engine_creator()

Base.metadata.create_all(engine)

