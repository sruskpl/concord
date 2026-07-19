from pydantic import BaseModel, EmailStr
from datetime import datetime, date
from decimal import Decimal

class UserCreate(BaseModel):
    employee_id: str
    full_name: str
    email: EmailStr
    password: str

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class UserResponse(BaseModel):
    id: int
    employee_id: str
    full_name: str
    role: str
    created_at: datetime
    model_config = {
        "from_attributes": True
    }

class Token(BaseModel):
    access_token: str
    token_type: str
    role: str

class TransactionUpload(BaseModel):
    transaction_reference: str
    customer_id: str
    amount: Decimal
    currency: str
    transaction_date: date

class UploadResponse(BaseModel):
    message: str
    valid_rows: int
    invalid_rows: int