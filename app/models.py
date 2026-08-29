from sqlalchemy.orm import Mapped, mapped_column, relationship
from database import Base
from enum import Enum
from sqlalchemy import Enum as SQLEnum
from sqlalchemy import ForeignKey
from datetime import datetime, date
from decimal import Decimal
from sqlalchemy import String, Integer, DateTime, Date, func, Numeric, Text

class UserRole(str, Enum):
    OPERATOR = "operator"
    REVIEWER = "reviewer"
    ADMIN = "admin"

class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key = True, autoincrement = True)
    employee_id: Mapped[str] = mapped_column(String(50), unique = True, nullable = False)
    full_name: Mapped[str] = mapped_column(String(100), nullable = False)
    email: Mapped[str] = mapped_column(String(255), unique = True, nullable = False)
    password_hash: Mapped[str] = mapped_column(String(255), nullable = False)
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())
    last_login: Mapped[datetime | None] = mapped_column(DateTime, nullable = True) 
    role: Mapped[UserRole] = mapped_column(SQLEnum(UserRole), default = UserRole.OPERATOR, nullable = False)

class SessionStatus(str, Enum):
    UPLOADING = "UPLOADING"
    READY = "READY"
    IN_PROGRESS = "IN_PROGRESS"
    COMPLETED = "COMPLETED"

class ReconciliationSession(Base):
    __tablename__ = "reconciliation_sessions"

    id: Mapped[int] = mapped_column(Integer, primary_key = True, autoincrement = True)
    business_date: Mapped[date] = mapped_column(Date, nullable = False)
    required_sources: Mapped[int] = mapped_column(default = 4, nullable = False)
    status: Mapped[SessionStatus] = mapped_column(default = SessionStatus.UPLOADING, nullable = False)
    created_by: Mapped[str] = mapped_column(ForeignKey("users.employee_id"), nullable = False)
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default = func.now())
    completed_at: Mapped[datetime | None] = mapped_column(DateTime, nullable = True)
    matched_transactions: Mapped[int] = mapped_column(Integer, default = 0)
    exception_count: Mapped[int] = mapped_column(Integer, default = 0)

class UploadStatus(str, Enum):
    SUCCESS = "SUCCESS"
    FAILED = "FAILED"
    PARTIAL = "PARTIAL"

class SourceType(str, Enum):
    BANK = "Bank"
    MERCHANT = "Merchant"
    CARD_NETWORK = "Card Network"
    INTERNAL_LEDGER = "Internal Ledger"

class FileUpload(Base):
    __tablename__= "file_uploads"

    id: Mapped[int] = mapped_column(Integer, primary_key = True, autoincrement = True)
    session_id: Mapped[int] = mapped_column(ForeignKey("reconciliation_sessions.id"), nullable = False)
    source: Mapped[SourceType] = mapped_column(SQLEnum(SourceType), nullable = False)
    filename: Mapped[str] = mapped_column(String(255), nullable = False)
    uploaded_at: Mapped[datetime] = mapped_column(DateTime, server_default = func.now())
    status: Mapped[UploadStatus] = mapped_column(SQLEnum(UploadStatus), nullable = False)
    valid_records: Mapped[int] = mapped_column(Integer, nullable = False)
    invalid_records: Mapped[int] = mapped_column(Integer, nullable = False)
    transactions = relationship(
        "Transaction",
        back_populates="upload"
    )

class TransactionStatus(str, Enum):
    MATCHED = "MATCHED"
    UNMATCHED = "UNMATCHED"
    EXCEPTION = "EXCEPTION"
    PENDING = "PENDING"

class Transaction(Base):
    __tablename__ = "transactions"

    id: Mapped[int] = mapped_column(Integer, primary_key = True, autoincrement = True)
    upload_id: Mapped[int] = mapped_column(ForeignKey("file_uploads.id"), nullable = False)
    transaction_reference: Mapped[str] = mapped_column(String(100), unique = False, nullable = False)
    customer_id: Mapped[str] = mapped_column(String(100), nullable = False)
    amount: Mapped[Decimal] = mapped_column(Numeric(15, 2), nullable = False)
    currency: Mapped[str] = mapped_column(String(3), nullable = False)
    transaction_date: Mapped[Date] = mapped_column(Date, nullable = False)
    source: Mapped[SourceType] = mapped_column(SQLEnum(SourceType), nullable = False)
    transaction_status: Mapped[TransactionStatus] = mapped_column(SQLEnum(TransactionStatus), nullable = False)
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default = func.now())
    upload = relationship(
        "FileUpload",
        back_populates="transactions"
    )

class ReconciliationResultStatus(str, Enum):
    MATCHED = "MATCHED"
    EXCEPTION = "EXCEPTION"

class ReconciliationResult(Base):
    __tablename__ = "reconciliation_results"

    id: Mapped[int] = mapped_column(Integer, primary_key = True, autoincrement = True)
    transaction_id: Mapped[int] = mapped_column(ForeignKey("transactions.id"), nullable = False)
    session_id: Mapped[int] = mapped_column(ForeignKey("reconciliation_sessions.id"), nullable = False)
    result: Mapped[str] = mapped_column(String(20), nullable = False)
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default = func.now())
    transaction = relationship("Transaction")
    session = relationship("ReconciliationSession")

class ExceptionType(str, Enum):
    AMOUNT_MISMATCH = "AMOUNT MISMATCH"
    CURRENCY_MISMATCH = "CURRENCY MISMATCH"
    MISSING_RECORD = "MISSING RECORD"
    DUPLICATE_RECORD = "DUPLICATE RECORD"
    DATE_MISMATCH = "DATE MISMATCH"
    INVALID_REFERENCE = "INVALID REFERENCE"

class ExceptionStatus(str, Enum):
    OPEN = "OPEN"
    UNDER_REVIEW = "UNDER REVIEW"
    RESOLVED = "RESOLVED"
    ESCALATED = "ESCALATED"

class ExceptionSeverity(str, Enum):
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"

class ReconciliationException(Base):
    __tablename__ = "reconciliation_exceptions"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    transaction_id: Mapped[int] = mapped_column(ForeignKey("transactions.id"), nullable=False)
    exception_type: Mapped[ExceptionType] = mapped_column(SQLEnum(ExceptionType), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    status: Mapped[ExceptionStatus] = mapped_column(SQLEnum(ExceptionStatus), default=ExceptionStatus.OPEN, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())
    review_started_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    resolved_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    severity: Mapped[ExceptionSeverity] = mapped_column(SQLEnum(ExceptionSeverity), default=ExceptionSeverity.MEDIUM, nullable=False)
    transaction = relationship("Transaction")

class AuditAction(str, Enum):
    ADD_EXCEPTION_COMMENT = "ADD_EXCEPTION_COMMENT"
    LOGIN = "LOGIN"
    CREATE_SESSION = "CREATE_SESSION"
    UPLOAD_FILE = "UPLOAD_FILE"
    RUN_RECONCILIATION = "RUN_RECONCILIATION"
    CREATE_EXCEPTION = "CREATE_EXCEPTION"
    RESOLVE_EXCEPTION = "RESOLVE_EXCEPTION"
    LOGOUT = "LOGOUT"
    ESCALATE_EXCEPTION = "ESCALATE_EXCEPTION"
    KEEP_OPEN = "KEEP_OPEN"

class AuditLog(Base):
    __tablename__ = "audit_logs"

    id: Mapped[int] = mapped_column(Integer, primary_key = True, autoincrement = True)
    session_id: Mapped[int] = mapped_column(ForeignKey("reconciliation_sessions.id"), nullable = False)
    action: Mapped[AuditAction] = mapped_column(SQLEnum(AuditAction), nullable = False)
    description: Mapped[str] = mapped_column(Text, nullable = False)
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default = func.now())
    created_by: Mapped[str] = mapped_column(ForeignKey("users.employee_id"), nullable = False)

class ExceptionComment(Base):
    __tablename__ = "exception_comments"

    id: Mapped[int] = mapped_column(Integer, primary_key = True, autoincrement = True)
    exception_id: Mapped[int] = mapped_column(ForeignKey("reconciliation_exceptions.id"), nullable = False)
    employee_id: Mapped[str] = mapped_column(ForeignKey("users.employee_id"), nullable = False)
    comment: Mapped[str] = mapped_column(String(1000),nullable = False)
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default = func.now())