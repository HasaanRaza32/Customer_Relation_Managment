# Pydantic schemas for the backend

from pydantic import BaseModel, EmailStr, Field, validator
from typing import List, Optional
import datetime
import bleach

# --- Base Schemas ---

class ContactBase(BaseModel):
    name: str = Field(..., min_length=2, max_length=50)
    email: Optional[EmailStr] = None
    phone: Optional[str] = Field(None, min_length=7, max_length=20)

    @validator("name", pre=True)
    def sanitize_name(cls, v):
        return bleach.clean(v, strip=True)

    @validator("phone")
    def validate_phone(cls, v):
        if v and not v.replace("+", "").replace("-", "").replace(" ", "").isdigit():
            raise ValueError("Phone must contain only numbers, spaces, + or -")
        return v

# --- Create Schemas ---

class ContactCreate(ContactBase):
    pass

# --- Update Schemas ---

class UserUpdate(BaseModel):
    """ Schema for updating user profile information. All fields are optional. """
    username: Optional[str] = None
    email: Optional[EmailStr] = None
    password: Optional[str] = None

# --- Response Schemas ---

class ContactResponse(ContactBase):
    id: int
    class Config:
        from_attributes = True

class OpportunityBase(BaseModel):
    name: str = Field(..., min_length=2, max_length=100)
    value: Optional[float] = Field(None, ge=0)
    stage: Optional[str] = Field(None, max_length=50)
    close_date: Optional[datetime.datetime] = None

    @validator("name", "stage", pre=True)
    def sanitize_text(cls, v):
        return bleach.clean(v, strip=True) if v else v

class OpportunityCreate(OpportunityBase):
    pass

class OpportunityResponse(OpportunityBase):
    id: int
    class Config:
        from_attributes = True

class NoteBase(BaseModel):
    content: str = Field(..., min_length=1, max_length=1000)

    @validator("content", pre=True)
    def sanitize_content(cls, v):
        return bleach.clean(v, strip=True)

class NoteCreate(NoteBase):
    pass

class NoteResponse(NoteBase):
    id: int
    timestamp: datetime.datetime
    class Config:
        from_attributes = True

class ProductBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    price: int

class ProductCreate(ProductBase):
    pass

class ProductUpdate(ProductBase):
    pass

class ProductResponse(ProductBase):
    id: int
    class Config:
        from_attributes = True

class OrderBase(BaseModel):
    item: str = Field(..., min_length=1, max_length=100)
    product_id: Optional[int] = None

class OrderCreate(OrderBase):
    pass

class OrderUpdate(OrderBase):
    pass

class OrderResponse(OrderBase):
    id: int
    customer_id: int
    class Config:
        from_attributes = True

class CustomerBase(BaseModel):
    name: str = Field(..., min_length=2, max_length=100)
    email: EmailStr

class CustomerCreate(CustomerBase):
    pass

class CustomerUpdate(CustomerBase):
    pass

class CustomerResponse(CustomerBase):
    id: int
    orders: List[OrderResponse] = []
    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str
    token_type: str
