from sqlalchemy import Column, Integer, Boolean, String, Text, ForeignKey, DateTime, DATE
from sqlalchemy.orm import relationship
from sqlalchemy.sql.sqltypes import TIMESTAMP
from .database import Base
from sqlalchemy.sql import func
from sqlalchemy.sql.expression import text
from datetime import datetime
from sqlalchemy.schema import FetchedValue


class User(Base):
    __tablename__ = 'tbl_customer_master'
    id = Column(Integer, primary_key=True, nullable=False)
    name = Column(String(200), nullable=False)
    email = Column(String(200), nullable=False)
    phone = Column(String(10), nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=func.now())
    status = Column(Boolean, nullable=False, default=0)



class Inventory(Base):
    __tablename__ = 'tbl_inventory_master'
    id = Column(Integer, primary_key=True, nullable=False)
    vehicle_type = Column(String(200), nullable=False, unique=True)
    remaining = Column(Integer, nullable=False)
    allocated = Column(Integer, nullable=True)


class Rent(Base):
    __tablename__ = 'tbl_rent_master'
    id = Column(Integer, primary_key=True, nullable=False)
    user_id = Column(Integer, ForeignKey('tbl_customer_master.id', ondelete="CASCADE"), nullable=False)
    inv_id = Column(Integer, ForeignKey('tbl_inventory_master.id', ondelete="CASCADE"), nullable=False)
    rental_date = Column(DATE, nullable=True)
    return_date = Column(DATE, nullable=True)


class Emp(Base):
    __tablename__ = 'tbl_emp_master'
    id = Column(Integer, primary_key=True, nullable=False)
    name = Column(String(200), nullable=False)
    email = Column(String(200), nullable=False)
    phone = Column(String(10), nullable=False)
    password = Column(String(255),nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))