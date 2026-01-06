# todoapp

A simple Flask To-Do List web application with basic DevSecOps practices:
- Automated tests (pytest)
- Security scans (Bandit, pip-audit, Trivy)
- Docker containerization
- CI/CD using GitHub Actions
- Docker image published to GitHub Container Registry (GHCR)

---

## Features
- Add new tasks
- View all tasks
- Mark tasks as complete
- Edit task title
- Delete tasks
- Filter: All / Active / Completed

---

## Tech Stack
- **Backend:** Python + Flask
- **Database:** SQLite
- **Testing:** pytest
- **Container:** Docker
- **CI/CD:** GitHub Actions
- **Security Scans:** Bandit, pip-audit, Trivy
- **Registry:** GitHub Container Registry (GHCR)

---

## Run Locally (Windows)

### 1) Create & activate virtual environment
Open VS Code terminal in the project folder:

```bash
python -m venv .venv
