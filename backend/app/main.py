from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from . import models, schemas, crud
from .database import engine, SessionLocal
from . import auth

models.Base.metadata.create_all(bind=engine)
app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Customer endpoints
@app.post("/customers/", response_model=schemas.CustomerResponse)
def create_customer(customer: schemas.CustomerCreate, db: Session = Depends(get_db)):
    return crud.create_customer(db, customer)

@app.get("/customers/", response_model=list[schemas.CustomerResponse])
def read_customers(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_customers(db, skip=skip, limit=limit)

@app.get("/customers/{customer_id}", response_model=schemas.CustomerResponse)
def read_customer(customer_id: int, db: Session = Depends(get_db)):
    db_customer = crud.get_customer(db, customer_id)
    if db_customer is None:
        raise HTTPException(status_code=404, detail="Customer not found")
    return db_customer

@app.put("/customers/{customer_id}", response_model=schemas.CustomerResponse)
def update_customer(customer_id: int, customer: schemas.CustomerUpdate, db: Session = Depends(get_db)):
    db_customer = crud.update_customer(db, customer_id, customer)
    if db_customer is None:
        raise HTTPException(status_code=404, detail="Customer not found")
    return db_customer

@app.delete("/customers/{customer_id}")
def delete_customer(customer_id: int, db: Session = Depends(get_db)):
    success = crud.delete_customer(db, customer_id)
    if not success:
        raise HTTPException(status_code=404, detail="Customer not found")
    return {"ok": True}

# Product endpoints
@app.post("/products/", response_model=schemas.ProductResponse)
def create_product(product: schemas.ProductCreate, db: Session = Depends(get_db)):
    return crud.create_product(db, product)

@app.get("/products/", response_model=list[schemas.ProductResponse])
def read_products(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_products(db, skip=skip, limit=limit)

@app.get("/products/{product_id}", response_model=schemas.ProductResponse)
def read_product(product_id: int, db: Session = Depends(get_db)):
    db_product = crud.get_product(db, product_id)
    if db_product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    return db_product

@app.put("/products/{product_id}", response_model=schemas.ProductResponse)
def update_product(product_id: int, product: schemas.ProductUpdate, db: Session = Depends(get_db)):
    db_product = crud.update_product(db, product_id, product)
    if db_product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    return db_product

@app.delete("/products/{product_id}")
def delete_product(product_id: int, db: Session = Depends(get_db)):
    success = crud.delete_product(db, product_id)
    if not success:
        raise HTTPException(status_code=404, detail="Product not found")
    return {"ok": True}

# Order endpoints
@app.post("/customers/{customer_id}/orders/", response_model=schemas.OrderResponse)
def create_order_for_customer(customer_id: int, order: schemas.OrderCreate, db: Session = Depends(get_db)):
    return crud.create_order(db, order, customer_id)

@app.get("/customers/{customer_id}/orders/", response_model=list[schemas.OrderResponse])
def get_orders_for_customer(customer_id: int, db: Session = Depends(get_db)):
    return crud.get_orders(db, customer_id)

@app.put("/orders/{order_id}", response_model=schemas.OrderResponse)
def update_order(order_id: int, order: schemas.OrderUpdate, db: Session = Depends(get_db)):
    db_order = crud.update_order(db, order_id, order)
    if db_order is None:
        raise HTTPException(status_code=404, detail="Order not found")
    return db_order

@app.delete("/orders/{order_id}")
def delete_order(order_id: int, db: Session = Depends(get_db)):
    success = crud.delete_order(db, order_id)
    if not success:
        raise HTTPException(status_code=404, detail="Order not found")
    return {"ok": True}
    return db_customer

@app.delete("/customers/{customer_id}")
def delete_customer(
    customer_id: int,
    db: Session = Depends(get_db),
    current_user: models.Customer = Depends(auth.get_current_user)
):
    success = crud.delete_customer(db, customer_id)
    if not success:
        raise HTTPException(status_code=404, detail="Customer not found")
    return {"ok": True}

@app.post("/customers/{customer_id}/contacts/", response_model=schemas.ContactResponse)
def create_contact_for_customer(
    customer_id: int,
    contact: schemas.ContactCreate,
    db: Session = Depends(get_db),
    current_user: models.Customer = Depends(auth.get_current_user)
):
    return crud.create_contact(db, contact, customer_id)

@app.get("/customers/{customer_id}/contacts/", response_model=list[schemas.ContactResponse])
def get_contacts_for_customer(
    customer_id: int,
    db: Session = Depends(get_db),
    current_user: models.Customer = Depends(auth.get_current_user)
):
    return crud.get_contacts(db, customer_id)

@app.post("/customers/{customer_id}/opportunities/", response_model=schemas.OpportunityResponse)
def create_opportunity_for_customer(
    customer_id: int,
    opportunity: schemas.OpportunityCreate,
    db: Session = Depends(get_db),
    current_user: models.Customer = Depends(auth.get_current_user)
):
    return crud.create_opportunity(db, opportunity, customer_id)

@app.get("/customers/{customer_id}/opportunities/", response_model=list[schemas.OpportunityResponse])
def get_opportunities_for_customer(
    customer_id: int,
    db: Session = Depends(get_db),
    current_user: models.Customer = Depends(auth.get_current_user)
):
    return crud.get_opportunities(db, customer_id)

@app.post("/customers/{customer_id}/notes/", response_model=schemas.NoteResponse)
def create_note_for_customer(
    customer_id: int,
    note: schemas.NoteCreate,
    db: Session = Depends(get_db),
    current_user: models.Customer = Depends(auth.get_current_user)
):
    return crud.create_note(db, note, customer_id)

@app.get("/customers/{customer_id}/notes/", response_model=list[schemas.NoteResponse])
def get_notes_for_customer(
    customer_id: int,
    db: Session = Depends(get_db),
    current_user: models.Customer = Depends(auth.get_current_user)
):
    return crud.get_notes(db, customer_id)
