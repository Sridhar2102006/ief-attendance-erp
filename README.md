# IEF Attendance ERP

Offline-first attendance and Micro ERP project.

## Project structure

```text
ief-attendance-erp/
├── apps/
│   ├── admin-web/
│   ├── api/
│   └── verifier-pwa/
├── infrastructure/
├── .env
├── .env.example
├── .gitignore
├── docker-compose.yml
└── README.md
```

The application directories are reserved for the admin web app, API, and
verifier PWA. The local Compose setup currently defines PostgreSQL, Redis, and
Mailpit services on the `ief-network` Docker network.

## Local environment

Copy `.env.example` to `.env` and replace the password placeholders with
local-only credentials. Never commit `.env`.

Start the local services with:

```powershell
docker compose up -d
```

The Mailpit web inbox is available at <http://127.0.0.1:8025>. PostgreSQL and
Redis are only exposed to containers on `ief-network`.
