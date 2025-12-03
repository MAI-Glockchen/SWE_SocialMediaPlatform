# SWE_SocialMediaPlatform
**Team:** Andreas Wallnöfer, Armin Lohse

Simple social media platform built as an exercise to understand and use software engineering concepts.

# Branching Model & Workflow

This project uses a **Git Flow-inspired branching model** with enforced CI/CD and review policies.

---

## Branches

| Branch       | Purpose                   | Rules |
|--------------|---------------------------|-------|
| `main`       | Production / Release      | - Only pull requests from `feature/**` branches <br> - CI (`build-test`) and `WorkTimeLog.txt` check must pass <br> - Direct pushes prohibited |
| `feature/**` | New features              | - Local development <br> - Merge only via PR to `main` <br> - Pre-commit hooks must pass locally |

---

## Merge Rules

- **Feature → Main**  
  - Always via Pull Request  
  - CI (Tests + Lint) must pass  
  - `WorktimeLog.txt` must be updated  
  - Local pre-commit hooks must pass  
  - Direct push to `main` is prohibited  

---

## GitHub Actions & CI

- **Pre-commit (`pre-commit-config.yaml`)**  
  - Runs before commit  
  - Code formatting (Black)  
  - Import order (isort)  

- **CI Workflow (`ci.yml`)**  
  - Runs on pull requests targeting `main`
  - Installs dependencies via `uv`  
  - Lints code (flake8)  
  - Runs tests (pytest)
  - Checks that `WorkTimeLog.txt` has been modified  
  - Ensures CI (`build-test`) passes before merge  
  - **Note:** Black and isort are handled locally via pre-commit  

> Only when all checks pass can a feature branch be merged into `main`.

---

## Pre-Commit Hooks (Recommended)

Pre-commit hooks automatically run **before every commit**, so you do **not** need to run Black or isort manually.  
They ensure your code is formatted correctly and imports are sorted before it reaches the repository.

Checks performed locally via pre-commit:

- Code formatting (Black)
- Import order (isort)
- Lint (flake8)

**Installation and first-time setup:**

```bash
pip install pre-commit
pre-commit install
pre-commit run --all-files
```

---

# Running the Application

This project consists of a **Python backend** and an **Angular frontend**.

---

## Backend (Python / FastAPI)
The backend lives in the `backend/` directory.

### Requirements

- Python 3.12+
- `uv` or `poetry`

From the repository root:

```bash
poetry install
```
or the respective uv command.

### Start backend

From the repository root:

```bash
poetry run uvicorn backend.main:app --reload
```
or the respective uv command.

Backend runs at:
http://localhost:8000


### Run backend tests

```bash
cd backend
poetry run pytest
```
or the respective uv command.

### Backend Docker Image

The backend is containerized and automatically built via GitHub Actions when merging into `main`.
Docker images are pushed to GitHub Container Registry at:

ghcr.io/mai-glockchen/swe-social-backend:sha


with tags for the commit SHA and latest (for main branch pushes).

You can pull and run the image locally:

docker pull ghcr.io/<owner>/swe-social-backend:latest
docker run -p 8000:8000 ghcr.io/<owner>/swe-social-backend:latest


This will run the backend FastAPI app on localhost:8000.


---

# Frontend (Angular 21 + Vitest)

Located in the `frontend/` directory.

## Requirements

- Node 20+
- npm 10+

Install all packages:

```bash
cd frontend
npm install
```

---

## Start Angular frontend

```bash
npm start
```

Runs at:
http://localhost:4200



---

## Run frontend tests (Vitest)

Vitest is fully set up with Angular-compatible mocks (no TestBed required).

Run all tests:

```bash
npx vitest
```

Watch mode:

```bash
npx vitest --watch
```

Single file:

```bash
npx vitest src/app/components/landing/landing.component.spec.ts
```


---

# Notes for Developers

- Frontend uses standalone Angular components and Vitest.  
- You **do not** need Zone.js or Angular TestBed.  
- API URL for local dev defaults to `http://localhost:8000`.

---
