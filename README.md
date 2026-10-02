# Expense Predictor Application

Full-stack app to log expenses, run ML-based monthly forecasts, and review spending history. Built with React, Flask, and PostgreSQL.

## Features

- Log expenses by category and month
- Predict category-wise spending from budget and lifestyle inputs
- Save predictions to the database
- Home dashboard with recent expenses and saved predictions
- Monthly category summary

## Tech stack

| Layer | Stack |
|-------|--------|
| Frontend | React 18, React Router |
| Backend | Flask, SQLAlchemy, scikit-learn (joblib models) |
| Database | PostgreSQL |

## Prerequisites

- Node.js 18+ and npm
- Python 3.10+
- PostgreSQL 14+

## Database setup

1. **Create an empty database** (example name `expense_app`):

   ```sh
   createdb expense_app
   ```

   Or in `psql`:

   ```sql
   CREATE DATABASE expense_app;
   ```

2. **Configure the backend** — copy the example env file and edit credentials:

   ```sh
   cd backend
   cp .env.example .env
   ```

   Set `DATABASE_URL` in `.env`:

   ```env
   DATABASE_URL=postgresql://YOUR_USER:YOUR_PASSWORD@localhost:5432/expense_app
   ```

3. **Tables on startup** — when the Flask app starts, it runs `db.create_all()` and creates missing tables (`expenses`, `predictions`, etc.).

4. **Optional: migrations** — for existing databases that already used Alembic:

   ```sh
   cd backend
   export FLASK_APP=app.py
   flask db upgrade
   ```

### Environment variables (backend)

| Variable | Description | Default |
|----------|-------------|---------|
| `DATABASE_URL` | PostgreSQL connection string | `postgresql://postgres:postgres@localhost:5432/expense_app` |
| `FRONTEND_URL` | Allowed CORS origin in production | `http://localhost:3000` |
| `CORS_PERMISSIVE` | Set to `1` to allow all origins (local dev) | unset |
| `PORT` | HTTP port | `5000` |

Heroku-style `postgres://` URLs are normalized to `postgresql://` automatically.

## Backend setup and run

```sh
cd backend
python -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env       # then edit DATABASE_URL
```

ML model files must exist under `backend/models3/` (e.g. `Food_model.pkl`). Run training scripts in the repo if needed.

Start the server **from the `backend` directory**:

```sh
python app.py
```

Health check: `GET http://localhost:5000/api/health`

### API overview

| Method | Path | Purpose |
|--------|------|---------|
| GET | `/api/health` | App and DB status |
| GET | `/api/dashboard` | Recent expenses and predictions (home page) |
| GET/POST | `/api/expenses` | List or create expenses |
| GET | `/api/expenses/monthly-summary` | Totals by category for month/year |
| POST | `/api/predict-category` | ML forecast |
| POST/GET | `/api/predictions/save-prediction`, `get-prediction`, etc. | Persist forecasts |

`GET /api/x` remains as a deprecated alias for listing expenses.

## Frontend setup and run

```sh
cd frontend
npm install
cp .env.example .env
```

Set in `.env`:

```env
REACT_APP_API_BASE_URL=http://localhost:5000
```

```sh
npm start
```

Open [http://localhost:3000](http://localhost:3000).

### Routes

| Path | Page |
|------|------|
| `/` | Home — usage history |
| `/log-expense` | Log a new expense |
| `/prediction` | Run and save ML prediction |
| `/expenses` | All expenses |
| `/summary` | Monthly breakdown |

## Production notes

- Root [`Procfile`](Procfile) uses `gunicorn backend.app:app` from the repo root; ensure `DATABASE_URL` is set and the process can load `backend/models3/`.
- Restrict CORS with `FRONTEND_URL` and avoid `CORS_PERMISSIVE` in production.

## License

MIT
