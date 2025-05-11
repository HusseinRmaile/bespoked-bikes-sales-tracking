"""
This file handles all the database interactions.
Keeping SQL logic separate from the API routes makes the code cleaner and easier to maintain.
"""

from sqlalchemy.orm import Session
import models, schemas

# ---------- PRODUCTS ----------

def get_products(db: Session):
    return db.query(models.Product).all()

def get_product(db: Session, product_id: int):
    return db.query(models.Product).filter(models.Product.id == product_id).first()

def create_product(db: Session, product: schemas.ProductCreate):
    """
    Creates a new product.

    NOTE: The assignment requires no duplicate product names.
    The API route will handle checking for an existing product before calling this function.
    """
    db_product = models.Product(**product.dict())
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product

def update_product(db: Session, product_id: int, product: schemas.ProductCreate):
    db_product = get_product(db, product_id)
    if db_product:
        for key, value in product.dict().items():
            setattr(db_product, key, value)
        db.commit()
        db.refresh(db_product)
    return db_product

# ---------- SALESPERSONS ----------

def get_salespersons(db: Session):
    return db.query(models.Salesperson).all()

def get_salesperson(db: Session, salesperson_id: int):
    return db.query(models.Salesperson).filter(models.Salesperson.id == salesperson_id).first()

def create_salesperson(db: Session, salesperson: schemas.SalespersonCreate):
    """
    Creates a new salesperson.

    NOTE: The assignment requires no duplicate salespersons.
    The API route will check for an existing salesperson before calling this function.
    """
    db_salesperson = models.Salesperson(**salesperson.dict())
    db.add(db_salesperson)
    db.commit()
    db.refresh(db_salesperson)
    return db_salesperson

def update_salesperson(db: Session, salesperson_id: int, salesperson: schemas.SalespersonCreate):
    db_salesperson = get_salesperson(db, salesperson_id)
    if db_salesperson:
        for key, value in salesperson.dict().items():
            setattr(db_salesperson, key, value)
        db.commit()
        db.refresh(db_salesperson)
    return db_salesperson

# ---------- CUSTOMERS ----------

def get_customers(db: Session):
    return db.query(models.Customer).all()

def get_customer(db: Session, customer_id: int):
    return db.query(models.Customer).filter(models.Customer.id == customer_id).first()

def create_customer(db: Session, customer: schemas.CustomerCreate):
    db_customer = models.Customer(**customer.dict())
    db.add(db_customer)
    db.commit()
    db.refresh(db_customer)
    return db_customer

def update_customer(db: Session, customer_id: int, customer: schemas.CustomerCreate):
    db_customer = db.query(models.Customer).filter(models.Customer.id == customer_id).first()
    if db_customer:
        for key, value in customer.dict().items():
            setattr(db_customer, key, value)
        db.commit()
        db.refresh(db_customer)
    return db_customer

# ---------- SALES ----------

def get_sales(db: Session):
    return db.query(models.Sale).all()

def get_sale(db: Session, sale_id: int):
    return db.query(models.Sale).filter(models.Sale.id == sale_id).first()

def create_sale(db: Session, sale: schemas.SaleCreate):
    product = db.query(models.Product).filter(models.Product.id == sale.product_id).first()
    if product:
        if product.qty_on_hand > 0:
            product.qty_on_hand -= 1
        else:
            raise ValueError("Cannot create sale. Product is out of stock.")

    db_sale = models.Sale(**sale.dict())
    db.add(db_sale)
    db.commit()
    db.refresh(db_sale)
    return db_sale

def update_sale(db: Session, sale_id: int, sale: schemas.SaleCreate):
    db_sale = db.query(models.Sale).filter(models.Sale.id == sale_id).first()
    if db_sale:
        for key, value in sale.dict().items():
            setattr(db_sale, key, value)
        db.commit()
        db.refresh(db_sale)
    return db_sale

def delete_sale(db: Session, sale_obj):
    product = db.query(models.Product).filter(models.Product.id == sale_obj.product_id).first()
    if product:
        product.qty_on_hand += 1
    db.delete(sale_obj)

# ---------- DISCOUNTS ----------

def get_discounts(db: Session):
    return db.query(models.Discount).all()

def get_discount(db: Session, discount_id: int):
    return db.query(models.Discount).filter(models.Discount.id == discount_id).first()

def create_discount(db: Session, discount: schemas.DiscountCreate):
    db_discount = models.Discount(**discount.dict())
    db.add(db_discount)
    db.commit()
    db.refresh(db_discount)
    return db_discount

def update_discount(db: Session, discount_id: int, discount: schemas.DiscountCreate):
    db_discount = db.query(models.Discount).filter(models.Discount.id == discount_id).first()
    if db_discount:
        for key, value in discount.dict().items():
            setattr(db_discount, key, value)
        db.commit()
        db.refresh(db_discount)
    return db_discount
