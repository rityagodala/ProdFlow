# Quick Setup Guide

## Terminal Commands

### 1. Start the app with docker-compose

```bash
cd /Users/rityagodala/Desktop/ProdFlow
docker-compose up --build
```

This will:
- Build and start PostgreSQL database
- Build and start the FastAPI backend
- Build and start the Next.js frontend
- Run database migrations automatically

Access:
- Frontend: http://localhost:3000
- Backend API: http://localhost:8000
- API Docs: http://localhost:8000/docs

### 2. Run backend tests

```bash
cd /Users/rityagodala/Desktop/ProdFlow/backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
pytest -v
```

### 3. Run frontend locally (without Docker)

```bash
cd /Users/rityagodala/Desktop/ProdFlow/frontend
npm install
npm run dev
```

The frontend will be available at http://localhost:3000

### 4. Initialize git and create the first commit

```bash
cd /Users/rityagodala/Desktop/ProdFlow
git init
git add .
git commit -m "Initial commit: ProdFlow full-stack application"
```

## Additional Commands

### Run backend linting
```bash
cd backend
ruff check .
mypy app/
```

### Run frontend linting and type checking
```bash
cd frontend
npm run lint
npm run type-check
```

### Create a new database migration
```bash
cd backend
alembic revision --autogenerate -m "Description of changes"
alembic upgrade head
```

### Stop docker-compose
```bash
docker-compose down
```

### Stop docker-compose and remove volumes
```bash
docker-compose down -v
```

