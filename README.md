<div align="center">

# 🏋️ Workout Tracker API

[![Python](https://img.shields.io/badge/Python-3.12+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.129-009688?style=for-the-badge&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-15-336791?style=for-the-badge&logo=postgresql&logoColor=white)](https://postgresql.org)
[![Redis](https://img.shields.io/badge/Redis-Cache-DC382D?style=for-the-badge&logo=redis&logoColor=white)](https://redis.io)
[![Docker](https://img.shields.io/badge/Docker-Compose-2496ED?style=for-the-badge&logo=docker&logoColor=white)](https://docker.com)

**A full-featured async REST API for tracking gym workouts**  
Plan sessions, log sets, and monitor your progress — all in one place.

🔗 **GitHub:** [https://github.com/100kgtrotila/workout-tracker](https://github.com/100kgtrotila/workout-tracker)  
📋 **Project Page:** [https://roadmap.sh/projects/fitness-workout-tracker](https://roadmap.sh/projects/fitness-workout-tracker)

</div>

---

## 📋 Table of Contents

- [About](#-about)
- [Features](#-features)
- [Tech Stack](#-tech-stack)
- [Architecture](#-architecture)
- [Project Structure](#-project-structure)
- [Data Models](#-data-models)
- [API Endpoints](#-api-endpoints)
- [Quick Start](#-quick-start)
- [Environment Variables](#-environment-variables)
- [Database Migrations](#-database-migrations)
- [Testing](#-testing)
- [Security](#-security)

---

## 🎯 About

**Workout Tracker** is an asynchronous REST API backend built with FastAPI. It allows users to:

- Register and authenticate using JWT tokens
- Browse and manage a library of exercises categorized by muscle group
- Plan and track workouts with scheduling, statuses, and notes
- Add exercises to workouts in a custom order
- Log individual sets with reps and weight per exercise

---

## ✨ Features

| Category | Details |
|----------|---------|
| 👤 **Users** | Registration, login, JWT authentication, role-based access (user / admin) |
| 🏃 **Exercises** | Full CRUD, muscle group classification, Redis caching |
| 📅 **Workouts** | Planning, statuses (planned / completed / skipped), notes |
| 💪 **Workout Exercises** | Add exercises to workouts, manage execution order |
| 📊 **Sets** | Log reps and weight for every set of every exercise |
| ⚡ **Caching** | Redis cache for exercises with 1h TTL and tag-based invalidation |
| 🔐 **Authorization** | Role-Based Access Control (RBAC), protected endpoints |
| 🐳 **Docker** | Fully containerized: app + PostgreSQL + Redis |

---

## 🛠 Tech Stack

### Core
- **[FastAPI](https://fastapi.tiangolo.com/)** — modern async web framework
- **[SQLAlchemy 2.0](https://sqlalchemy.org/)** — async ORM with full typing support
- **[Alembic](https://alembic.sqlalchemy.org/)** — database schema migrations
- **[Pydantic v2](https://docs.pydantic.dev/)** — data validation and settings management

### Database & Cache
- **PostgreSQL 15** — primary relational database
- **asyncpg** — async PostgreSQL driver
- **Redis** — in-memory caching layer
- **[Cashews](https://github.com/Krukov/cashews)** — Redis caching library with TTL and tag-based invalidation

### Security
- **[pwdlib](https://github.com/frankie567/pwdlib)** + **Argon2** — secure password hashing
- **PyJWT** — JWT token creation and validation
- **OAuth2 Password Bearer** — standard authentication scheme

### DevOps & Quality
- **Docker + Docker Compose** — full containerization
- **[uv](https://github.com/astral-sh/uv)** — ultra-fast Python package manager
- **Ruff** — linter and code formatter
- **pytest + pytest-asyncio** — async testing framework
- **httpx** — async HTTP client for tests

---

## 🏗 Architecture

The project follows a **modular layered architecture** with clear separation of concerns:

```
HTTP Request
     │
     ▼
  Router        ← validates input via Pydantic schemas
     │
     ▼
  Service       ← business logic + cache layer (Redis/Cashews)
     │
     ▼
SQLAlchemy      ← async ORM queries
     │
     ▼
 PostgreSQL      ← persistent storage
```

Each domain module (`gym`, `training`, `user`) is self-contained and includes:

- **`models.py`** — SQLAlchemy ORM models
- **`schemas.py`** — Pydantic request/response schemas
- **`service.py`** — business logic and data access
- **`router.py`** — HTTP route handlers
- **`exceptions.py`** — domain-specific exceptions
- **`enums.py`** — enumerations (where applicable)

---

## 📁 Project Structure

```
workout-tracker/
│
├── app/
│   ├── core/                    # Application core
│   │   ├── config.py            # Settings via pydantic-settings
│   │   ├── db.py                # DB engine, Base, get_db dependency
│   │   ├── security.py          # JWT, password hashing, RBAC
│   │   ├── exceptions.py        # Base exception classes
│   │   ├── handlers.py          # Global error handlers
│   │   ├── schemas.py           # Base Pydantic model
│   │   └── cache.py             # Cache configuration
│   │
│   ├── modules/
│   │   ├── gym/                 # Exercise module
│   │   │   ├── models.py        # Exercise model
│   │   │   ├── schemas.py       # ExerciseCreate / Update / Response
│   │   │   ├── service.py       # CRUD + Redis caching
│   │   │   ├── router.py        # /exercise/ endpoints
│   │   │   ├── enums.py         # MuscleGroup enum
│   │   │   └── exceptions.py    # ExerciseNotFound, AlreadyExists
│   │   │
│   │   ├── training/            # Workout module
│   │   │   ├── models.py        # Workout, WorkoutExercise, WorkoutSet
│   │   │   ├── schemas.py       # Schemas for all 3 models
│   │   │   ├── service.py       # Workout business logic
│   │   │   ├── router.py        # /training/ endpoints
│   │   │   ├── enums.py         # WorkoutStatus enum
│   │   │   └── exceptions.py
│   │   │
│   │   └── user/                # User module
│   │       ├── models.py        # User model
│   │       ├── schemas.py       # UserCreate / Response, Token
│   │       ├── service.py       # Registration, authentication
│   │       ├── router.py        # /user/register, /user/login
│   │       └── exceptions.py
│   │
│   └── main.py                  # App entry point, lifespan, router registration
│
├── alembic/                     # Database migrations
│   └── versions/
│       ├── d9ee1d232830_initial_create.py
│       ├── 7b399ebc26f7_tz_aware_datetimes.py
│       └── afb9c94ffffb_added_user_roles.py
│
├── test/
│   ├── conftest.py              # Fixtures: in-memory SQLite, async test client
│   └── test_exercises.py        # Exercise endpoint tests
│
├── Dockerfile                   # Python 3.12 slim + uv build
├── docker-compose.yml           # app + PostgreSQL 15 + Redis
├── pyproject.toml               # Project metadata and dependencies
├── alembic.ini                  # Alembic configuration
└── test_main.http               # HTTP scratch file for manual testing
```

---

## 🗄 Data Models

### User
```
id            int       Primary key
email         str       Unique, max 50 chars
password_hash str       Argon2 hash
role          str       "user" | "admin"  (default: "user")
created_at    datetime  Server-side timestamp
workouts      →         One-to-many → Workout (cascade delete)
```

### Exercise
```
id            int          Primary key
name          str          Unique, max 150 chars
description   str?         Optional, max 1000 chars
muscle_group  MuscleGroup  chest | back | legs | arms | shoulders | cardio
```

### Workout
```
id            int           Primary key
user_id       int           FK → users.id
name          str           Max 100 chars
scheduled_at  datetime?     Timezone-aware planned date
status        WorkoutStatus planned | completed | skipped
notes         str?          Max 500 chars
exercises     →             One-to-many → WorkoutExercise
```

### WorkoutExercise
```
id            int   Primary key
workout_id    int   FK → workouts.id
exercise_id   int   FK → exercises.id
order         int   Execution order (default 0)
sets          →     One-to-many → WorkoutSet
```

### WorkoutSet
```
id                    int    Primary key
workout_exercise_id   int    FK → workout_exercises.id
reps                  int    Number of repetitions (≥ 1)
weight                float  Weight in kg (≥ 0.0)
set_number            int    Set number (≥ 1)
```

---

## 🔌 API Endpoints

### 👤 Users — `/user`

| Method | URL | Description | Access |
|--------|-----|-------------|--------|
| `POST` | `/user/register` | Register a new user | Public |
| `POST` | `/user/login` | Login and receive JWT token | Public |

### 🏃 Exercises — `/exercise`

| Method | URL | Description | Access |
|--------|-----|-------------|--------|
| `GET` | `/exercise/` | List all exercises | Public |
| `GET` | `/exercise/{id}` | Get exercise by ID | Public |
| `POST` | `/exercise/` | Create a new exercise | Admin only |
| `PATCH` | `/exercise/{id}` | Update an exercise | Admin only |
| `DELETE` | `/exercise/{id}` | Delete an exercise | Admin only |

### 📅 Workouts — `/training`

| Method | URL | Description | Access |
|--------|-----|-------------|--------|
| `GET` | `/training/workouts` | List user workouts (cursor pagination) | Authenticated |
| `GET` | `/training/workouts/{id}` | Get workout by ID | Authenticated |
| `POST` | `/training/workouts` | Create a new workout | Authenticated |
| `PATCH` | `/training/workouts/{id}` | Update workout info | Authenticated |
| `DELETE` | `/training/workouts/{id}` | Delete a workout | Authenticated |

### 💪 Workout Exercises — `/training`

| Method | URL | Description | Access |
|--------|-----|-------------|--------|
| `POST` | `/training/workouts/{id}/exercises` | Add exercise to workout | Authenticated |
| `PATCH` | `/training/exercises/{id}` | Update exercise order | Authenticated |
| `DELETE` | `/training/exercises/{id}` | Remove exercise from workout | Authenticated |

### 📊 Workout Sets — `/training`

| Method | URL | Description | Access |
|--------|-----|-------------|--------|
| `POST` | `/training/exercises/{id}/sets` | Add a set | Authenticated |
| `PATCH` | `/training/sets/{id}` | Update a set | Authenticated |
| `DELETE` | `/training/sets/{id}` | Delete a set | Authenticated |

> 📖 Full interactive docs available at **`http://localhost:8000/docs`** (Swagger UI) and **`http://localhost:8000/redoc`** (ReDoc) after starting the server.

---

## 🚀 Quick Start

### Option 1: Docker Compose (recommended)

```bash
# 1. Clone the repository
git clone https://github.com/100kgtrotila/workout-tracker.git
cd workout-tracker

# 2. Create your .env file (see Environment Variables below)
cp .env.example .env

# 3. Start all services
docker compose up --build

# 4. Apply database migrations
docker compose exec app alembic upgrade head
```

The API will be available at **`http://localhost:8000`**

### Option 2: Local Development with uv

```bash
# 1. Clone the repository
git clone https://github.com/100kgtrotila/workout-tracker.git
cd workout-tracker

# 2. Install uv (if not already installed)
curl -Lf https://astral.sh/uv/install.sh | sh

# 3. Install dependencies
uv sync

# 4. Set up environment variables
cp .env.example .env   # fill in your values

# 5. Apply migrations
uv run alembic upgrade head

# 6. Run the development server
uv run uvicorn app.main:app --reload
```

---

## 🔧 Environment Variables

Create a `.env` file in the project root:

```env
# Database
DATABASE_URL=postgresql+asyncpg://user:password@localhost:5432/workout_db

# Redis
REDIS_URL=redis://localhost:6379/0

# JWT
SECRET_KEY=your-secret-key-at-least-32-characters-long
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

> ⚠️ When using Docker Compose, `DATABASE_URL` and `REDIS_URL` are pre-configured in `docker-compose.yml` using internal service names. You only need to change `SECRET_KEY`.

---

## 🗃 Database Migrations

This project uses **Alembic** for schema version control.

```bash
# Apply all pending migrations
alembic upgrade head

# Roll back the last migration
alembic downgrade -1

# Auto-generate a new migration from model changes
alembic revision --autogenerate -m "describe your change"

# View migration history
alembic history
```

### Migration History

| Revision | Description |
|----------|-------------|
| `d9ee1d232830` | Initial schema — users, exercises, workouts, sets |
| `7b399ebc26f7` | Timezone-aware datetime columns |
| `afb9c94ffffb` | Added user roles |

---

## 🧪 Testing

Tests use an **in-memory SQLite** database — no external services needed.

```bash
# Run all tests
uv run pytest

# Verbose output
uv run pytest -v

# Run a specific file
uv run pytest test/test_exercises.py
```

The test suite uses:
- **pytest-asyncio** for async test support
- **httpx AsyncClient** for HTTP requests against the ASGI app
- **aiosqlite** as a lightweight in-memory test database
- **Dependency overrides** to bypass authentication during tests

---

## 🔐 Security

### Password Hashing
Passwords are hashed with **Argon2** via `pwdlib` — one of the strongest modern hashing algorithms, resistant to brute-force and GPU-based attacks.

### JWT Authentication
Tokens are signed with **HS256** and expire after a configurable period (default: 30 minutes). Protected routes require a valid `Bearer` token in the `Authorization` header.

### Role-Based Access Control (RBAC)
The `RoleChecker` dependency restricts endpoints to specific roles:

```python
# Only admins can create exercises
@router.post("/", dependencies=[Depends(admin_only)])
async def create_exercise(...):
    ...
```

### Timing-Safe Login
A `DUMMY_HASH` is computed at startup to ensure that login attempts for non-existent users take the same amount of time as valid ones, preventing user enumeration via timing attacks.

---

## 📄 License

This project is open source and available under the [MIT License](LICENSE).

---

<div align="center">

Built with ❤️ using **FastAPI** · **PostgreSQL** · **Redis** · **Docker**

🔗 **[https://github.com/100kgtrotila/workout-tracker](https://github.com/100kgtrotila/workout-tracker)**  
📋 **[https://roadmap.sh/projects/fitness-workout-tracker](https://roadmap.sh/projects/fitness-workout-tracker)**

</div>