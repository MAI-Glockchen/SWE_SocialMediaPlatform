# SWE_SocialMediaPlatform
**Team:** Andreas Wallnöfer, Armin Lohse

Simple social media platform built as an exercise to understand and use software engineering concepts.

# Branching Model & Workflow

This project uses a **Git Flow-inspired branching model** with enforced CI/CD and review policies.

---

## 1️⃣ Branches

| Branch       | Purpose                   | Rules |
|--------------|---------------------------|-------|
| `main`       | Production / Release      | - Only pull requests from `feature/**` branches <br> - CI (`build-test`) and `WorkTimeLog.txt` check must pass <br> - Direct pushes prohibited |
| `feature/**` | New features  | - Local development <br> - Merge only via PR to `main` <br> - Pre-commit hooks must pass locally |

---

## 2️⃣ Merge Rules

- **Feature → Main**  
  - Always via Pull Request  
  - CI (Tests + Lint) must pass  
  - `WorktimeLog.txt` must be updated  
  - Local pre-commit hooks must pass  
  - Direct push to `main` is prohibited  


---

## 3️⃣ GitHub Actions & CI

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

## 4️⃣ Pre-Commit Hooks (Recommended)

Pre-commit hooks automatically run **before every commit**, so you do **not** need to run Black or isort manually. They ensure your code is formatted correctly and imports are sorted before it reaches the repository.

- Checks performed locally via pre-commit:
  - **Code formatting** (Black)
  - **Import order** (isort)
  - **Lint** (flake8)

**Installation and first-time setup:**
```bash
# Install pre-commit tool
pip install pre-commit

# Register the hooks in your git repository
pre-commit install

# Run all hooks once on all files (recommended on first setup)
pre-commit run --all-files
