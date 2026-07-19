from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from database import get_db
from models import (User, UserRole, Transaction, FileUpload, AuditLog, UploadSource)
from auth import verify_password, create_access_token
from schemas import (UserCreate, UserResponse, UserLogin, Token, UploadResponse, TransactionUpload)
from auth import hash_password
from fastapi import (UploadFile, File, Form)
import csv
from io import StringIO

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://127.0.0.1:5500",
        "http://localhost:5500"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

@app.post("/register", response_model=UserResponse)
def register_user(
    user: UserCreate,
    db: Session = Depends(get_db)
):

    existing_user = db.query(User).filter(
        User.email == user.email
    ).first()

    if existing_user:
        raise HTTPException(
            status_code=400,
            detail="Email already registered."
        )

    hashed_password = hash_password(user.password)

    new_user = User(
        employee_id=user.employee_id,
        full_name=user.full_name,
        email=user.email,
        password_hash=hashed_password,
        role=UserRole.OPERATOR
    )

    db.add(new_user)

    db.commit()

    db.refresh(new_user)

    return new_user

@app.post("/login", response_model=Token)
def login_user(
    user: UserLogin,
    db: Session = Depends(get_db)
):

    db_user = db.query(User).filter(
        User.email == user.email
    ).first()

    if not db_user:
        raise HTTPException(
            status_code=401,
            detail="Invalid email or password."
        )

    if not verify_password(
        user.password,
        db_user.password_hash
    ):
        raise HTTPException(
            status_code=401,
            detail="Invalid email or password."
        )

    access_token = create_access_token(
        {
            "sub": db_user.employee_id,
            "role": db_user.role
        }
    )

    return Token(
        access_token=access_token,
        token_type="bearer",
        role=db_user.role
    )

@app.post("/upload", response_model = UploadResponse)
def upload_file(
    session_id: int = Form(...),
    source: UploadSource = Form(...),
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    if not file.filename.endswith(".csv"):
        raise HTTPException(
            status_code=400,
            detail="Only CSV files are allowed."
        )
contents = file.file.read().decode("utf-8")
csv_reader = csv.DictReader(
StringIO(contents)
)

upload = FileUpload(
    session_id=session_id,
    source=source,
    filename=file.filename,
    valid_rows=valid_records,
    invalid_rows=invalid_records
)

db.add(upload)

db.commit()

db.refresh(upload)

valid_rows = 0
invalid_rows = 0

for row in csv_reader:

    try:

        transaction_data = TransactionUpload(**row)

        new_transaction = Transaction(
            transaction_reference=transaction_data.transaction_reference,
            customer_id=transaction_data.customer_id,
            amount=transaction_data.amount,
            currency=transaction_data.currency,
            transaction_date=transaction_data.transaction_date,
            source=transaction_data.source_system,
            session_id=transaction_data.upload_id
        )

        db.add(new_transaction)

        valid_rows += 1

    except Exception:

        invalid_rows += 1

db.commit()

audit = AuditLog(
    employee_id=get_current_employee_id(),
    action="FILE_UPLOAD",
    description=f"Uploaded {file.filename}"
)

db.add(audit)

db.commit()

return UploadResponse(
    message="Upload Successful",
    valid_rows=valid_rows,
    invalid_rows=invalid_rows
)