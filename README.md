# Lite-Dispatch

**Lite-Dispatch** is a production-grade Incident Management System built with **FastAPI**, **PostgreSQL**, and **Docker**.

It mimics the core architecture of tools like [Netflix Dispatch](https://github.com/Netflix/dispatch), focusing on clean design patterns, extensibility, and modern backend practices.

## 🚀 Key Features

*   **Service Layer Architecture**: Clean separation between API, Business Logic, and Data.
*   **Plugin System**: Extensible architecture using Abstract Base Classes (ABC) for integrations (e.g., Notifications).
*   **State Machine Logic**: Enforced incident transitions (Open -> Investigating -> Resolved).
*   **Async Background Tasks**: Non-blocking I/O for heavy operations using `BackgroundTasks`.
*   **Authentication**: Secure JWT-based auth with `passlib` (bcrypt) and `python-jose`.
*   **Structured Logging**: Production-ready JSON logging with `structlog`.
*   **Database Migrations**: Version-controlled schema changes using `Alembic`.
*   **Integration Testing**: Comprehensive test suite using `pytest` and SQLite.

## 🛠️ Tech Stack

*   **Language**: Python 3.10+
*   **Framework**: FastAPI
*   **Database**: PostgreSQL
*   **ORM**: SQLAlchemy
*   **Containerization**: Docker & Docker Compose
*   **Dependency Management**: Poetry

## 📚 Documentation

*   **[System Design](system_design.md)**: Deep dive into the architecture, ER Diagram, and Database Theory (ACID, Normalization).

## 🏃‍♂️ How to Run

### Prerequisities
*   Docker & Docker Compose

### Quick Start
1.  **Clone the repository**
2.  **Start the stack**:
    ```bash
    docker-compose up --build
    ```
3.  **Access the API**:
    Navigate to [http://localhost:8000/docs](http://localhost:8000/docs) to see the interactive Swagger UI.

### Running Tests
To run the integration tests:
```bash
poetry run pytest
```

## 🔒 Authentication
To interact with protected endpoints:
1.  Go to the `/docs` page.
2.  Click **Authorize**.
3.  **Username**: `admin@example.com`
4.  **Password**: `secret`