"""
This script populates the database with test data.
All data is lowercase for consistency.
"""

from datetime import date
from sqlalchemy.orm import Session
from database import SessionLocal
import models

def seed_database():
    db: Session = SessionLocal()

    # Clear existing data (order matters due to foreign key constraints)
    db.query(models.Sale).delete()
    db.query(models.Discount).delete()
    db.query(models.Customer).delete()
    db.query(models.Salesperson).delete()
    db.query(models.Product).delete()
    db.commit()

    # Products
    products = [
        models.Product(name="speedster 3000", manufacturer="cyclepro", style="road", purchase_price=500.0, sale_price=750.0, qty_on_hand=2, commission_percentage=10.0),
        models.Product(name="mountain king", manufacturer="trailblazer", style="mountain", purchase_price=600.0, sale_price=900.0, qty_on_hand=5, commission_percentage=12.5),
        models.Product(name="city cruiser", manufacturer="urbanrider", style="hybrid", purchase_price=300.0, sale_price=500.0, qty_on_hand=8, commission_percentage=8.0),
        models.Product(name="gravel master", manufacturer="allterrain", style="gravel", purchase_price=550.0, sale_price=800.0, qty_on_hand=4, commission_percentage=11.0),
        models.Product(name="kids fun rider", manufacturer="tinybikes", style="kids", purchase_price=200.0, sale_price=350.0, qty_on_hand=7, commission_percentage=9.0),
    ]
    db.add_all(products)

    # Salespersons
    salespersons = [
        models.Salesperson(first_name="john", last_name="doe", address="123 main st", phone="555-1234", start_date=date(2020, 5, 1), termination_date=None, manager="jane smith"),
        models.Salesperson(first_name="alice", last_name="johnson", address="456 oak ave", phone="555-5678", start_date=date(2019, 3, 15), termination_date=None, manager="jane smith"),
        models.Salesperson(first_name="mike", last_name="carter", address="789 elm st", phone="555-9876", start_date=date(2021, 7, 10), termination_date=None, manager="jane smith"),
    ]
    db.add_all(salespersons)

    # Customers
    customers = [
        models.Customer(first_name="tom", last_name="anderson", address="789 pine rd", phone="555-8765", start_date=date(2023, 1, 10)),
        models.Customer(first_name="sara", last_name="miller", address="321 maple ln", phone="555-4321", start_date=date(2023, 2, 20)),
        models.Customer(first_name="david", last_name="lee", address="555 cedar blvd", phone="555-6543", start_date=date(2023, 3, 5)),
    ]
    db.add_all(customers)

    db.commit()

    # Sales (spread across quarters)
    sales = [
        # john
        models.Sale(product_id=1, salesperson_id=1, customer_id=1, sales_date=date(2024, 1, 15)),
        models.Sale(product_id=2, salesperson_id=1, customer_id=2, sales_date=date(2024, 4, 10)),
        models.Sale(product_id=3, salesperson_id=1, customer_id=3, sales_date=date(2024, 7, 20)),
        # alice
        models.Sale(product_id=4, salesperson_id=2, customer_id=2, sales_date=date(2024, 3, 22)),
        models.Sale(product_id=1, salesperson_id=2, customer_id=3, sales_date=date(2024, 6, 18)),
        models.Sale(product_id=2, salesperson_id=2, customer_id=1, sales_date=date(2024, 9, 5)),
        # mike
        models.Sale(product_id=3, salesperson_id=3, customer_id=3, sales_date=date(2024, 2, 14)),
        models.Sale(product_id=4, salesperson_id=3, customer_id=1, sales_date=date(2024, 5, 30)),
        models.Sale(product_id=2, salesperson_id=3, customer_id=2, sales_date=date(2024, 10, 8)),
    ]
    db.add_all(sales)

    # Discounts (3 overlap sales, 2 don't)
    discounts = [
        models.Discount(product_id=1, begin_date=date(2024, 1, 1), end_date=date(2024, 1, 31), discount_percentage=15.0),  # overlaps sale
        models.Discount(product_id=2, begin_date=date(2024, 9, 1), end_date=date(2024, 9, 30), discount_percentage=20.0),  # overlaps sale
        models.Discount(product_id=4, begin_date=date(2024, 5, 15), end_date=date(2024, 6, 15), discount_percentage=10.0),  # overlaps sale
        models.Discount(product_id=5, begin_date=date(2024, 7, 1), end_date=date(2024, 7, 31), discount_percentage=25.0),  # no sale
        models.Discount(product_id=5, begin_date=date(2024, 11, 1), end_date=date(2024, 11, 30), discount_percentage=12.5), # no sale
    ]
    db.add_all(discounts)

    db.commit()
    db.close()

    print("Database seeded successfully.")

if __name__ == "__main__":
    seed_database()
