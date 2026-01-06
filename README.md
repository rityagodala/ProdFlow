# ProdFlow

A production-grade, full-stack Projects & Tasks management platform demonstrating real-world engineering practices, clean architecture, and DevOps workflows.

## Overview

ProdFlow is a cloud-ready application that enables users to manage projects and tasks efficiently. It showcases:

- **Clean Backend Architecture**: FastAPI with clear separation of concerns (routers, services, models, schemas)
- **Modern Frontend**: Next.js 14 with TypeScript and Tailwind CSS
- **Production Practices**: Docker containerization, CI/CD pipelines, database migrations
- **Type Safety**: Strong typing throughout the stack
- **Testing**: Unit tests for core backend functionality

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                         Frontend                             │
│  Next.js 14 + TypeScript + Tailwind CSS                     │
│  - Login/Register Pages                                      │
│  - Dashboard (Projects List)                                 │
│  - Project Detail (Tasks CRUD)                               │
└──────────────────────┬──────────────────────────────────────┘
                       │ HTTP/REST
                       │
┌──────────────────────▼──────────────────────────────────────┐
│                         Backend                              │
│  FastAPI + SQLAlchemy + Alembic                             │
│  - Authentication (JWT)                                      │
│  - Projects CRUD                                             │
│  - Tasks CRUD                                                │
└──────────────────────┬──────────────────────────────────────┘
                       │
┌──────────────────────▼──────────────────────────────────────┐
│                      PostgreSQL                              │
│  - Users Table                                               │
│  - Projects Table                                            │
│  - Tasks Table                                               │
└─────────────────────────────────────────────────────────────┘
```

## Tech Stack

### Frontend
- **Next.js 14** (App Router)
- **TypeScript**
- **Tailwind CSS**
- **Axios** (HTTP client)

### Backend
- **FastAPI** (Python 3.11)
- **SQLAlchemy** (ORM)
- **Alembic** (Migrations)
- **JWT** (Authentication)
- **Pydantic** (Data validation)

### Database
- **PostgreSQL 15**

### DevOps
- **Docker** + **docker-compose**
- **GitHub Actions** (CI/CD)
- **Ruff** (Linting)
- **MyPy** (Type checking)
- **Pytest** (Testing)

## Features

### Authentication
- User registration with email and password
- JWT-based authentication
- Protected API routes
- Secure password hashing (bcrypt)

### Projects Management
- Create, read, update, delete projects
- User-specific project ownership
- Project descriptions

### Tasks Management
- Create, read, update, delete tasks within projects
- Task status: `todo`, `in_progress`, `done`
- Task assignment to users
- Task descriptions

### API Endpoints

#### Authentication
- `POST /api/v1/auth/register` - Register a new user
- `POST /api/v1/auth/login` - Login and get access token

#### Projects
- `GET /api/v1/projects` - Get all user's projects
- `POST /api/v1/projects` - Create a new project
- `GET /api/v1/projects/{id}` - Get project by ID
- `PUT /api/v1/projects/{id}` - Update a project
- `DELETE /api/v1/projects/{id}` - Delete a project

#### Tasks
- `GET /api/v1/projects/{project_id}/tasks` - Get all tasks for a project
- `POST /api/v1/projects/{project_id}/tasks` - Create a new task
- `GET /api/v1/projects/{project_id}/tasks/{task_id}` - Get task by ID
- `PUT /api/v1/projects/{project_id}/tasks/{task_id}` - Update a task
- `DELETE /api/v1/projects/{project_id}/tasks/{task_id}` - Delete a task

#### Health
- `GET /health` - Health check endpoint

## Local Development Setup

### Prerequisites
- Python 3.11+
- Node.js 20+
- PostgreSQL 15+ (or use Docker)
- Docker & Docker Compose (optional)

### Option 1: Docker Compose (Recommended)

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd ProdFlow
   ```

2. **Set up environment variables**
   ```bash
   cp backend/.env.example backend/.env
   cp frontend/.env.example frontend/.env
   ```
   Edit `.env` files with your configuration.

3. **Start all services**
   ```bash
   docker-compose up --build
   ```

   This will start:
   - PostgreSQL on port 5432
   - Backend API on port 8000
   - Frontend on port 3000

4. **Access the application**
   - Frontend: http://localhost:3000
   - Backend API: http://localhost:8000
   - API Docs: http://localhost:8000/docs

### Option 2: Local Development

#### Backend Setup

1. **Create virtual environment**
   ```bash
   cd backend
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up PostgreSQL database**
   ```bash
   createdb prodflow
   ```

4. **Configure environment**
   ```bash
   cp .env.example .env
   # Edit .env with your database URL
   ```

5. **Run migrations**
   ```bash
   alembic upgrade head
   ```

6. **Start the server**
   ```bash
   uvicorn app.main:app --reload
   ```

#### Frontend Setup

1. **Install dependencies**
   ```bash
   cd frontend
   npm install
   ```

2. **Configure environment**
   ```bash
   cp .env.example .env
   # Edit .env with your API URL
   ```

3. **Start development server**
   ```bash
   npm run dev
   ```

## Database Migrations

### Create a new migration
```bash
cd backend
alembic revision --autogenerate -m "Description of changes"
```

### Apply migrations
```bash
alembic upgrade head
```

### Rollback migration
```bash
alembic downgrade -1
```

## Running Tests

### Backend Tests
```bash
cd backend
pytest -v
```

### Frontend Tests
```bash
cd frontend
npm run lint
npm run type-check
```

## CI/CD

GitHub Actions workflows are configured for:

### Backend CI
- Runs on push/PR to `main` or `develop` branches
- Checks: Ruff linting, MyPy type checking, Pytest tests
- Location: `.github/workflows/backend-ci.yml`

### Frontend CI
- Runs on push/PR to `main` or `develop` branches
- Checks: ESLint, TypeScript type checking, Build
- Location: `.github/workflows/frontend-ci.yml`

## Project Structure

```
ProdFlow/
├── backend/
│   ├── app/
│   │   ├── api/
│   │   │   └── v1/
│   │   │       ├── endpoints/    # API route handlers
│   │   │       └── dependencies.py
│   │   ├── core/                 # Core configuration
│   │   ├── models/               # SQLAlchemy models
│   │   ├── schemas/              # Pydantic schemas
│   │   ├── services/             # Business logic
│   │   └── main.py               # FastAPI app
│   ├── alembic/                  # Database migrations
│   ├── tests/                    # Unit tests
│   ├── Dockerfile
│   ├── requirements.txt
│   └── .env.example
├── frontend/
│   ├── app/                      # Next.js app directory
│   │   ├── dashboard/            # Dashboard page
│   │   ├── login/                # Login page
│   │   ├── register/             # Register page
│   │   └── projects/             # Project detail pages
│   ├── lib/                      # Utilities
│   │   ├── api.ts                # API client
│   │   └── auth.tsx              # Auth context
│   ├── Dockerfile
│   ├── package.json
│   └── .env.example
├── .github/
│   └── workflows/                # CI/CD workflows
├── docker-compose.yml
└── README.md
```

## Environment Variables

### Backend (.env)
```env
DATABASE_URL=postgresql://user:password@localhost:5432/prodflow
SECRET_KEY=your-secret-key-change-in-production
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
CORS_ORIGINS=["http://localhost:3000"]
```

### Frontend (.env)
```env
NEXT_PUBLIC_API_URL=http://localhost:8000
```

## Future Improvements

### Monitoring & Observability
- Add application monitoring (e.g., Prometheus, Grafana)
- Implement structured logging
- Add distributed tracing
- Set up error tracking (e.g., Sentry)

### Security Enhancements
- Implement rate limiting
- Add input validation and sanitization
- Set up secrets management (e.g., AWS Secrets Manager, HashiCorp Vault)
- Implement refresh tokens
- Add password strength requirements
- Enable HTTPS in production

### Infrastructure
- Kubernetes deployment manifests
- Terraform/IaC for cloud infrastructure
- Staging and production environments
- Database backup and recovery procedures
- CDN for static assets

### Features
- Real-time updates (WebSockets)
- File attachments for tasks
- Project templates
- Task comments and activity logs
- User roles and permissions
- Project sharing and collaboration
- Search and filtering
- Export/import functionality

### Testing
- Integration tests
- End-to-end tests (Playwright/Cypress)
- Load testing
- Security testing

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is open source and available under the MIT License.

## Contact

For questions or suggestions, please open an issue in the repository.

