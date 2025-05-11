"""
This file defines the main FastAPI app and routes.
It acts as the 'controller' layer, handling requests and responses.
"""

from fastapi import FastAPI, Request, Form, Depends, HTTPException
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import Session
from database import SessionLocal, engine, Base
import models, crud, schemas

# initializes db on startup if not done already
Base.metadata.create_all(bind=engine)

app = FastAPI(title="BeSpoked Bikes Client App")

# Setup Jinja2 templates
templates = Jinja2Templates(directory="templates")

# Mount static files
app.mount("/static", StaticFiles(directory="static"), name="static")

# Dependency to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# ---------- Home Page ----------

@app.get("/")
def home(request: Request):
    return templates.TemplateResponse("home.html", {"request": request})

# ---------- Products Pages ----------

@app.get("/products/")
def list_products(request: Request, db: Session = Depends(get_db)):
    products = crud.get_products(db)
    return templates.TemplateResponse("products/list.html", {"request": request, "products": products})

@app.get("/products/create/")
def create_product_form(request: Request):
    return templates.TemplateResponse("products/create.html", {"request": request})

@app.post("/products/create/")
def create_product(
    request: Request,
    name: str = Form(...),
    manufacturer: str = Form(...),
    style: str = Form(...),
    purchase_price: float = Form(...),
    sale_price: float = Form(...),
    qty_on_hand: int = Form(...),
    commission_percentage: float = Form(...),
    db: Session = Depends(get_db)
):
    # normalize
    name = name.strip().lower()
    manufacturer = manufacturer.strip().lower()
    style = style.strip().lower()

    existing = db.query(models.Product).filter(models.Product.name == name).first()
    if existing:
        raise HTTPException(status_code=400, detail="Product already exists.")

    product = schemas.ProductCreate(
        name=name,
        manufacturer=manufacturer,
        style=style,
        purchase_price=purchase_price,
        sale_price=sale_price,
        qty_on_hand=qty_on_hand,
        commission_percentage=commission_percentage
    )
    crud.create_product(db, product)
    return RedirectResponse(url="/products/", status_code=303)

@app.get("/products/{product_id}/edit/")
def edit_product_form(product_id: int, request: Request, db: Session = Depends(get_db)):
    product = crud.get_product(db, product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found.")
    return templates.TemplateResponse("products/edit.html", {"request": request, "product": product})

@app.post("/products/{product_id}/edit/")
def update_product(
    product_id: int,
    request: Request,
    name: str = Form(...),
    manufacturer: str = Form(...),
    style: str = Form(...),
    purchase_price: float = Form(...),
    sale_price: float = Form(...),
    qty_on_hand: int = Form(...),
    commission_percentage: float = Form(...),
    db: Session = Depends(get_db)
):
    product_data = schemas.ProductCreate(
        name=name.strip().lower(),
        manufacturer=manufacturer.strip().lower(),
        style=style.strip().lower(),
        purchase_price=purchase_price,
        sale_price=sale_price,
        qty_on_hand=qty_on_hand,
        commission_percentage=commission_percentage
    )
    updated = crud.update_product(db, product_id, product_data)
    if not updated:
        raise HTTPException(status_code=404, detail="Product not found.")
    return RedirectResponse(url="/products/", status_code=303)

@app.post("/products/{product_id}/delete/")
def delete_product(product_id: int, db: Session = Depends(get_db)):
    product = crud.get_product(db, product_id)
    if product:
        db.delete(product)
        db.commit()
    return RedirectResponse(url="/products/", status_code=303)

# ---------- Salespersons Pages ----------

@app.get("/salespersons/")
def list_salespersons(request: Request, db: Session = Depends(get_db)):
    salespersons = crud.get_salespersons(db)
    return templates.TemplateResponse("salespersons/list.html", {"request": request, "salespersons": salespersons})

@app.get("/salespersons/create/")
def create_salesperson_form(request: Request):
    return templates.TemplateResponse("salespersons/create.html", {"request": request})

@app.post("/salespersons/create/")
def create_salesperson(
    request: Request,
    first_name: str = Form(...),
    last_name: str = Form(...),
    address: str = Form(...),
    phone: str = Form(...),
    start_date: str = Form(...),
    termination_date: str = Form(None),
    manager: str = Form(...),
    db: Session = Depends(get_db)
):
    # normalize
    first_name = first_name.strip().lower()
    last_name = last_name.strip().lower()
    address = address.strip().lower()
    manager = manager.strip().lower()
    phone = phone.strip()

    existing = db.query(models.Salesperson).filter(
        models.Salesperson.first_name == first_name,
        models.Salesperson.last_name == last_name,
        models.Salesperson.phone == phone
    ).first()
    if existing:
        raise HTTPException(status_code=400, detail="Salesperson already exists.")

    sp_data = schemas.SalespersonCreate(
        first_name=first_name,
        last_name=last_name,
        address=address,
        phone=phone,
        start_date=start_date,
        termination_date=termination_date if termination_date else None,
        manager=manager
    )
    crud.create_salesperson(db, sp_data)
    return RedirectResponse(url="/salespersons/", status_code=303)

@app.get("/salespersons/{salesperson_id}/edit/")
def edit_salesperson_form(salesperson_id: int, request: Request, db: Session = Depends(get_db)):
    sp = crud.get_salesperson(db, salesperson_id)
    if not sp:
        raise HTTPException(status_code=404, detail="Salesperson not found.")
    return templates.TemplateResponse("salespersons/edit.html", {"request": request, "sp": sp})

@app.post("/salespersons/{salesperson_id}/edit/")
def update_salesperson(
    salesperson_id: int,
    request: Request,
    first_name: str = Form(...),
    last_name: str = Form(...),
    address: str = Form(...),
    phone: str = Form(...),
    start_date: str = Form(...),
    termination_date: str = Form(None),
    manager: str = Form(...),
    db: Session = Depends(get_db)
):
    sp_data = schemas.SalespersonCreate(
        first_name=first_name.strip().lower(),
        last_name=last_name.strip().lower(),
        address=address.strip().lower(),
        phone=phone.strip(),
        start_date=start_date,
        termination_date=termination_date if termination_date else None,
        manager=manager.strip().lower()
    )
    updated = crud.update_salesperson(db, salesperson_id, sp_data)
    if not updated:
        raise HTTPException(status_code=404, detail="Salesperson not found.")
    return RedirectResponse(url="/salespersons/", status_code=303)

@app.post("/salespersons/{salesperson_id}/delete/")
def delete_salesperson(salesperson_id: int, db: Session = Depends(get_db)):
    sp = crud.get_salesperson(db, salesperson_id)
    if sp:
        db.delete(sp)
        db.commit()
    return RedirectResponse(url="/salespersons/", status_code=303)

# ---------- Customers Pages ----------

@app.get("/customers/")
def list_customers(request: Request, db: Session = Depends(get_db)):
    customers = crud.get_customers(db)
    return templates.TemplateResponse("customers/list.html", {"request": request, "customers": customers})

@app.get("/customers/create/")
def create_customer_form(request: Request):
    return templates.TemplateResponse("customers/create.html", {"request": request})

@app.post("/customers/create/")
def create_customer(
    request: Request,
    first_name: str = Form(...),
    last_name: str = Form(...),
    address: str = Form(...),
    phone: str = Form(...),
    start_date: str = Form(...),
    db: Session = Depends(get_db)
):
    customer_data = schemas.CustomerCreate(
        first_name=first_name.strip().lower(),
        last_name=last_name.strip().lower(),
        address=address.strip().lower(),
        phone=phone.strip(),
        start_date=start_date
    )
    crud.create_customer(db, customer_data)
    return RedirectResponse(url="/customers/", status_code=303)

@app.get("/customers/{customer_id}/edit/")
def edit_customer_form(customer_id: int, request: Request, db: Session = Depends(get_db)):
    customer = crud.get_customer(db, customer_id)
    if not customer:
        raise HTTPException(status_code=404, detail="Customer not found.")
    return templates.TemplateResponse("customers/edit.html", {"request": request, "customer": customer})

@app.post("/customers/{customer_id}/edit/")
def update_customer(
    customer_id: int,
    request: Request,
    first_name: str = Form(...),
    last_name: str = Form(...),
    address: str = Form(...),
    phone: str = Form(...),
    start_date: str = Form(...),
    db: Session = Depends(get_db)
):
    customer_data = schemas.CustomerCreate(
        first_name=first_name.strip().lower(),
        last_name=last_name.strip().lower(),
        address=address.strip().lower(),
        phone=phone.strip(),
        start_date=start_date
    )
    updated = crud.update_customer(db, customer_id, customer_data)
    if not updated:
        raise HTTPException(status_code=404, detail="Customer not found.")
    return RedirectResponse(url="/customers/", status_code=303)

@app.post("/customers/{customer_id}/delete/")
def delete_customer(customer_id: int, db: Session = Depends(get_db)):
    customer = crud.get_customer(db, customer_id)
    if customer:
        db.delete(customer)
        db.commit()
    return RedirectResponse(url="/customers/", status_code=303)

# ---------- Sales Pages ----------

@app.get("/sales/")
def list_sales(request: Request, db: Session = Depends(get_db)):
    sales = crud.get_sales(db)
    return templates.TemplateResponse("sales/list.html", {"request": request, "sales": sales})

@app.get("/sales/create/")
def create_sale_form(request: Request, db: Session = Depends(get_db)):
    products = crud.get_products(db)
    salespersons = crud.get_salespersons(db)
    customers = crud.get_customers(db)
    return templates.TemplateResponse("sales/create.html", {
        "request": request,
        "products": products,
        "salespersons": salespersons,
        "customers": customers
    })

@app.post("/sales/create/")
def create_sale(
    request: Request,
    product_id: int = Form(...),
    salesperson_id: int = Form(...),
    customer_id: int = Form(...),
    sales_date: str = Form(...),
    db: Session = Depends(get_db)
):
    try:
        sale_data = schemas.SaleCreate(
            product_id=product_id,
            salesperson_id=salesperson_id,
            customer_id=customer_id,
            sales_date=sales_date
        )
        crud.create_sale(db, sale_data)
        return RedirectResponse(url="/sales/", status_code=303)
    except ValueError as e:
        products = crud.get_products(db)
        salespersons = crud.get_salespersons(db)
        customers = crud.get_customers(db)
        return templates.TemplateResponse("sales/create.html", {
            "request": request,
            "products": products,
            "salespersons": salespersons,
            "customers": customers,
            "error": str(e)
        })

@app.get("/sales/{sale_id}/edit/")
def edit_sale_form(sale_id: int, request: Request, db: Session = Depends(get_db)):
    sale = crud.get_sale(db, sale_id)
    if not sale:
        raise HTTPException(status_code=404, detail="Sale not found.")
    products = crud.get_products(db)
    salespersons = crud.get_salespersons(db)
    customers = crud.get_customers(db)
    return templates.TemplateResponse("sales/edit.html", {
        "request": request,
        "sale": sale,
        "products": products,
        "salespersons": salespersons,
        "customers": customers
    })

@app.post("/sales/{sale_id}/edit/")
def update_sale(
    sale_id: int,
    request: Request,
    product_id: int = Form(...),
    salesperson_id: int = Form(...),
    customer_id: int = Form(...),
    sales_date: str = Form(...),
    db: Session = Depends(get_db)
):
    sale_data = schemas.SaleCreate(
        product_id=product_id,
        salesperson_id=salesperson_id,
        customer_id=customer_id,
        sales_date=sales_date
    )
    updated = crud.update_sale(db, sale_id, sale_data)
    if not updated:
        raise HTTPException(status_code=404, detail="Sale not found.")
    return RedirectResponse(url="/sales/", status_code=303)

@app.post("/sales/{sale_id}/delete/")
def delete_sale(sale_id: int, db: Session = Depends(get_db)):
    sale = crud.get_sale(db, sale_id)
    if sale:
        crud.delete_sale(db, sale)
        db.commit()
    return RedirectResponse(url="/sales/", status_code=303)

# ---------- Discounts Pages ----------

@app.get("/discounts/")
def list_discounts(request: Request, db: Session = Depends(get_db)):
    discounts = crud.get_discounts(db)
    return templates.TemplateResponse("discounts/list.html", {"request": request, "discounts": discounts})

@app.get("/discounts/create/")
def create_discount_form(request: Request, db: Session = Depends(get_db)):
    products = crud.get_products(db)
    return templates.TemplateResponse("discounts/create.html", {"request": request, "products": products})

@app.post("/discounts/create/")
def create_discount(
    request: Request,
    product_id: int = Form(...),
    begin_date: str = Form(...),
    end_date: str = Form(...),
    discount_percentage: float = Form(...),
    db: Session = Depends(get_db)
):
    discount_data = schemas.DiscountCreate(
        product_id=product_id,
        begin_date=begin_date,
        end_date=end_date,
        discount_percentage=discount_percentage
    )
    crud.create_discount(db, discount_data)
    return RedirectResponse(url="/discounts/", status_code=303)

@app.get("/discounts/{discount_id}/edit/")
def edit_discount_form(discount_id: int, request: Request, db: Session = Depends(get_db)):
    discount = crud.get_discount(db, discount_id)
    if not discount:
        raise HTTPException(status_code=404, detail="Discount not found.")
    products = crud.get_products(db)
    return templates.TemplateResponse("discounts/edit.html", {"request": request, "discount": discount, "products": products})

@app.post("/discounts/{discount_id}/edit/")
def update_discount(
    discount_id: int,
    request: Request,
    product_id: int = Form(...),
    begin_date: str = Form(...),
    end_date: str = Form(...),
    discount_percentage: float = Form(...),
    db: Session = Depends(get_db)
):
    discount_data = schemas.DiscountCreate(
        product_id=product_id,
        begin_date=begin_date,
        end_date=end_date,
        discount_percentage=discount_percentage
    )
    updated = crud.update_discount(db, discount_id, discount_data)
    if not updated:
        raise HTTPException(status_code=404, detail="Discount not found.")
    return RedirectResponse(url="/discounts/", status_code=303)

@app.post("/discounts/{discount_id}/delete/")
def delete_discount(discount_id: int, db: Session = Depends(get_db)):
    discount = crud.get_discount(db, discount_id)
    if discount:
        db.delete(discount)
        db.commit()
    return RedirectResponse(url="/discounts/", status_code=303)

# ---------- Commission Report Page ----------

from sqlalchemy import and_
from datetime import date, timedelta

@app.get("/commission_report/")
def commission_report_form(request: Request):
    return templates.TemplateResponse("commission/report.html", {"request": request, "report": None})

@app.post("/commission_report/")
def generate_commission_report(
    request: Request,
    year: int = Form(...),
    quarter: int = Form(...),
    db: Session = Depends(get_db)
):
    
    report = []
    salespersons = db.query(models.Salesperson).all()

    for sp in salespersons:
        sales_query = db.query(models.Sale).filter(models.Sale.salesperson_id == sp.id)

        if year != 0:
            if quarter != 0:
                # Filter by year + quarter
                quarter_start_month = (quarter - 1) * 3 + 1
                quarter_end_month = quarter_start_month + 2

                quarter_start = date(year, quarter_start_month, 1)
                if quarter_end_month == 12:
                    quarter_end = date(year, 12, 31)
                else:
                    quarter_end = date(year, quarter_end_month + 1, 1) - timedelta(days=1)

                sales_query = sales_query.filter(
                    models.Sale.sales_date >= quarter_start,
                    models.Sale.sales_date <= quarter_end
                )
            else:
                # Filter by year only (all quarters)
                year_start = date(year, 1, 1)
                year_end = date(year, 12, 31)
                sales_query = sales_query.filter(
                    models.Sale.sales_date >= year_start,
                    models.Sale.sales_date <= year_end
                )
        # if year == 0, do not add any date filter, get all sales

        sales = sales_query.all()

        num_sales = len(sales)
        total_sales_amount = 0.0
        total_commission = 0.0

        for sale in sales:
            product = sale.product
            price = product.sale_price

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

    return templates.TemplateResponse("commission/report.html", {"request": request, "report": report, "year": year, "quarter": quarter})
