from sqlalchemy.orm import Session
from . import models, schemas

def create_customer(db: Session, customer: schemas.CustomerCreate):
    db_customer = models.Customer(**customer.dict())
    db.add(db_customer)
    db.commit()
    db.refresh(db_customer)
    return db_customer

def get_customer(db: Session, customer_id: int):
    return db.query(models.Customer).filter(models.Customer.id == customer_id).first()

def get_customers(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Customer).offset(skip).limit(limit).all()

def update_customer(db: Session, customer_id: int, customer: schemas.CustomerUpdate):
    db_customer = get_customer(db, customer_id)
    if not db_customer:
        return None
    for key, value in customer.dict().items():
        setattr(db_customer, key, value)
    db.commit()
    db.refresh(db_customer)
    return db_customer

def delete_customer(db: Session, customer_id: int):
    db_customer = get_customer(db, customer_id)
    if not db_customer:
        return False
    db.delete(db_customer)
    db.commit()
    return True

def create_product(db: Session, product: schemas.ProductCreate):
    db_product = models.Product(**product.dict())
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product

def get_product(db: Session, product_id: int):
    return db.query(models.Product).filter(models.Product.id == product_id).first()

def get_products(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Product).offset(skip).limit(limit).all()

def update_product(db: Session, product_id: int, product: schemas.ProductUpdate):
    db_product = get_product(db, product_id)
    if not db_product:
        return None
    for key, value in product.dict().items():
        setattr(db_product, key, value)
    db.commit()
    db.refresh(db_product)
    return db_product

def delete_product(db: Session, product_id: int):
    db_product = get_product(db, product_id)
    if not db_product:
        return False
    db.delete(db_product)
    db.commit()
    return True

def create_order(db: Session, order: schemas.OrderCreate, customer_id: int):
    db_order = models.Order(**order.dict(), customer_id=customer_id)
    db.add(db_order)
    db.commit()
    db.refresh(db_order)
    return db_order

def get_orders(db: Session, customer_id: int):
    return db.query(models.Order).filter(models.Order.customer_id == customer_id).all()

def update_order(db: Session, order_id: int, order: schemas.OrderUpdate):
    db_order = db.query(models.Order).filter(models.Order.id == order_id).first()
    if not db_order:
        return None
    for key, value in order.dict().items():
        setattr(db_order, key, value)
    db.commit()
    db.refresh(db_order)
    return db_order

def delete_order(db: Session, order_id: int):
    db_order = db.query(models.Order).filter(models.Order.id == order_id).first()
    if not db_order:
        return False
    db.delete(db_order)
    db.commit()
    return True

# --- Contact CRUD ---
def create_contact(db: Session, contact: schemas.ContactCreate, customer_id: int):
    db_contact = models.Contact(**contact.dict(), customer_id=customer_id)
    db.add(db_contact)
    db.commit()
    db.refresh(db_contact)
    return db_contact

def get_contacts(db: Session, customer_id: int):
    return db.query(models.Contact).filter(models.Contact.customer_id == customer_id).all()

# --- Opportunity CRUD ---
def create_opportunity(db: Session, opportunity: schemas.OpportunityCreate, customer_id: int):
    db_opp = models.Opportunity(**opportunity.dict(), customer_id=customer_id)
    db.add(db_opp)
    db.commit()
    db.refresh(db_opp)
    return db_opp

def get_opportunities(db: Session, customer_id: int):
    return db.query(models.Opportunity).filter(models.Opportunity.customer_id == customer_id).all()

# --- Note CRUD ---
def create_note(db: Session, note: schemas.NoteCreate, customer_id: int):
    db_note = models.Note(**note.dict(), customer_id=customer_id)
    db.add(db_note)
    db.commit()
    db.refresh(db_note)
    return db_note

def get_notes(db: Session, customer_id: int):
    return db.query(models.Note).filter(models.Note.customer_id == customer_id).all()

# --- User CRUD ---
def create_user(db: Session, user: schemas.OrderCreate):
    hashed_password = get_password_hash(user.password)
    db_user = models.User(username=user.username, email=user.email, hashed_password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def get_customer_by_name(db: Session, name: str):
    return db.query(models.Customer).filter(models.Customer.name == name).first()

def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()

def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.User).offset(skip).limit(limit).all()

def update_user(db: Session, user_id: int, user_update: schemas.UserUpdate):
    """Updates a user's profile information."""
    db_user = get_user(db, user_id)
    if not db_user:
        return None

    if user_update.username:
        db_user.username = user_update.username
    if user_update.email:
        db_user.email = user_update.email
    if user_update.password:
        db_user.hashed_password = get_password_hash(user_update.password)
    
    db.commit()
    db.refresh(db_user)
    return db_user

def delete_user(db: Session, user_id: int):
    """Deletes a user and all their associated data via cascading deletes."""
    db_user = db.query(models.User).filter(models.User.id == user_id).first()
    if not db_user:
        return False
    
    db.delete(db_user)
    db.commit()
    return True

# --- Friendship and Friend Request Functions ---

def get_friends(db: Session, user_id: int):
    """Gets a list of a user's friends."""
    friendships = db.query(models.Friendship).filter(models.Friendship.user_id == user_id).all()
    friend_ids = [f.friend_id for f in friendships]
    return db.query(models.User).filter(models.User.id.in_(friend_ids)).all()

def unfriend(db: Session, user_id: int, friend_id: int):
    """Removes a friendship between two users (bidirectional)."""
    # Delete friendship from user to friend
    friendship1 = db.query(models.Friendship).filter(
        and_(models.Friendship.user_id == user_id, models.Friendship.friend_id == friend_id)
    ).first()
    
    # Delete friendship from friend to user
    friendship2 = db.query(models.Friendship).filter(
        and_(models.Friendship.user_id == friend_id, models.Friendship.friend_id == user_id)
    ).first()

    if not friendship1 or not friendship2:
        return False # Friendship doesn't exist

    db.delete(friendship1)
    db.delete(friendship2)
    db.commit()
    return True

def send_friend_request(db: Session, sender_id: int, receiver_id: int):
    existing = db.query(models.FriendRequest).filter(
        or_(
            and_(models.FriendRequest.sender_id == sender_id, models.FriendRequest.receiver_id == receiver_id),
            and_(models.FriendRequest.sender_id == receiver_id, models.FriendRequest.receiver_id == sender_id)
        )
    ).first()
    if existing:
        return None # Request already exists or has been handled
    fr = models.FriendRequest(sender_id=sender_id, receiver_id=receiver_id)
    db.add(fr)
    db.commit()
    db.refresh(fr)
    return fr

def get_friend_requests(db: Session, user_id: int):
    return db.query(models.FriendRequest).filter(models.FriendRequest.receiver_id == user_id, models.FriendRequest.status == "pending").all()

def get_sent_friend_requests(db: Session, user_id: int):
    return db.query(models.FriendRequest).filter(models.FriendRequest.sender_id == user_id, models.FriendRequest.status == "pending").all()

def respond_friend_request(db: Session, request_id: int, accept: bool):
    fr = db.query(models.FriendRequest).filter(models.FriendRequest.id == request_id).first()
    if not fr or fr.status != "pending":
        return None
    if accept:
        fr.status = "accepted"
        # Create friendships both ways
        db.add(models.Friendship(user_id=fr.sender_id, friend_id=fr.receiver_id))
        db.add(models.Friendship(user_id=fr.receiver_id, friend_id=fr.sender_id))
    else:
        fr.status = "rejected"
    db.commit()
    db.refresh(fr)
    return fr
