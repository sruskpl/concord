from pydantic import BaseModel, EmailStr, ConfigDict
from datetime import datetime, date
from decimal import Decimal
from models import ExceptionStatus, SessionStatus, AuditAction, UserRole

class UserCreate(BaseModel):
    employee_id: str
    full_name: str
    email: EmailStr
    password: str

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class UserResponse(BaseModel):

    employee_id: str

    full_name: str

    email: str

    role: UserRole

    created_at: datetime

    last_login: datetime | None

    model_config = ConfigDict(
        from_attributes=True
    )

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

class ExceptionCommentCreate(BaseModel):
    comment:str

class ExceptionResponse(BaseModel):

    id: int
    exception_type: str
    severity: str
    status: str
    description: str

    model_config = {
        "from_attributes": True
    }

class ExceptionStatusUpdate(BaseModel):
    status: ExceptionStatus

class SessionStartResponse(BaseModel):
    message: str
    session_id: int
    business_date: date
    status: str

class Config:
    from_attributes = True

class AuditLogResponse(BaseModel):
    id: int
    created_by: str
    action: AuditAction
    description: str
    created_at: datetime
    model_config = ConfigDict(from_attributes = True)  

class SessionResponse(BaseModel):

    id: int

    business_date: date

    status: SessionStatus

    matched_transactions: int

    exception_count: int

    model_config = ConfigDict(from_attributes=True)     