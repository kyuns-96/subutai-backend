# Subutai Backend

FastAPI backend for the Subutai Playground — data analysis dashboard with JWT authentication and per-user DoE setup management.

## Tech Stack

| Layer | Stack |
|-------|-------|
| Framework | FastAPI |
| Database | MySQL 8.0 |
| ORM | SQLAlchemy 2.0 (async) |
| Migrations | Alembic |
| Auth | JWT (python-jose), bcrypt (passlib) |
| Validation | Pydantic v2 |
| Runtime | Python 3.11+, uv |

## Quick Start

### Prerequisites

- Python 3.11+
- [uv](https://docs.astral.sh/uv/)
- Docker (for MySQL)

### Setup

```bash
# Clone
git clone https://github.com/kyuns-96/subutai-backend.git
cd subutai-backend

# Install dependencies
uv sync

# Configure environment
cp .env.example .env
# Edit .env: set SUBUTAI_JWT_SECRET to a secure random string

# Start MySQL
docker compose up -d

# Run migrations
uv run alembic upgrade head
```

### Run

```bash
uv run uvicorn app.main:app --reload
```

| Service | URL |
|---------|-----|
| API | http://localhost:8000 |
| Docs | http://localhost:8000/docs |

## API Endpoints

### Auth (`/api/v1/auth`)

| Method | Path | Description |
|--------|------|-------------|
| POST | `/register` | Create account |
| POST | `/login` | Get JWT access token |
| GET | `/me` | Get current user (requires auth) |

### DoE Setups (`/api/v1/doe-setups`)

All endpoints require `Authorization: Bearer <token>` header. Data is scoped to the authenticated user.

| Method | Path | Description |
|--------|------|-------------|
| GET | `/` | List saved setups |
| POST | `/` | Create setup |
| PUT | `/:id` | Update setup |
| DELETE | `/:id` | Delete setup |

## Environment Variables

| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| `SUBUTAI_JWT_SECRET` | Yes | — | JWT signing secret |
| `SUBUTAI_DATABASE_URL` | No | `mysql+asyncmy://root:rootpassword@localhost:3306/subutai?charset=utf8mb4` | Database connection |
| `SUBUTAI_CORS_ORIGINS` | No | `["http://localhost:5173"]` | Allowed CORS origins |
| `SUBUTAI_ENV` | No | `development` | Environment |
| `SUBUTAI_ACCESS_TOKEN_EXPIRE_MINUTES` | No | `30` | JWT token lifetime |

## Testing

```bash
# Start MySQL first
docker compose up -d

# Run tests
uv run pytest -v
```

## Related Projects

- [kyuns-96/shadcn_project](https://github.com/kyuns-96/shadcn_project) — Frontend (React + TypeScript)
