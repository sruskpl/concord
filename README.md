# Concord 

A financial reconciliation platform that enables organizations to reconcile transactions across multiple data sources, investigate exceptions, maintain audit trails, and streamline operational workflows through secure role-based dashboards.

## Project Overview

### Concord is a full-stack financial reconciliation platform that simulates how banks and financial institutions reconcile transactions received from multiple financial systems. The application enables operators to create reconciliation sessions, upload transaction files from different financial sources, execute transaction reconciliation, investigate exceptions, and maintain a complete audit trail of operational activities.

### The project was designed to replicate a real-world back-office financial workflow. It demonstrates authentication, role-based access control, relational database design, session lifecycle management, reconciliation processing, exception management, and audit logging within a modular full-stack architecture.

### Concord currently supports three operational roles—Operator, Reviewer, and Administrator—each with dedicated dashboards and permissions, closely resembling enterprise financial systems used for transaction operations and compliance.

## Key Highlights
- Full-stack financial reconciliation platform inspired by real-world banking operations.
- Role-Based Access Control (Operator, Reviewer, Administrator) with dedicated dashboards and workflows.
- Session-driven reconciliation lifecycle from creation to completion.
- Transaction reconciliation engine that groups financial records across multiple uploaded sources.
- Exception management workflow with reviewer investigation and resolution tracking.
- Immutable audit logging of operational activities for accountability and traceability.
- Secure JWT-based authentication with protected REST APIs.
- PostgreSQL database designed using normalized relational models and SQLAlchemy ORM.
- Modern React frontend integrated with a FastAPI backend through RESTful APIs.

## Tech Stack

### Frontend
- React
- React Router
- JavaScript (ES6+)
- HTML5
- CSS3

### Backend
- FastAPI
- Python

### Database
- PostgreSQL
- SQLAlchemy ORM

### Authentication & Security
- JWT (JSON Web Tokens)
- Passlib (bcrypt)

### Development Tools
- Git
- GitHub
- VS Code

### APIs
- RESTful APIs

## System Architecture

Concord follows a modular client-server architecture designed around a financial reconciliation workflow.

- The React frontend provides role-specific dashboards for Operators, Reviewers and Administrators.
- React communicates with the FastAPI backend through authenticated REST APIs.
- FastAPI handles authentication, authorization, reconciliation logic, session management and exception workflows.
- SQLAlchemy ORM manages all database interactions.
- PostgreSQL stores users, reconciliation sessions, uploaded files, transactions, exceptions, comments and audit logs.
- JWT secures protected API endpoints through role-based access control.

                 +----------------------+
                 |    React Frontend    |
                 +----------+-----------+
                            |
                    REST API Requests
                            |
                 +----------v-----------+
                 |     FastAPI API      |
                 +----------+-----------+
                            |
        +-------------------+------------------+
        |                   |                  |
 Authentication       Reconciliation      Exception Handling
        |                   |                  |
        +-------------------+------------------+
                            |
                      SQLAlchemy ORM
                            |
                 +----------v-----------+
                 |      PostgreSQL      |
                 +----------------------+

## API Endpoints

### Authentication

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/register` | Register a new user |
| POST | `/login` | Authenticate user and return JWT |
| GET | `/me` | Retrieve authenticated user information |

### Reconciliation Sessions

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/sessions/start` | Start a new reconciliation session |
| GET | `/sessions` | Retrieve all reconciliation sessions |
| GET | `/dashboard/current` | Retrieve current dashboard summary |

### File Uploads

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/upload` | Upload transaction CSV file |

### Reconciliation

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/reconcile/{session_id}` | Execute reconciliation for a session |

### Exception Management

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/exceptions/session-info` | Retrieve latest completed session |
| GET | `/exceptions/session/{session_id}` | Retrieve reconciliation exceptions |
| GET | `/exception/{id}` | Retrieve exception details |
| POST | `/exceptions/{id}/comment` | Add reviewer comment |
| PUT | `/exceptions/{id}/status` | Update exception status |

### Audit Logs

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/audit/operator` | Retrieve operator audit logs |
| GET | `/audit/reviewer` | Retrieve reviewer audit logs |
| GET | `/audit/admin` | Retrieve administrator audit logs |

### Administration

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/admin/dashboard` | Retrieve administrator dashboard metrics |
| GET | `/admin/users` | Retrieve registered users |

## Database Design

Concord uses a normalized PostgreSQL relational database to model the complete financial reconciliation lifecycle. The schema separates authentication, reconciliation sessions, uploaded financial records, transaction processing, exception management, and audit logging into dedicated entities.

### Core Tables

| Table | Purpose |
|--------|----------|
| Users | Stores authenticated users and role-based access information. |
| Reconciliation Sessions | Tracks each reconciliation cycle, business date, status and processing statistics. |
| File Uploads | Maintains metadata about uploaded financial source files. |
| Transactions | Stores every financial transaction imported from uploaded files. |
| Reconciliation Results | Records whether each transaction was successfully matched or became an exception. |
| Reconciliation Exceptions | Stores unmatched transactions requiring manual investigation. |
| Exception Comments | Maintains reviewer investigation notes and resolution history. |
| Audit Logs | Provides an immutable audit trail of every important system activity. |

The database was designed using SQLAlchemy ORM with PostgreSQL and follows a normalized relational structure to minimize redundancy while maintaining referential integrity through foreign key relationships.

## Financial Reconciliation Workflow
Concord models a simplified financial reconciliation process commonly followed by banking and financial operations teams. Each reconciliation session progresses through a structured workflow from transaction ingestion to exception investigation while maintaining complete operational traceability.
 
 ### Workflow Diagram

                ┌──────────────────────────────┐
│      Operator Login          │
└──────────────┬───────────────┘
               │
               ▼
┌──────────────────────────────┐
│ Create Reconciliation Session│
└──────────────┬───────────────┘
               │
               ▼
┌──────────────────────────────┐
│ Business Date Assigned       │
└──────────────┬───────────────┘
               │
               ▼
┌──────────────────────────────┐
│ Upload Source Files          │
└──────────────┬───────────────┘
               │
     ┌─────────┼─────────┬─────────┐
     │         │         │         │
     ▼         ▼         ▼         ▼
┌────────┐ ┌─────────┐ ┌──────────┐ ┌────────────────┐
│ Bank   │ │Merchant │ │Card Net. │ │Internal Ledger │
└────┬───┘ └────┬────┘ └────┬─────┘ └───────┬────────┘
     └──────────┴───────────┴───────────────┘
                        │
                        ▼
┌──────────────────────────────┐
│ Basic CSV Parsing            │
│                              │
└──────────────┬───────────────┘
               │
               ▼
┌──────────────────────────────┐
│ Store Transactions           │
│ PostgreSQL                   │
└──────────────┬───────────────┘
               │
               ▼
┌──────────────────────────────┐
│ All Required Sources         │
│ Uploaded?                    │
└───────┬───────────────┬──────┘
        │               │
       No              Yes
        │               │
        ▼               ▼
 Wait for all        Run Reconciliation
 sources                |
 to be uploaded         │
                        ▼
┌──────────────────────────────┐
│ Matching Engine              │
│ Groups transactions by       │
│ Transaction Reference        │
└──────────────┬───────────────┘
               │
      ┌────────┴────────┐
      │                 │
      ▼                 ▼
Matched Records   Unmatched Records
      │                 │
      ▼                 ▼
      |          Create Exceptions
      │                 │
      └────────┬────────┘
               ▼
┌───────────────────────────────┐
│Generate Reconciliation Results│
└──────────────┬────────────────┘
               │
               ▼
┌──────────────────────────────┐
│ Reviewer Queue               │
└──────────────┬───────────────┘
               │
               ▼
┌──────────────────────────────┐
│ Open Exception               │
└──────────────┬───────────────┘
               │
               ▼
┌──────────────────────────────┐
│ Investigation Timeline       │
└──────────────┬───────────────┘
               │
               ▼
┌──────────────────────────────┐
│ Reviewer Comments            │
└──────────────┬───────────────┘
               │
               ▼
┌──────────────────────────────┐
│ Resolve / Escalate           │
└──────────────┬───────────────┘
               │
               ▼
┌──────────────────────────────┐
│ Immutable Audit Log          │
└──────────────────────────────┘

### Workflow Stages

1. **Authentication**
   - The operator authenticates using JWT-based authentication.

2. **Session Creation**
   - A reconciliation session is created for the selected business date.

3. **Transaction Upload**
   - Financial transaction files are uploaded and stored in the database.

4. **Reconciliation**
   - Transactions sharing the same transaction reference across uploaded sources are grouped and processed by the reconciliation engine.

5. **Result Generation**
   - Successfully matched transactions are recorded as reconciled.
   - Remaining transactions become reconciliation exceptions.

6. **Exception Investigation**
   - Reviewers inspect unresolved exceptions, add investigation comments and update their status.

7. **Audit Logging**
   - Every critical operation—including logins, uploads, reconciliation execution and exception handling—is permanently recorded in the audit log.

## Skills Demonstrated

- FastAPI Backend Development
- REST API Design and Development
- JWT Authentication & Role-Based Authorization
- Password Hashing using bcrypt
- PostgreSQL Database Design
- SQLAlchemy ORM
- Database Relationship Modeling
- CSV File Processing
- Financial Reconciliation Workflow Design
- Exception Management System
- Audit Logging
- Server-side Pagination for Sessions and Exception Queue
- Role-Based Dashboard Routing
- React Frontend Development
- Frontend–Backend Integration
- State Management using React Hooks
- Git & GitHub

## Future Improvements

Although Concord provides a complete end-to-end reconciliation workflow, several enhancements are planned for future versions:

- Implement advanced CSV validation before transactions are stored in the database.
- Support configurable reconciliation rules instead of matching only by transaction reference.
- Display detailed reconciliation statistics and interactive dashboards with charts.
- Generate downloadable reconciliation and exception reports in PDF and Excel formats.
- Enable bulk exception resolution and assignment to reviewers.
- Introduce email and in-application notifications for pending exception reviews.
- Implement role-based permissions with finer access control for administrative operations.
- Expand pagination on reconciliation exceptions, sessions and audit log views for larger datasets. 
- Introduce advanced filtering and search capabilities for sessions, audit logs, and reconciliation exceptions.

