# IEF Attendance ERP API

FastAPI foundation for the IEF Attendance ERP. This milestone provides API and
database health endpoints plus an Alembic scaffold; it does not create ERP
tables or implement business features.

## Requirements

- Windows with the Python `py` launcher available.
- PostgreSQL reachable through the configured `DATABASE_URL` for
  `/health/db`.

The current Compose configuration does not publish PostgreSQL's port. A
backend running directly on Windows can use `localhost:5432` only after
PostgreSQL's port is explicitly published to the host. A future backend
container attached to `ief-network` should use `postgres:5432`.

## Create and activate a virtual environment

From the project root:

```powershell
py -m venv apps\api\.venv
.\apps\api\.venv\Scripts\python.exe -m pip install -r apps\api\requirements.txt
Copy-Item apps\api\.env.example apps\api\.env
```

Edit `apps\api\.env` and set `DATABASE_URL` to a reachable PostgreSQL URL. Keep
credentials local and never commit `.env`.

## Run tests

From the project root:

```powershell
.\apps\api\.venv\Scripts\python.exe -m pytest apps\api\tests
```

The database health tests use an isolated in-memory SQLite database and a
simulated query failure; they do not connect to the development PostgreSQL
database.

## Start the API

From the project root:

```powershell
.\apps\api\.venv\Scripts\python.exe -m uvicorn app.main:app --app-dir apps\api --reload
```

The API is available at `http://127.0.0.1:8000`. The health endpoints are
`GET /health` and `GET /health/db`; interactive API documentation is at
`/docs`.

## Alembic

Alembic configuration and an empty migration structure are provided. Do not
run migrations until a later milestone defines the ERP schema.
