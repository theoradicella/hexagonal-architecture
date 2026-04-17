# Hexagonal Architecture — Order Management API

A small Python project demonstrating **hexagonal architecture** (also known as ports & adapters) with FastAPI, SQLAlchemy and JWT authentication. The domain is a simple order management system with customers, vendors and orders that move through a state machine.

The point of this repository is the **architecture**, not the features. The code is kept small so the layering is easy to follow.

---

## What is hexagonal architecture?

The core idea: your business logic (the **domain**) should not depend on any framework, database or external tool. Dependencies always point **inward** toward the domain. External systems are plugged in through **ports** (interfaces) and **adapters** (concrete implementations).

```flowchart LR
 subgraph Driving["Driving adapters (inbound)"]
    direction TB
        HTTP["FastAPI routes"]
        CLI["CLI / tests"]
  end
 subgraph Driven["Driven adapters (outbound)"]
    direction TB
        DB["SQLAlchemy / MySQL"]
        JWT["JWT token service"]
        BCRYPT["bcrypt hasher"]
        SMTP["SMTP notifier"]
  end
    HTTP --> DOMAIN{{"Domain<br><br>Entities<br>Use cases<br>Ports"}}
    CLI --> DOMAIN
    DOMAIN --> DB & JWT & BCRYPT & SMTP

     DOMAIN:::Peach
    classDef Peach stroke-width:1px, stroke-dasharray:none, stroke:#FBB35A, fill:#FFEFDB, color:#8F632D
    style DOMAIN stroke:#000000,color:#D50000
```

- **Driving adapters** call into the domain (HTTP requests, CLI commands, tests).
- **Driven adapters** are called *by* the domain (databases, email servers, JWT libraries).
- The domain only knows about **ports**. It never imports from `adapters/`.
- The **composition root** (`infrastructure/dependencies.py`) is the only place allowed to wire ports to concrete adapters.

This decoupling means you can swap MySQL for Postgres, bcrypt for argon2, or FastAPI for gRPC without touching a single use case.

---

## Tech stack

| Layer | Technology |
|---|---|
| Web framework | FastAPI + Uvicorn |
| Validation | Pydantic v2 |
| ORM | SQLAlchemy 2.x (async) |
| Database | MySQL 8 (via Docker) |
| Migrations | Alembic |
| Auth | JWT (`python-jose`) + `bcrypt` |
| Testing | pytest + pytest-asyncio + httpx |
| Tooling | uv, ruff, mypy |
| API collection | Bruno |

---

## Project structure

```
domain/              Pure business logic — no framework imports
  entities/          Plain dataclasses (User, Customer, Vendor, Order)
  ports/             Protocol interfaces (repositories, services, notifiers)
  use_cases/         One class per business operation
  exceptions.py      Domain-level errors (no HTTP awareness)

adapters/
  driving/api/       Inbound — FastAPI routes and Pydantic schemas
  driven/
    persistence/     SQLAlchemy models and repositories
    auth/            bcrypt hasher + JWT token service
    notifications/   SMTP and in-memory email notifiers

infrastructure/
  config.py          Typed settings from .env
  database.py        Engine, session factory, declarative Base
  dependencies.py    Composition root — the only file that imports both sides

alembic/             Database migrations
tests/
  unit/              Use cases tested in isolation with in-memory stubs
  integration/       Real HTTP + SQLite, end-to-end flows
bruno/               Request collection for the Bruno HTTP client
```

---

## Getting started

### Prerequisites

- Python 3.12+
- [uv](https://github.com/astral-sh/uv) for dependency management
- Docker (for the MySQL container)

### 1. Clone and install

```bash
git clone <repo-url>
cd hexagonal-test
uv venv && source .venv/bin/activate
uv sync
```

### 2. Start MySQL

```bash
docker compose up -d
```

This runs MySQL 8 on port 3306 with a database called `ordersdb`.

### 3. Configure environment

```bash
cp .env.example .env
```

The defaults work out of the box against the Docker container. Change `SECRET_KEY` before deploying anywhere real.

### 4. Apply migrations

```bash
alembic upgrade head
```

### 5. Run the server

```bash
uvicorn main:app --reload
```

The API is at `http://localhost:8000`. Swagger UI is at `http://localhost:8000/docs`.

---

## Testing

```bash
pytest                      # all tests
pytest tests/unit/          # unit tests only (fast, in-memory)
pytest tests/integration/   # integration tests (real HTTP + SQLite)
```

Unit tests use hand-rolled in-memory stubs under `tests/unit/stubs/` — this is the payoff of hexagonal architecture: the domain can be exercised without a database or network.

Integration tests spin up an in-memory SQLite database per test and hit the real FastAPI app via `httpx.AsyncClient`.

---

## Code quality

```bash
ruff check .    # linting + import sorting
mypy .          # type checking (strict mode)
```

---

## Using the API

### Swagger UI

Open `http://localhost:8000/docs` for an interactive Swagger UI. All endpoints are documented with their request and response schemas.

### Bruno collection

A versioned request collection lives under `bruno/`. Open the folder in [Bruno](https://www.usebruno.com/) (or the Bruno VS Code extension), select the `local` environment, and run the requests in order:

1. `auth/Register` — creates a user
2. `auth/Login` — captures the JWT into `{{token}}` automatically
3. All other requests include `Authorization: Bearer {{token}}` and work straight away

### Endpoints

| Method | Path | Description |
|---|---|---|
| `POST` | `/api/v1/auth/register` | Create a new user |
| `POST` | `/api/v1/auth/login` | Authenticate, returns a JWT |
| `POST` | `/api/v1/customers` | Create a customer |
| `GET` | `/api/v1/customers` | List customers (paginated) |
| `POST` | `/api/v1/vendors` | Create a vendor |
| `GET` | `/api/v1/vendors` | List vendors (paginated) |
| `POST` | `/api/v1/orders` | Create an order (status: `PENDING`) |
| `GET` | `/api/v1/orders` | List orders (paginated, filterable) |
| `PATCH` | `/api/v1/orders/{id}/status` | Transition order status |
| `DELETE` | `/api/v1/orders/{id}` | Cancel an order |

### Order state machine

Orders move through a strict state machine enforced by `Order.transition_to()`:

```
PENDING ──► CONFIRMED ──► SHIPPED ──► DELIVERED
   │            │
   └────────────┴──► CANCELLED
```

Any other transition raises `InvalidStatusTransitionError` in the domain, which the API maps to HTTP 422.

---

## Exception → HTTP mapping

Domain exceptions are framework-agnostic. The API layer translates them:

| Domain exception | HTTP status |
|---|---|
| `*NotFoundError` | 404 |
| `InvalidStatusTransitionError` | 422 |
| `InvalidCredentialsError` | 401 |
| `UserAlreadyExistsError` | 409 |
