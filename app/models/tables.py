from typing import List, Optional
from sqlalchemy import ForeignKey
from sqlalchemy.orm import mapped_column, relationship, Mapped
from sqlalchemy.ext.declarative import declarative_base

Table = declarative_base()

class Price(Table):
    __tablename__ = "prices"

    id: Mapped[int] = mapped_column(primary_key=True)
    superior_category: Mapped[str]
    day: Mapped[int]
    first_hour: Mapped[Optional[int]]
    half_hour: Mapped[Optional[int]]
    hour: Mapped[int]
    per_24_hours: Mapped[int]

class Point(Table):
    __tablename__ = "rental_points"

    id: Mapped[int] = mapped_column(primary_key=True)
    point_key: Mapped[str]
    name: Mapped[str]
    users: Mapped[List["User"]] = relationship(back_populates="rental_point")
    vehicles: Mapped[List["Vehicle"]] = relationship(back_populates="rental_point")


class User(Table):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str]
    password: Mapped[str]
    fullname: Mapped[str]
    disabled: Mapped[bool]
    role: Mapped[str]
    rental_point_id = mapped_column(ForeignKey("rental_points.id"))
    rental_point: Mapped[Point] = relationship(back_populates="users")


class Vehicle(Table):
    __tablename__ = "vehicles"

    id: Mapped[int] = mapped_column(primary_key=True)
    rented: Mapped[bool]
    superior_category: Mapped[str]
    sub_category: Mapped[str]
    vehicle_key: Mapped[str]
    rental_point_id = mapped_column(ForeignKey("rental_points.id"))
    rental_point: Mapped[Point] = relationship(back_populates="vehicles")

# class Rental(Table):
#     __tablename__ = "rentals"
#
#     current: Mapped[int]
#     days: Mapped[int]
#     hours: Mapped[str]
#     interval: Mapped[str]
#     liability: Mapped[float]
#     rented: Mapped[bool]
#     start_time: Mapped[str]
#
#     id: Mapped[int] = mapped_column(primary_key=True)
#     rental_point_id = mapped_column(ForeignKey("rental_points.id"))
#     user_id = mapped_column(ForeignKey("users.id"))
#     # customer_id = mapped_column(ForeignKey("customers.id"))
#
#     user: Mapped[User] = relationship(back_populates="rentals")
#     rental_point: Mapped[Point] = relationship(back_populates="rentals")
    # customer: Mapped[Customer] = relationship(back_populates="rentals")
    # payments: Mapped[List["Payment"]] = relationship(back_populates="rental")
    # liabilities: Mapped[List["Liability"]] = relationship(back_populates="rental")
    # vehicles: Mapped[List["Equipment"]] = relationship(back_populates="rental")





# class Customer(Base):
#     __tablename__ = "customers"

#     id: Mapped[int] = mapped_column(primary_key=True)

#     phone: Mapped[str]
#     postcode: Mapped[str]
#     lastName: Mapped[str]
#     firstName: Mapped[str]
#     pesel: Mapped[str]
#     peselSelected: Mapped[bool]
#     streetAndNumber: Mapped[str]
#     idNumber: Mapped[str]
#     addressSelected: Mapped[bool]
#     email: Mapped[str]
#     country: Mapped[str]
#     countryCode: Mapped[str]

#     rentals: Mapped[List["Rental"]] = relationship(back_populates="customer")


# class Liability(Base):
#     __tablename__ = "liability"

#     id: Mapped[int] = mapped_column(primary_key=True)
#     rental_id = mapped_column(ForeignKey("rentals.id"))

#     amount: Mapped[int]
#     rentailpoint: Mapped[str]
#     type: Mapped[str]

#     rental: Mapped[Rental] = relationship(back_populates="liabilities")


# class Payment(Base):
#     __tablename__ = "payment"

#     id: Mapped[int] = mapped_column(primary_key=True)
#     rentalId = mapped_column(ForeignKey("rentals.id"))

#     amount: Mapped[int]
#     paymentTimestamp: Mapped[str]
#     rentalpoint: Mapped[str]
#     type: Mapped[str]

#     rental: Mapped[Rental] = relationship(back_populates="payments")


# class Equipment(Base):
#     __tablename__ = "equipment"

#     id: Mapped[int] = mapped_column(primary_key=True)
#     rentalId = mapped_column(ForeignKey("rentals.id"))

#     endDateTime = Mapped[str]
#     returned = Mapped[bool]
#     startDateTime = Mapped[str]
#     vehicleId = Mapped[str]

#     rental: Mapped[Rental] = relationship(back_populates="vehicles")


# class TurnOver(Base):
#     __tablename__ = "turnover"

#     id: Mapped[int] = mapped_column(primary_key=True)

#     date: Mapped[str]
#     issuing: Mapped[str]
#     rentalpoint: Mapped[str]
#     turnover: Mapped[str]
