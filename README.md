# SWE_SocialMediaPlatform
Simple social media platform built as an exercise to understand and use software engineering concepts.

# Branching Model & Workflow

This project uses a **Git Flow-inspired branching model** with enforced CI/CD and review policies.

---

## 1️⃣ Branches

| Branch       | Purpose                   | Rules |
|--------------|---------------------------|-------|
| `main`       | Production / Release      | - Only pull requests from `develop` <br> - CI (`build-test`) and `WorktimeLog.txt` check must be filled out with the time that you spent on this feature <br> - Direct pushes prohibited |
| `develop`    | Integration / Testing     | - Pull requests from feature branches <br> - CI (`build-test`) must pass <br> - Direct pushes prohibited |
| `feature/**` | New features  | - Local development <br> - Merge only via PR to `develop` <br> - Pre-commit hooks must pass locally |

---

## 2️⃣ Merge Rules

- **Feature → Develop**  
  - Always via Pull Request  
  - CI (Tests + Lint) must pass  
  - Local pre-commit hooks must be clean  

- **Develop → Main**  
  - Only via Pull Request  
  - CI must pass (`build-test`)  
  - `WorktimeLog.txt` must be updated  
  - Direct push to `main` is prohibited  

- **Feature → Main**  
  - ❌ Not allowed  

---

## 3️⃣ GitHub Actions & CI

- **CI Workflow (`ci.yml`)**  
  - Runs on `feature/**` and `develop` branches  
  - Installs dependencies via `uv`  
  - Checks code style with **Black** and **isort**  
  - Lints code (flake8)  
  - Runs tests (pytest)  

- **Deploy/Check Workflow (`deploy.yml`)**  
  - Runs on pull requests targeting `main`  
  - Ensures CI (`build-test`) passes  
  - Checks that `WorkTimeLog.txt` has been modified  

> Only when all checks pass can `develop` be merged into `main`.

---

## 4️⃣ Pre-Commit Hooks

- Local pre-commit hooks must run before committing:  
  - Lint (flake8)  
  - Code formatting (Black)  
  - Import order (isort)  
  - Optional: run tests  

**Installation:**
```bash
pip install pre-commit
pre-commit install
pre-commit run --all-files
