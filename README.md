BeSpoked Bikes Sales Management App

This is my final full-stack project for my technical interview for Profisee.

Technologies Used:

* FastAPI (Python web framework)
* SQLAlchemy (ORM for SQLite database)
* Jinja2 (HTML template engine)
* SQLite (local relational database)

Features:

* Products CRUD (create, read, update, delete)
* Salespersons CRUD
* Customers CRUD
* Sales CRUD with full inventory tracking
* Discounts CRUD
* Commission Report with filtering by year/quarter/all
* Error handling for out-of-stock products
* Basic styling for clean UI
* Fully separated backend (data layer) and frontend (client web app) within a single monolithic app architecture

Project Structure:
/static/             →       CSS styles

/templates/          →       HTML templates

app.py               →       Frontend client web app

api_test.py          →       Backend testing during development

models.py            →       SQLAlchemy models

crud.py              →       Database access functions

schemas.py           →       Pydantic schemas

database.py          →       DB session + connection

seed_data.py         →       Populate database with demo data

Setup Instructions:

1. Clone the repo:
   
   git clone [https://github.com/HusseinRmaile/bespoked-bikes-sales-tracking.git](https://github.com/HusseinRmaile/bespoked-bikes-sales-tracking.git)

   cd bespoked-bikes-sales-tracking

2. Install dependencies:

   pip install -r requirements.txt

3. Seed the database:

   python seed_data.py

4. Run client web app server (on port 8000):

   uvicorn app:app --reload

5. Access client:

   [http://127.0.0.1:8000/](http://127.0.0.1:8000/)

For Backend API Testing:

1. Run backend web app server (on port 8000):

   uvicorn api_test:app --reload

2. Access Swagger API docs:

   [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

Additional Notes:

* api_test.py was for testing during backend development, it's not needed for the app to run.
* All data resets if you re-run seed_data.py.
* Project has been fully tested with error handling and realistic demo data.