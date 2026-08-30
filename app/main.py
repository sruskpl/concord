from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from database import get_db, Base, engine
from models import (User, UserRole, Transaction, FileUpload, AuditLog, SourceType, UploadStatus, TransactionStatus, AuditAction, ReconciliationException, ExceptionType, ReconciliationSession, ExceptionStatus, ExceptionComment, SessionStatus, ExceptionSeverity)
from auth import (hash_password, verify_password, create_access_token)
from schemas import (UserCreate, UserResponse, UserLogin, Token, UploadResponse, TransactionUpload, ExceptionCommentCreate, ExceptionStatusUpdate, SessionStartResponse, AuditLogResponse)
from fastapi import (UploadFile, File, Form)
import csv
from datetime import datetime, UTC
from io import StringIO
from sqlalchemy import func
from auth import get_current_user

app = FastAPI()

Base.metadata.create_all(bind=engine)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/me")
def get_current_logged_in_user(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    user = (
        db.query(User)
        .filter(User.employee_id == current_user["employee_id"])
        .first()
    )

    return {
        "employee_id": user.employee_id,
        "full_name": user.full_name,
        "role": user.role.value
    }

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
        employee_id=user.employee_id.upper(),
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

    db_user.last_login = datetime.now()

    db.commit()

    db.refresh(db_user)

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
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    current_session = (
    db.query(ReconciliationSession)
    .filter(
        ReconciliationSession.status != SessionStatus.COMPLETED
    )
    .order_by(
        ReconciliationSession.created_at.desc()
    )
    .first()
)

    if current_session is None:
        raise HTTPException(
        status_code=400,
        detail="Please start a session first."
    )
    
    if not file.filename.endswith(".csv"):
        raise HTTPException(
            status_code=400,
            detail="Only CSV files are allowed."
        )

    filename = file.filename.lower()
    
    if "bank" in filename:
        source = SourceType.BANK

    elif "merchant" in filename:
        source = SourceType.MERCHANT
    
    elif "card" in filename:
        source = SourceType.CARD_NETWORK
    
    elif "ledger" in filename:
        source = SourceType.INTERNAL_LEDGER
    
    else:
       raise HTTPException(
            status_code=400,
            detail="Unknown source."
        )

    contents = file.file.read().decode("utf-8")
    csv_reader = csv.DictReader(
    StringIO(contents)
    )

    valid_rows = 0
    invalid_rows = 0

    transactions: list[TransactionUpload] = []

    for row in csv_reader:

        try:

            transaction_data = TransactionUpload(**row)

            transactions.append(transaction_data)

            valid_rows += 1

        except Exception as error:

            print("CSV validation error:", error)

            invalid_rows += 1

    
    if invalid_rows == 0:
        upload_status = UploadStatus.SUCCESS

    elif valid_rows == 0:
        upload_status = UploadStatus.FAILED

    else:
        upload_status = UploadStatus.PARTIAL

    upload = FileUpload(
        session_id=current_session.id,
        source=source,
        filename=file.filename,
        valid_records=valid_rows,
        invalid_records=invalid_rows,
        status=upload_status
    )
    db.add(upload)

    db.commit()

    db.refresh(upload)

    for transaction_data in transactions:
        new_transaction = Transaction(
            upload_id=upload.id,
            transaction_reference=transaction_data.transaction_reference,
            customer_id=transaction_data.customer_id,
            amount=transaction_data.amount,
            currency=transaction_data.currency,
            transaction_date=transaction_data.transaction_date,
            source=source,
            transaction_status=TransactionStatus.PENDING
        )

        db.add(new_transaction)
    db.commit()

    audit = AuditLog(
    session_id=upload.session_id,
    created_by=current_user["employee_id"],
    description=f"Uploaded file {file.filename}",
    action=AuditAction.UPLOAD_FILE
)

    db.add(audit)

    db.commit()

    uploaded_sources = (
        db.query(FileUpload.source)
        .filter(FileUpload.session_id == current_session.id)
        .distinct()
        .all()
    )

    uploaded_sources = {source[0] for source in uploaded_sources}

    required_sources = set(SourceType)

    if uploaded_sources == required_sources:

        session = (
            db.query(ReconciliationSession)
            .filter(ReconciliationSession.id == current_session.id)
            .first()
        )

        session.status = SessionStatus.READY

        db.commit()

        db.refresh(session)

    if upload_status == UploadStatus.SUCCESS:
        message = "Upload Successful"

    elif upload_status == UploadStatus.PARTIAL:
        message = "Upload Completed with Validation Errors"

    else:
        message = "Upload Failed"

    return UploadResponse(
        message=message,
        valid_rows=valid_rows,
        invalid_rows=invalid_rows
    )

@app.post("/reconcile/{session_id}")
def reconcile(
    session_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    transactions = (
        db.query(Transaction)
        .join(FileUpload)
        .filter(
            FileUpload.session_id == session_id
        )
        .all()
    )

    session = (
        db.query(ReconciliationSession)
        .filter(
            ReconciliationSession.id == session_id
        )
        .first()
    )

    if session is None:
        raise HTTPException(
            status_code=404,
            detail="Session not found"
        )

    # Group transactions by transaction reference

    grouped_transactions = {}

    for transaction in transactions:

        reference = transaction.transaction_reference

        if reference not in grouped_transactions:

            grouped_transactions[reference] = []

        grouped_transactions[reference].append(
            transaction
        )

    total_matches = 0
    total_exceptions = 0

    # All four sources that should be present

    required_sources = {
        SourceType.BANK,
        SourceType.MERCHANT,
        SourceType.CARD_NETWORK,
        SourceType.INTERNAL_LEDGER
    }

    # Check every transaction reference

    for reference, transaction_group in grouped_transactions.items():

        # --------------------------------------------------
        # 1. CHECK FOR MISSING AND DUPLICATE RECORDS
        # --------------------------------------------------

        source_counts = {}

        for transaction in transaction_group:

            source = transaction.source

            if source not in source_counts:

                source_counts[source] = 0

            source_counts[source] += 1

        missing_sources = (
            required_sources
            - set(source_counts.keys())
        )

        duplicate_sources = [

            source

            for source, count
            in source_counts.items()

            if count > 1
        ]

        # --------------------------------------------------
        # 2. CHECK AMOUNT, CURRENCY AND DATE
        # --------------------------------------------------

        amounts = {
            transaction.amount
            for transaction in transaction_group
        }

        currencies = {
            transaction.currency
            for transaction in transaction_group
        }

        dates = {
            transaction.transaction_date
            for transaction in transaction_group
        }

        has_exception = False

        # --------------------------------------------------
        # 3. MARK TRANSACTIONS AS EXCEPTION IF REQUIRED
        # --------------------------------------------------

        if (
            missing_sources
            or duplicate_sources
            or len(amounts) > 1
            or len(currencies) > 1
            or len(dates) > 1
        ):

            has_exception = True

            for transaction in transaction_group:

                transaction.transaction_status = (
                    TransactionStatus.EXCEPTION
                )

        else:

            for transaction in transaction_group:

                transaction.transaction_status = (
                    TransactionStatus.MATCHED
                )

            total_matches += 1

        # --------------------------------------------------
        # 4. CREATE MISSING RECORD EXCEPTIONS
        # --------------------------------------------------

        representative_transaction = (
            transaction_group[0]
        )

        for source in missing_sources:

            db.add(

                ReconciliationException(

                    transaction_id=
                        representative_transaction.id,

                    exception_type=
                        ExceptionType.MISSING_RECORD,

                    description=
                        f"Missing {source.value} record.",

                    severity=
                        ExceptionSeverity.HIGH
                )
            )

            total_exceptions += 1

        # --------------------------------------------------
        # 5. CREATE DUPLICATE RECORD EXCEPTIONS
        # --------------------------------------------------

        for source in duplicate_sources:

            db.add(

                ReconciliationException(

                    transaction_id=
                        representative_transaction.id,

                    exception_type=
                        ExceptionType.DUPLICATE_RECORD,

                    description=
                        f"Duplicate {source.value} record.",

                    severity=
                        ExceptionSeverity.HIGH
                )
            )

            total_exceptions += 1

        # --------------------------------------------------
        # 6. CREATE AMOUNT MISMATCH EXCEPTION
        # --------------------------------------------------

        if len(amounts) > 1:

            db.add(

                ReconciliationException(

                    transaction_id=
                        representative_transaction.id,

                    exception_type=
                        ExceptionType.AMOUNT_MISMATCH,

                    description=
                        "Amount mismatch across sources.",

                    severity=
                        ExceptionSeverity.MEDIUM
                )
            )

            total_exceptions += 1

        # --------------------------------------------------
        # 7. CREATE CURRENCY MISMATCH EXCEPTION
        # --------------------------------------------------

        if len(currencies) > 1:

            db.add(

                ReconciliationException(

                    transaction_id=
                        representative_transaction.id,

                    exception_type=
                        ExceptionType.CURRENCY_MISMATCH,

                    description=
                        "Currency mismatch across sources.",

                    severity=
                        ExceptionSeverity.MEDIUM
                )
            )

            total_exceptions += 1

        # --------------------------------------------------
        # 8. CREATE DATE MISMATCH EXCEPTION
        # --------------------------------------------------

        if len(dates) > 1:

            db.add(

                ReconciliationException(

                    transaction_id=
                        representative_transaction.id,

                    exception_type=
                        ExceptionType.DATE_MISMATCH,

                    description=
                        "Date mismatch across sources.",

                    severity=
                        ExceptionSeverity.LOW
                )
            )

            total_exceptions += 1

    # --------------------------------------------------
    # 9. UPDATE RECONCILIATION SESSION
    # --------------------------------------------------

    session.matched_transactions = total_matches

    session.exception_count = total_exceptions

    session.status = SessionStatus.COMPLETED

    # --------------------------------------------------
    # 10. CREATE AUDIT LOG
    # --------------------------------------------------

    audit = AuditLog(

        session_id=session_id,

        created_by=current_user["employee_id"],

        action=AuditAction.RUN_RECONCILIATION,

        description="Reconciliation completed."

    )

    db.add(audit)

    # --------------------------------------------------
    # 11. SAVE EVERYTHING
    # --------------------------------------------------

    db.commit()

    return {

        "matched_transactions":
            total_matches,

        "exception_transactions":
            total_exceptions

    }

@app.post(
    "/sessions/start",
    response_model=SessionStartResponse
)
def start_session(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    today = datetime.now(UTC).date()

    existing_session = (
        db.query(ReconciliationSession)
        .filter(
            ReconciliationSession.business_date == today,
            ReconciliationSession.status != SessionStatus.COMPLETED
        )
        .first()
    )

    if existing_session:
        return {
        "message": "Today's session already exists.",
        "session_id": existing_session.id,
        "business_date": existing_session.business_date,
        "status": existing_session.status.value
    }

    new_session = ReconciliationSession(
        business_date=today,
        created_by=current_user["employee_id"],
        status=SessionStatus.UPLOADING
    )

    db.add(new_session)
    db.commit()
    db.refresh(new_session)

    audit = AuditLog(
    session_id=new_session.id,
    created_by=current_user["employee_id"],
    action=AuditAction.CREATE_SESSION,
    description="Started reconciliation session."
)

    db.add(audit)
    db.commit()

    return {
    "message": "Session started successfully.",
    "session_id": new_session.id,
    "business_date": new_session.business_date,
    "status": new_session.status.value
    }

@app.get("/sessions")
def get_sessions(db: Session = Depends(get_db)):

    sessions = (
        db.query(ReconciliationSession)
        .order_by(ReconciliationSession.id.desc())
        .all()
    )

    return sessions

@app.post("/uploads/validate")
def validate_upload(
    session_id: int = Form(...),
    source: SourceType = Form(...),
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    session = (
        db.query(ReconciliationSession)
        .filter(ReconciliationSession.id == session_id)
        .first()
    )

    if session is None:
        raise HTTPException(
            status_code=404,
            detail="Session not found."
        )

    if session.status == SessionStatus.COMPLETED:
        raise HTTPException(
        status_code=400,
        detail="This reconciliation session is already completed."
        )

    existing_upload = (
        db.query(FileUpload)
        .filter(
            FileUpload.session_id == session_id,
            FileUpload.source == source
        )
        .first()
    )

    if existing_upload:
        raise HTTPException(
            status_code=400,
            detail=f"{source.value} file already uploaded."
        )

    if not file.filename.endswith(".csv"):
        raise HTTPException(
            status_code=400,
            detail="Only CSV files are allowed."
        )

    contents = file.file.read().decode("utf-8")

    reader = csv.DictReader(StringIO(contents))

    valid_rows = 0
    invalid_rows = 0

    validated_transactions = []

    for row in reader:

        try:

            transaction = TransactionUpload(**row)

            validated_transactions.append(transaction)

            valid_rows += 1

        except Exception as error:

            print("CSV validation error:", error)

            invalid_rows += 1

    if invalid_rows == 0:
        upload_status = UploadStatus.SUCCESS

    elif valid_rows == 0:
        upload_status = UploadStatus.FAILED

    else:
        upload_status = UploadStatus.PARTIAL

    upload = FileUpload(
        session_id=session_id,
        source=source,
        filename=file.filename,
        valid_records=valid_rows,
        invalid_records=invalid_rows,
        status=upload_status
    )

    db.add(upload)
    db.commit()
    db.refresh(upload)

    for transaction in validated_transactions:

        db.add(
            Transaction(
                upload_id=upload.id,
                transaction_reference=transaction.transaction_reference,
                customer_id=transaction.customer_id,
                amount=transaction.amount,
                currency=transaction.currency,
                transaction_date=transaction.transaction_date,
                source=source,
                transaction_status=TransactionStatus.PENDING
            )
        )

    db.commit()

    audit = AuditLog(
        session_id=session_id,
        created_by=current_user.employee_id,
        action=AuditAction.UPLOAD_FILE,
        description=f"{source.value} uploaded."
    )

    db.add(audit)
    db.commit()

    return {
        "message": "Upload validated successfully.",
        "upload_status": upload_status,
        "valid_rows": valid_rows,
        "invalid_rows": invalid_rows,
        "upload_id": upload.id
    }

@app.get("/dashboard/current")
def get_dashboard(
    db: Session = Depends(get_db)
):
    today = datetime.now(UTC).date()

    total_sessions = db.query(ReconciliationSession).count()

    todays_sessions = (
        db.query(ReconciliationSession)
        .filter(
            ReconciliationSession.business_date == today
        )
        .count()
    )

    current_session = (
    db.query(ReconciliationSession)
    .filter(
        ReconciliationSession.business_date == today
    )
    .order_by(ReconciliationSession.id.desc())
    .first()
    )

    if current_session is None:

        return {

            "session_id": None,
            "business_date": today,
            "todays_sessions": todays_sessions,
            "total_sessions": total_sessions,
            "current_session_status": "",
            "uploaded_sources": [],
            "missing_sources": [],
            "matched_transactions": 0,
            "exception_transactions": 0,
            "average_resolution_time": 0

        }

    total_sessions = (
    db.query(ReconciliationSession)
      .count()
    )

    uploaded_sources = (
    db.query(FileUpload.source)
      .filter(FileUpload.session_id == current_session.id)
      .distinct()
      .all()
    )

    uploaded_sources = [
    source[0].value
    for source in uploaded_sources
    ]

    all_sources = list(SourceType)

    missing_sources = [
    source.value
    for source in all_sources
    if source.value not in uploaded_sources
    ]

    matched_transactions = (
    db.query(Transaction.transaction_reference)
    .join(
        FileUpload,
        Transaction.upload_id == FileUpload.id
    )
    .filter(
        FileUpload.session_id == current_session.id,
        Transaction.transaction_status == TransactionStatus.MATCHED
    )
    .distinct()
    .count()
    )

    exception_transactions = (
    db.query(Transaction.transaction_reference)
    .join(
        FileUpload,
        Transaction.upload_id == FileUpload.id
    )
    .filter(
        FileUpload.session_id == current_session.id,
        Transaction.transaction_status == TransactionStatus.EXCEPTION
    )
    .distinct()
    .count()
    )

    pending_review = (
    db.query(Transaction.transaction_reference)
    .join(ReconciliationException,
          ReconciliationException.transaction_id == Transaction.id)
    .join(FileUpload,
          Transaction.upload_id == FileUpload.id)
    .filter(
        FileUpload.session_id == current_session.id,
        ReconciliationException.status == ExceptionStatus.OPEN
    )
    .distinct()
    .count()
    )
    
    resolved_exceptions = (

    db.query(ReconciliationException)

    .join(Transaction)

    .join(FileUpload)

    .filter(
        FileUpload.session_id == current_session.id,
        ReconciliationException.status == ExceptionStatus.RESOLVED,
        ReconciliationException.resolved_at.isnot(None),
        ReconciliationException.review_started_at.isnot(None)
    )

    .all()
    )

    average_resolution_time = 0

    if resolved_exceptions:

        total_minutes = 0

        for exception in resolved_exceptions:

            total_minutes += (
                exception.resolved_at -
                exception.review_started_at
            ).total_seconds() / 60

        average_resolution_time = round(
            total_minutes / len(resolved_exceptions),
            2
        )

    return {
    "session_id": current_session.id,
    "business_date": current_session.business_date,
    "todays_sessions": todays_sessions,
    "total_sessions": total_sessions,
    "current_session_status": current_session.status.value,
    "can_start_session":
        current_session.status == SessionStatus.COMPLETED,
    "uploaded_sources": uploaded_sources,
    "missing_sources": missing_sources,
    "matched_transactions": matched_transactions,
    "exception_transactions": exception_transactions,
    "average_resolution_time": average_resolution_time,
    "pending_review": pending_review,
    }

@app.get("/summary/{session_id}")
def get_reconciliation_summary(
    session_id: int,
    db: Session = Depends(get_db)
):

    session = (
    db.query(ReconciliationSession)
    .filter(ReconciliationSession.id == session_id)
    .first()
)

    if session is None:
        raise HTTPException(
            status_code=404,
            detail="Session not found."
        )

    total_transactions = (
        db.query(Transaction)
        .join(FileUpload)
        .filter(FileUpload.session_id == session_id)
        .count()
    )

    matched_transactions = (
    db.query(Transaction)
    .join(FileUpload)
    .filter(
        FileUpload.session_id == session_id,
        Transaction.transaction_status == TransactionStatus.MATCHED
    )
    .count()
)

    exception_transactions = (
    db.query(Transaction)
    .join(FileUpload)
    .filter(
        FileUpload.session_id == session_id,
        Transaction.transaction_status == TransactionStatus.EXCEPTION
    )
    .count()
)

    pending_transactions = (
        db.query(Transaction)
        .join(FileUpload)
        .filter(
            FileUpload.session_id == session_id,
            Transaction.transaction_status == TransactionStatus.PENDING
        )
        .count()
    )

    session.status = SessionStatus.COMPLETED
    session.completed_at = datetime.now()
    
    db.commit()

    return {
        "business_date": session.business_date,
        "session_status": session.status,
        "total_transactions": total_transactions,
        "matched_transactions": matched_transactions,
        "exception_transactions": exception_transactions,
        "pending_review": pending_transactions
    }

@app.get("/exceptions/session-info")
def latest_exception_session(
    db: Session = Depends(get_db)
):

    latest_session = (

        db.query(ReconciliationSession)

        .filter(
            ReconciliationSession.status ==
            SessionStatus.COMPLETED
        )

        .order_by(
            ReconciliationSession.id.desc()
        )

        .first()

    )

    if latest_session is None:

        return {
            "session_id": None
        }

    return {

        "session_id": latest_session.id

    }

@app.get("/exceptions/session/{session_id}")
def get_session_exceptions(
    session_id: int,
    db: Session = Depends(get_db)
):

    exceptions = (

        db.query(ReconciliationException)

        .join(Transaction)

        .join(FileUpload)

        .filter(
            FileUpload.session_id == session_id
        )

        .all()

    )

    return [

        {
            "id": exception.id,
            "exception_type": exception.exception_type,
            "status": exception.status,
            "severity": exception.severity,
            "description": exception.description
        }

        for exception in exceptions

    ]

@app.get("/exceptions/{id}")
def get_exception(
    id: int,
    db: Session = Depends(get_db)
):

    exception = (

        db.query(ReconciliationException)

        .filter(
            ReconciliationException.id == id
        )

        .first()

    )

    if exception is None:

        raise HTTPException(
            status_code=404,
            detail="Exception not found."
        )

    if (
    exception.status == ExceptionStatus.OPEN
    and exception.review_started_at is None
    ):

        exception.status = ExceptionStatus.UNDER_REVIEW
        exception.review_started_at = datetime.now()

        db.commit()
        db.refresh(exception)

    transaction = (

        db.query(Transaction)

        .filter(
            Transaction.id == exception.transaction_id
        )

        .first()

    )

    related_transactions = (

    db.query(Transaction)

    .join(FileUpload)

    .filter(

        FileUpload.session_id == transaction.upload.session_id,

        Transaction.transaction_reference == transaction.transaction_reference

    )

    .all()

    )

    comments = (

        db.query(ExceptionComment)

        .filter(
            ExceptionComment.exception_id == id
        )

        .all()

    )

    return {

        "exception_id": exception.id,
        "exception_type": exception.exception_type,
        "description": exception.description,
        "severity": exception.severity,
        "status": exception.status,
        "transaction": transaction,
        "comments": comments,
        "related_transactions": [
        {
        "source": transaction.source,
        "amount": float(transaction.amount),
        "currency": transaction.currency,
        "date": transaction.transaction_date,
        "status": transaction.transaction_status
        }
        for transaction in related_transactions
        ],

    }

@app.post("/exceptions/{id}/comments")
def add_comment(
    id:int,
    comment_data:ExceptionCommentCreate,
    db:Session = Depends(get_db),
    current_user:User=Depends(get_current_user)
):

    exception = (
        db.query(ReconciliationException)
        .filter(
            ReconciliationException.id == id
        )
        .first()
    )

    if exception is None:
        raise HTTPException(
            status_code=404,
            detail="Exception not found."
        )

    new_comment = ExceptionComment(
        exception_id=id,
        employee_id=current_user["employee_id"],
        comment=comment_data.comment
    )

    db.add(new_comment)
    db.commit()
    db.refresh(new_comment)

    audit = AuditLog(
    session_id=exception.transaction.upload.session_id,
    created_by=current_user["employee_id"],
    action=AuditAction.ADD_EXCEPTION_COMMENT,
    description=f"Added comment to exception {id}"
)

    db.add(audit)
    db.commit()

    return new_comment

@app.patch("/exceptions/{id}/status")
def update_exception_status(
    id: int,
    status_update: ExceptionStatusUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    exception = (
        db.query(ReconciliationException)
        .filter(
            ReconciliationException.id == id
        )
        .first()
    )

    if exception is None:
        raise HTTPException(
            status_code=404,
            detail="Exception not found."
        )

    exception.status = status_update.status

    if (
        status_update.status == ExceptionStatus.UNDER_REVIEW
        and exception.review_started_at is None
    ):

        exception.review_started_at = datetime.now()

    if status_update.status == ExceptionStatus.RESOLVED:

        exception.resolved_at = datetime.now()

        action = AuditAction.RESOLVE_EXCEPTION
        description = f"Resolved exception {id}"

    elif status_update.status == ExceptionStatus.ESCALATED:

        exception.resolved_at = None

        action = AuditAction.ESCALATE_EXCEPTION
        description = f"Escalated exception {id}"

    else:

        exception.resolved_at = None

        action = AuditAction.CREATE_EXCEPTION
        description = (
            f"Updated exception {id} "
            f"to {status_update.status.value}"
        )

    audit = AuditLog(
        session_id=exception.transaction.upload.session_id,
        created_by=current_user["employee_id"],
        action=action,
        description=description
    )

    db.add(audit)

    db.commit()

    db.refresh(exception)

    return exception

@app.get(
    "/audit-logs",
    response_model=list[AuditLogResponse]
)
def get_audit_logs(

    db: Session = Depends(get_db)

):

    logs = (

        db.query(AuditLog)

        .order_by(

            AuditLog.created_at.desc()

        )

        .all()

    )

    return logs

@app.get(
    "/audit-logs/operator",
    response_model=list[AuditLogResponse]
)
def get_operator_logs(
    db: Session = Depends(get_db)
):

    return (

        db.query(AuditLog)

        .filter(

            AuditLog.action.in_([

                AuditAction.CREATE_SESSION,
                AuditAction.UPLOAD_FILE,
                AuditAction.RUN_RECONCILIATION

            ])

        )

        .order_by(
            AuditLog.created_at.desc()
        )

        .all()

    )

@app.get("/reviewer/reports")
def reviewer_reports(
    db: Session = Depends(get_db)
):

    current_session = (
    db.query(ReconciliationSession)
    .filter(
        ReconciliationSession.status == SessionStatus.COMPLETED
    )
    .order_by(ReconciliationSession.id.desc())
    .first()
    )

    if current_session is None:
        raise HTTPException(
            status_code=404,
            detail="No reconciliation session found."
        )

    total = (
    db.query(ReconciliationException)
    .join(Transaction)
    .join(FileUpload)
    .filter(FileUpload.session_id == current_session.id)
    .count()
)

    resolved = (
    db.query(ReconciliationException)
    .join(Transaction)
    .join(FileUpload)
    .filter(FileUpload.session_id == current_session.id).filter(
        ReconciliationException.status ==
        ExceptionStatus.RESOLVED
    ).count()
    )

    escalated = (
    db.query(ReconciliationException)
    .join(Transaction)
    .join(FileUpload)
    .filter(FileUpload.session_id == current_session.id).filter(
        ReconciliationException.status ==
        ExceptionStatus.ESCALATED
    ).count()
    )

    high = (
    db.query(ReconciliationException)
    .join(Transaction)
    .join(FileUpload)
    .filter(FileUpload.session_id == current_session.id).filter(
        ReconciliationException.severity ==
        ExceptionSeverity.HIGH
    ).count()
    )

    if total == 0:

        resolution_rate = 0
        high_share = 0

    else:

        resolution_rate = round(
            resolved * 100 / total,
            1
        )

        high_share = round(
            high * 100 / total,
            1
        )

    most_common = (

    db.query(
        ReconciliationException.exception_type,
        func.count()
    )

    .join(Transaction)
    .join(FileUpload)

    .filter(
        FileUpload.session_id == current_session.id
    )

    .group_by(
        ReconciliationException.exception_type
    )

    .order_by(
        func.count().desc()
    )

    .first()

    )

    avg_resolution_time = (

    db.query(

        func.avg(

            func.extract(
                "epoch",
                ReconciliationException.resolved_at
                - ReconciliationException.review_started_at
            )

        )

    )

    .join(Transaction)
    .join(FileUpload)

    .filter(
        FileUpload.session_id == current_session.id
    )

    .filter(
        ReconciliationException.status ==
        ExceptionStatus.RESOLVED
    )

    .filter(
        ReconciliationException.review_started_at.isnot(None)
    )

    .scalar()

    )

    if avg_resolution_time is None:

        avg_resolution_time = 0

    else:

        avg_resolution_time = round(
            avg_resolution_time / 60,
            1
        )

    return {

        "total": total,

        "resolution_rate": resolution_rate,

        "escalated": escalated,

        "average_resolution_time": avg_resolution_time,

        "most_common":
            most_common[0] if most_common else "N/A",

        "high_share": high_share

    }

@app.get("/admin/dashboard")
def admin_dashboard(
    db: Session = Depends(get_db)
):

    total_users = db.query(User).count()

    active_sessions = (

        db.query(ReconciliationSession)

        .filter(

            ReconciliationSession.status !=

            SessionStatus.COMPLETED

        )

        .count()

    )

    open_exceptions = (

        db.query(ReconciliationException)

        .filter(

            ReconciliationException.status ==

            ExceptionStatus.OPEN

        )

        .count()

    )

    recent_users = (

        db.query(User)

        .order_by(User.created_at.desc())

        .limit(5)

        .all()

    )

    return {

        "total_users": total_users,

        "active_sessions": active_sessions,

        "open_exceptions": open_exceptions,

        "recent_users": recent_users

    }

@app.get(
    "/admin/users",
    response_model=list[UserResponse]
)
def get_admin_users(

    db: Session = Depends(get_db)

):

    return (

        db.query(User)

        .order_by(

            User.created_at.desc()

        )

        .all()

    )

@app.get("/admin/reports")
def admin_reports(

    db: Session = Depends(get_db)

):

    total_users = db.query(User).count()

    completed_sessions = (

        db.query(ReconciliationSession)

        .filter(

            ReconciliationSession.status ==

            SessionStatus.COMPLETED

        )

        .count()

    )

    matched = (

        db.query(Transaction)

        .filter(

            Transaction.transaction_status ==

            TransactionStatus.MATCHED

        )

        .count()

    )

    exceptions = (

        db.query(Transaction)

        .filter(

            Transaction.transaction_status ==

            TransactionStatus.EXCEPTION

        )

        .count()

    )

    if matched + exceptions == 0:

        match_rate = 0

    else:

        match_rate = round(

            matched * 100 /

            (matched + exceptions),

            1

        )

    return {

        "total_users": total_users,

        "completed_sessions": completed_sessions,

        "match_rate": match_rate,

        "exceptions": exceptions

    }

@app.get(
    "/audit-logs/reviewer",
    response_model=list[AuditLogResponse]
)
def get_reviewer_logs(
    db: Session = Depends(get_db)
):

    return (

        db.query(AuditLog)

        .filter(

    AuditLog.action.in_([
        AuditAction.CREATE_EXCEPTION,
        AuditAction.ADD_EXCEPTION_COMMENT,
        AuditAction.RESOLVE_EXCEPTION,
        AuditAction.ESCALATE_EXCEPTION,
        AuditAction.KEEP_OPEN
    ])

)

        .order_by(AuditLog.created_at.desc())

        .all()

    )