from typing import List 
from sqlalchemy import ForeignKey
from sqlalchemy.orm import mapped_column, relationship, Mapped

from app.database import Table


class RentalPoint(Table):
    __tablename__ = "rental_points"

    key: Mapped[str]
    name: Mapped[str]

    id: Mapped[int] = mapped_column(primary_key=True)

    users: Mapped[List["User"]] = relationship(back_populates="current_rental_point")
    # rentals: Mapped[List["Rental"]] = relationship(back_populates="rental_point")
    # vehicles: Mapped[Optional[List["Vehicle"]]] = relationship(back_populates="rental_point")
    # defect_vehicles: Mapped[Optional[List["DefectVehicle"]]] = relationship(back_populates="rental_point")


class User(Table):
    __tablename__ = "users"

    username: Mapped[str]
    password: Mapped[str]
    role: Mapped[str]

    id: Mapped[int] = mapped_column(primary_key=True)
    rental_point_id = mapped_column(ForeignKey("rental_points.id"))

    current_rental_point: Mapped[RentalPoint] = relationship(back_populates="users")
    # rentals: Mapped[List["Rentals"]] = relationship(back_populates="user")


# class Rental(Base):
#     __tablename__ = "rentals"


#     current: Mapped[int]
#     days: Mapped[int]
#     hours: Mapped[str]
#     interval: Mapped[str]
#     liabilty: Mapped[float]
#     rented: Mapped[bool]
#     start_time: Mapped[str]

#     id: Mapped[int] = mapped_column(primary_key=True)
#     customer_id = mapped_column(ForeignKey("customers.id"))
#     rental_point_id = mapped_column(ForeignKey("rental_points.id"))
#     user_id = mapped_column(ForeignKey("users.id"))

#     user: Mapped[User] = relationship(back_populates="rentals")
#     customer: Mapped[Customer] = relationship(back_populates="rentals")
#     rental_point: Mapped[RentalPoint] = relationship(back_populates="rentals")
#     payments: Mapped[List["Payment"]] = relationship(back_populates="rental")
#     liabilities: Mapped[List["Liability"]] = relationship(back_populates="rental")
#     vehicles: Mapped[List["Equipment"]] = relationship(back_populates="rental")


# class DefectVehicle(Base):
#     __tablename__ = "defect_vehicles"

#     id: Mapped[int] = mapped_column(primary_key=True)

#     rental_point_id = mapped_column(ForeignKey("rentals.id"))
#     vehicle_id = mapped_column(ForeignKey("vehicles.id"))

#     date: Mapped[datetime]
#     description: Mapped[str]

#     rentalpoint: Mapped[RentalPoint] = relationship(back_populates="defect_vehicles")
#     vehicle: Mapped[List["Vehicle"]] = relationship(back_populates="fault") 


# class Vehicle(Base):
#     __tablename__ = "vehicles"

#     id: Mapped[int] = mapped_column(primary_key=True)
#     rental_point_id = mapped_column(ForeignKey("rentals.id"))

#     ready_to_use: Mapped[bool]
#     rented: Mapped[bool]
#     superior_category: Mapped[str]
#     sub_category: Mapped[str]
#     tag: Mapped[str]

#     rental_point: Mapped[RentalPoint] = relationship(back_populates="vehicles")
#     fault: Mapped[Optional[DefectVehicle]] = relationship(back_populates="vehicle")



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
