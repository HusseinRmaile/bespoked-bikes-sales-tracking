"""
This file defines the main FastAPI app and routes.
It acts as the 'controller' layer, handling requests and responses.
"""

from fastapi import FastAPI, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import and_
from database import SessionLocal, engine, Base
from datetime import date, timedelta
import models, crud, schemas

# Create database tables at startup if they don't exist
Base.metadata.create_all(bind=engine)

# Create FastAPI app instance
app = FastAPI()

# Dependency: Get DB session for each request
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# ---------- Root test route ----------
@app.get("/")
def read_root():
    return {"message": "BeSpoked Bikes App is running!"}

# ---------- PRODUCTS ----------

@app.get("/products/", response_model=list[schemas.Product])
def read_products(db: Session = Depends(get_db)):
    return crud.get_products(db)

@app.post("/products/", response_model=schemas.Product)
def create_product(product: schemas.ProductCreate, db: Session = Depends(get_db)):
    """
    Creates a new product if it does not already exist.
    Normalizes all string fields (strip + lowercase) for clean storage and duplicate prevention.
    """
    # Normalize all string fields
    product.name = product.name.strip().lower()
    product.manufacturer = product.manufacturer.strip().lower()
    product.style = product.style.strip().lower()

    # Check for existing product
    db_product = db.query(models.Product).filter(models.Product.name == product.name).first()
    if db_product:
        raise HTTPException(status_code=400, detail="Product already exists.")

    return crud.create_product(db, product)

@app.put("/products/{product_id}", response_model=schemas.Product)
def update_product(product_id: int, product: schemas.ProductCreate, db: Session = Depends(get_db)):
    """
    Updates an existing product.
    Normalizes string fields (name, manufacturer, style).
    """
    # Normalize string fields
    product.name = product.name.strip().lower()
    product.manufacturer = product.manufacturer.strip().lower()
    product.style = product.style.strip().lower()

    db_product = crud.update_product(db, product_id, product)
    if not db_product:
        raise HTTPException(status_code=404, detail="Product not found.")
    return db_product

@app.delete("/products/{product_id}")
def delete_product(product_id: int, db: Session = Depends(get_db)):
    db_product = crud.get_product(db, product_id)
    if not db_product:
        raise HTTPException(status_code=404, detail="Product not found.")
    db.delete(db_product)
    db.commit()
    return {"detail": "Product deleted successfully."}

# ---------- SALESPERSONS ----------

@app.get("/salespersons/", response_model=list[schemas.Salesperson])
def read_salespersons(db: Session = Depends(get_db)):
    return crud.get_salespersons(db)

@app.post("/salespersons/", response_model=schemas.Salesperson)
def create_salesperson(salesperson: schemas.SalespersonCreate, db: Session = Depends(get_db)):
    """
    Creates a new salesperson if they do not already exist.
    Normalizes all string fields: first_name, last_name, address, manager (strip + lowercase), phone (strip only).
    """
    # Normalize all string fields
    salesperson.first_name = salesperson.first_name.strip().lower()
    salesperson.last_name = salesperson.last_name.strip().lower()
    salesperson.address = salesperson.address.strip().lower()
    salesperson.manager = salesperson.manager.strip().lower()
    salesperson.phone = salesperson.phone.strip()

    # Check for existing salesperson
    db_salesperson = db.query(models.Salesperson).filter(
        models.Salesperson.first_name == salesperson.first_name,
        models.Salesperson.last_name == salesperson.last_name,
        models.Salesperson.phone == salesperson.phone
    ).first()
    if db_salesperson:
        raise HTTPException(status_code=400, detail="Salesperson already exists.")

    return crud.create_salesperson(db, salesperson)

@app.put("/salespersons/{salesperson_id}", response_model=schemas.Salesperson)
def update_salesperson(salesperson_id: int, salesperson: schemas.SalespersonCreate, db: Session = Depends(get_db)):
    """
    Updates an existing salesperson.
    Normalizes string fields (first_name, last_name, manager) with strip + lowercase.
    Address and phone use strip only.
    """
    # Normalize string fields
    salesperson.first_name = salesperson.first_name.strip().lower()
    salesperson.last_name = salesperson.last_name.strip().lower()
    salesperson.address = salesperson.address.strip().lower()
    salesperson.manager = salesperson.manager.strip().lower()
    salesperson.phone = salesperson.phone.strip()

    db_salesperson = crud.update_salesperson(db, salesperson_id, salesperson)
    if not db_salesperson:
        raise HTTPException(status_code=404, detail="Salesperson not found.")
    return db_salesperson

@app.delete("/salespersons/{salesperson_id}")
def delete_salesperson(salesperson_id: int, db: Session = Depends(get_db)):
    db_salesperson = crud.get_salesperson(db, salesperson_id)
    if not db_salesperson:
        raise HTTPException(status_code=404, detail="Salesperson not found.")
    db.delete(db_salesperson)
    db.commit()
    return {"detail": "Salesperson deleted successfully."}

# ---------- CUSTOMERS ----------

@app.get("/customers/", response_model=list[schemas.Customer])
def read_customers(db: Session = Depends(get_db)):
    return crud.get_customers(db)

@app.post("/customers/", response_model=schemas.Customer)
def create_customer(customer: schemas.CustomerCreate, db: Session = Depends(get_db)):
    """
    Creates a new customer.
    Normalizes first_name and last_name (strip + lowercase), address and phone (strip only).
    No duplicate check required per assignment.
    """
    # Normalize all string fields
    customer.first_name = customer.first_name.strip().lower()
    customer.last_name = customer.last_name.strip().lower()
    customer.address = customer.address.strip().lower()
    customer.phone = customer.phone.strip()

    return crud.create_customer(db, customer)

@app.put("/customers/{customer_id}", response_model=schemas.Customer)
def update_customer(customer_id: int, customer: schemas.CustomerCreate, db: Session = Depends(get_db)):
    """
    Updates an existing customer.
    Normalizes first_name and last_name (strip + lowercase), address and phone (strip only).
    """
    customer.first_name = customer.first_name.strip().lower()
    customer.last_name = customer.last_name.strip().lower()
    customer.address = customer.address.strip().lower()
    customer.phone = customer.phone.strip()

    db_customer = crud.update_customer(db, customer_id, customer)
    if not db_customer:
        raise HTTPException(status_code=404, detail="Customer not found.")
    return db_customer

@app.delete("/customers/{customer_id}")
def delete_customer(customer_id: int, db: Session = Depends(get_db)):
    db_customer = crud.get_customer(db, customer_id)
    if not db_customer:
        raise HTTPException(status_code=404, detail="Customer not found.")
    db.delete(db_customer)
    db.commit()
    return {"detail": "Customer deleted successfully."}

# ---------- SALES ----------

@app.get("/sales/", response_model=list[schemas.Sale])
def read_sales(db: Session = Depends(get_db)):
    return crud.get_sales(db)

@app.post("/sales/", response_model=schemas.Sale)
def create_sale(sale: schemas.SaleCreate, db: Session = Depends(get_db)):
    """
    Creates a new sale record.
    Sales uses IDs only so no normalization is needed.
    """
    return crud.create_sale(db, sale)

@app.put("/sales/{sale_id}", response_model=schemas.Sale)
def update_sale(sale_id: int, sale: schemas.SaleCreate, db: Session = Depends(get_db)):
    """
    Updates an existing sale.
    No normalization needed (no string fields).
    """
    db_sale = crud.update_sale(db, sale_id, sale)
    if not db_sale:
        raise HTTPException(status_code=404, detail="Sale not found.")
    return db_sale

@app.delete("/sales/{sale_id}")
def delete_sale(sale_id: int, db: Session = Depends(get_db)):
    db_sale = crud.get_sale(db, sale_id)
    if not db_sale:
        raise HTTPException(status_code=404, detail="Sale not found.")
    crud.delete_sale(db, db_sale)
    db.commit()
    return {"detail": "Sale deleted successfully."}

# ---------- DISCOUNTS ----------

@app.get("/discounts/", response_model=list[schemas.Discount])
def read_discounts(db: Session = Depends(get_db)):
    return crud.get_discounts(db)

@app.post("/discounts/", response_model=schemas.Discount)
def create_discount(discount: schemas.DiscountCreate, db: Session = Depends(get_db)):
    """
    Creates a new discount.
    No normalization needed (no string fields).
    """
    return crud.create_discount(db, discount)

@app.put("/discounts/{discount_id}", response_model=schemas.Discount)
def update_discount_route(discount_id: int, discount: schemas.DiscountCreate, db: Session = Depends(get_db)):
    """
    Updates an existing discount.
    No normalization needed (no string fields).
    """
    db_discount = crud.update_discount(db, discount_id, discount)
    if not db_discount:
        raise HTTPException(status_code=404, detail="Discount not found.")
    return db_discount

@app.delete("/discounts/{discount_id}")
def delete_discount(discount_id: int, db: Session = Depends(get_db)):
    db_discount = crud.get_discount(db, discount_id)
    if not db_discount:
        raise HTTPException(status_code=404, detail="Discount not found.")
    db.delete(db_discount)
    db.commit()
    return {"detail": "Discount deleted successfully."}

# ---------- COMMISSION REPORT ----------

@app.get("/commission_report/")
def get_commission_report(
    year: int = Query(..., description="Year for the report"),
    quarter: int = Query(..., ge=1, le=4, description="Quarter (1-4) for the report"),
    db: Session = Depends(get_db)
):
    """
    Calculates and returns the quarterly commission report for all salespersons.
    """

    # Calculate quarter start and end dates
    quarter_start_month = (quarter - 1) * 3 + 1
    quarter_end_month = quarter_start_month + 2

    from datetime import date
    quarter_start = date(year, quarter_start_month, 1)
    if quarter_end_month == 12:
        quarter_end = date(year, 12, 31)
    else:
        quarter_end = date(year, quarter_end_month + 1, 1) - timedelta(days=1)

    report = []

    salespersons = db.query(models.Salesperson).all()

    for sp in salespersons:
        sales = db.query(models.Sale).filter(
            models.Sale.salesperson_id == sp.id,
            and_(
                models.Sale.sales_date >= quarter_start,
                models.Sale.sales_date <= quarter_end
            )
        ).all()

        num_sales = len(sales)
        total_sales_amount = 0.0
        total_commission = 0.0

        for sale in sales:
            product = sale.product
            price = product.sale_price

            # Check if any discount applied to this product at time of sale
            discount = db.query(models.Discount).filter(
                models.Discount.product_id == product.id,
                models.Discount.begin_date <= sale.sales_date,
                models.Discount.end_date >= sale.sales_date
            ).first()

            if discount:
                price = price * (1 - discount.discount_percentage / 100)

            commission = price * (product.commission_percentage / 100)
            total_sales_amount += price
            total_commission += commission

        report.append({
            "salesperson_id": sp.id,
            "first_name": sp.first_name,
            "last_name": sp.last_name,
            "num_sales": num_sales,
            "total_sales_amount": round(total_sales_amount, 2),
            "total_commission": round(total_commission, 2)
        })

    return report