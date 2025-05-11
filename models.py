from sqlalchemy import Column, Integer, String, Float, Date, ForeignKey
from sqlalchemy.orm import relationship
from database import Base

# Product table
class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    manufacturer = Column(String)
    style = Column(String)
    purchase_price = Column(Float)
    sale_price = Column(Float)
    qty_on_hand = Column(Integer)
    commission_percentage = Column(Float)

# Salesperson table
class Salesperson(Base):
    __tablename__ = "salespersons"

    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String)
    last_name = Column(String)
    address = Column(String)
    phone = Column(String)
    start_date = Column(Date)
    termination_date = Column(Date, nullable=True)
    manager = Column(String)

# Customer table
class Customer(Base):
    __tablename__ = "customers"

    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String)
    last_name = Column(String)
    address = Column(String)
    phone = Column(String)
    start_date = Column(Date)

# Sales table
class Sale(Base):
    __tablename__ = "sales"

    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey("products.id"))
    salesperson_id = Column(Integer, ForeignKey("salespersons.id"))
    customer_id = Column(Integer, ForeignKey("customers.id"))
    sales_date = Column(Date)

    product = relationship("Product")
    salesperson = relationship("Salesperson")
    customer = relationship("Customer")

# Discount table
class Discount(Base):
    __tablename__ = "discounts"

    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey("products.id"))
    begin_date = Column(Date)
    end_date = Column(Date)
    discount_percentage = Column(Float)

    product = relationship("Product")