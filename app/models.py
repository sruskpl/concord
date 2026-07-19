from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import create_engine
from enum import Enum
from sqlalchemy import Enum as SQLEnum
from sqlalchemy import ForeignKey
from datetime import datetime, date
from decimal import Decimal
from sqlalchemy import String, Integer, DateTime, Date, func, Numeric, Text
from sqlalchemy.orm import DeclarativeBase, sessionmaker

DATABASE_URL = (
    "postgresql://postgres:your_password@localhost:5432/concord"
)

engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(
    bind=engine,
    autoflush=False,
    autocommit=False
)

class Base(DeclarativeBase):
    pass

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
    role: Mapped[UserRole] = mapped_column(default = UserRole.OPERATOR, nullable = False)

class SessionStatus(str, Enum):
    READY = "READY"
    IN_PROGRESS = "IN_PROGRESS"
    COMPLETED = "COMPLETED"

class ReconciliationSession(Base):
    __tablename__ = "reconciliation_sessions"

    id: Mapped[int] = mapped_column(Integer, primary_key = True, autoincrement = True)
    business_date: Mapped[date] = mapped_column(Date, nullable = False)
    status: Mapped[SessionStatus] = mapped_column(default = SessionStatus.READY, nullable = False)
    created_by: Mapped[str] = mapped_column(ForeignKey("users.employee_id"), nullable = False)
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default = func.now())
    completed_at: Mapped[datetime | None] = mapped_column(DateTime, nullable = True)

class UploadStatus(str, Enum):
    SUCCESS = "SUCCESS"
    FAILED = "FAILED"
    PARTIAL = "PARTIAL"

class UploadSource(str, Enum):
    BANK = "Bank"
    MERCHANT = "Merchant"
    CARD_NETWORK = "Card Network"
    INTERNAL_LEDGER = "Internal Ledger"

class FileUpload(Base):
    __tablename__= "file_uploads"

    id: Mapped[int] = mapped_column(Integer, primary_key = True, autoincrement = True)
    session_id: Mapped[int] = mapped_column(ForeignKey("reconciliation_sessions.id"), nullable = False)
    source: Mapped[UploadSource] = mapped_column(SQLEnum(UploadSource), nullable = False)
    filename: Mapped[str] = mapped_column(String(255), nullable = False)
    uploaded_at: Mapped[datetime] = mapped_column(DateTime, server_default = func.now())
    status: Mapped[UploadStatus] = mapped_column(SQLEnum(UploadStatus), nullable = False)
    valid_records: Mapped[int] = mapped_column(Integer, nullable = False)
    invalid_records: Mapped[int] = mapped_column(Integer, nullable = False)

class TransactionStatus(str, Enum):
    SUCCESS = "SUCCESS"
    FAILED = "FAILED"
    PENDING = "PENDING"

class Transaction(Base):
    __tablename__ = "transactions"

    id: Mapped[int] = mapped_column(Integer, primary_key = True, autoincrement = True)
    upload_id: Mapped[int] = mapped_column(ForeignKey("file_uploads.id"), nullable = False)
    transaction_reference: Mapped[str] = mapped_column(String(100), unique = True, nullable = False)
    customer_id: Mapped[str] = mapped_column(String(100), unique = True, nullable = False)
    amount: Mapped[Decimal] = mapped_column(Numeric(15, 2), nullable = False)
    currency: Mapped[str] = mapped_column(String(3), nullable = False)
    transaction_date: Mapped[Date] = mapped_column(Date, nullable = False)
    source_system: Mapped[UploadSource] = mapped_column(SQLEnum(UploadSource), nullable = False)
    transaction_status: Mapped[TransactionStatus] = mapped_column(SQLEnum(TransactionStatus), nullable = False)
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default = func.now())

class ExceptionType(str, Enum):
    AMOUNT_MISMATCH = "AMOUNT_MISMATCH"
    MISSING_RECORD = "MISSING_RECORD"
    DUPLICATE_RECORD = "DUPLICATE_RECORD"
    DATE_MISMATCH = "DATE_MISMATCH"
    INVALID_REFERENCE = "INVALID_REFERENCE"

class ExceptionStatus(str, Enum):
    OPEN = "OPEN"
    UNDER_REVIEW = "UNDER_REVIEW"
    RESOLVED = "RESOLVED"

class ExceptionSeverity(str, Enum):
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"
    CRITICAL = "CRITICAL"

class ReconciliationExceptions(Base):
    __tablename__ = "reconciliation_exceptions"

    id: Mapped[int] = mapped_column(Integer, primary_key = True, autoincrement = True)
    transaction_id: Mapped[int] = mapped_column(ForeignKey("transactions.id"), nullable = False)
    exception_type: Mapped[ExceptionType] = mapped_column(SQLEnum(ExceptionType), nullable = False)
    description: Mapped[str] = mapped_column(Text, nullable = False)
    status: Mapped[ExceptionStatus] = mapped_column(SQLEnum(ExceptionStatus), default=ExceptionStatus.OPEN, nullable = False)
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default = func.now())
    resolved_at: Mapped[datetime | None] = mapped_column(DateTime, nullable = True)
    severity: Mapped[ExceptionSeverity] = mapped_column(SQLEnum(ExceptionSeverity), default=ExceptionSeverity.MEDIUM, nullable = False)

class AuditAction(str, Enum):
    LOGIN = "LOGIN"
    CREATE_SESSION = "CREATE_SESSION"
    UPLOAD_FILE = "UPLOAD_FILE"
    RUN_RECONCILIATION = "RUN_RECONCILIATION"
    CREATE_EXCEPTION = "CREATE_EXCEPTION"
    RESOLVE_EXCEPTION = "RESOLVE_EXCEPTION"
    LOGOUT = "LOGOUT"

class AuditLog(Base):
    __tablename__ = "audit_logs"

    id: Mapped[int] = mapped_column(Integer, primary_key = True, autoincrement = True)
    session_id: Mapped[int] = mapped_column(ForeignKey("reconciliation_sessions.id"), nullable = False)
    employee_id: Mapped[str] = mapped_column(ForeignKey("users.employee_id"), nullable = False)
    action: Mapped[AuditAction] = mapped_column(SQLEnum(AuditAction), nullable = False)
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default = func.now())

class ExceptionComment(Base):
    __tablename__ = "exception_comments"

    id: Mapped[int] = mapped_column(Integer, primary_key = True, autoincrement = True)
    exception_id: Mapped[int] = mapped_column(ForeignKey("reconciliation_exceptions.id"), nullable = False)
    employee_id: Mapped[str] = mapped_column(ForeignKey("users.employee_id"), nullable = False)
    comment: Mapped[str] = mapped_column(String(1000),nullable = False)
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default = func.now())