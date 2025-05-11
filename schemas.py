"""
Pydantic schemas to define the structure of the data used in requests and responses.
This helps ensure consistency and makes validation automatic.
"""

from datetime import date
from pydantic import BaseModel

# Product schema
class ProductBase(BaseModel):
    name: str
    manufacturer: str
    style: str
    purchase_price: float
    sale_price: float
    qty_on_hand: int
    commission_percentage: float

class ProductCreate(ProductBase):
    pass

class Product(ProductBase):
    id: int

    class Config:
        orm_mode = True

# Salesperson schema
class SalespersonBase(BaseModel):
    first_name: str
    last_name: str
    address: str
    phone: str
    start_date: date
    termination_date: date | None = None
    manager: str

class SalespersonCreate(SalespersonBase):
    pass

class Salesperson(SalespersonBase):
    id: int

    class Config:
        orm_mode = True

# Customer schema
class CustomerBase(BaseModel):
    first_name: str
    last_name: str
    address: str
    phone: str
    start_date: date

class CustomerCreate(CustomerBase):
    pass

class Customer(CustomerBase):
    id: int

    class Config:
        orm_mode = True

# Sale schema
class SaleBase(BaseModel):
    product_id: int
    salesperson_id: int
    customer_id: int
    sales_date: date

class SaleCreate(SaleBase):
    pass

class Sale(SaleBase):
    id: int

    class Config:
        orm_mode = True

# Discount schema
class DiscountBase(BaseModel):
    product_id: int
    begin_date: date
    end_date: date
    discount_percentage: float

class DiscountCreate(DiscountBase):
    pass

class Discount(DiscountBase):
    id: int

    class Config:
        orm_mode = True
