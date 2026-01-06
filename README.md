[![CI-CD](https://github.com/amanj20/todoapp/actions/workflows/cicd.yml/badge.svg)](https://github.com/amanj20/todoapp/actions/workflows/cicd.yml)
# todoapp

A simple Flask To-Do List web application (CRUD) with basic DevSecOps practices:
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
Activate (PowerShell):

powershell
Copy code
.\.venv\Scripts\Activate.ps1
Activate (CMD):

bat
Copy code
.\.venv\Scripts\activate.bat
2) Install dependencies
bash
Copy code
python -m pip install --upgrade pip
pip install -r requirements.txt
3) Run the app
bash
Copy code
python app.py
Open in browser:
http://127.0.0.1:5000

Run with Docker (Local)
1) Build the image
bash
Copy code
docker build -t todo-app:local .
2) Run the container
bash
Copy code
docker run -p 5000:5000 todo-app:local
Open in browser:
http://localhost:5000

Run from GitHub Container Registry (GHCR)
Pull the latest image:

bash
Copy code
docker pull ghcr.io/amanj20/todo-app:latest
Run:

bash
Copy code
docker run -p 5000:5000 ghcr.io/amanj20/todo-app:latest
Open in browser:
http://localhost:5000

Run Tests
bash
Copy code
pytest -q
Security Scans (Local)
Bandit (code scan):

bash
Copy code
bandit -r . -x .venv,tests
Dependency scan:

bash
Copy code
pip-audit -r requirements.txt
CI/CD Pipeline (GitHub Actions)
Workflow file:

.github/workflows/cicd.yml

Pipeline stages:

Build & Test

Install dependencies

Run pytest

Security Scanning

Bandit (code)

pip-audit (dependencies)

Upload reports as workflow artifacts

Docker Build & Publish

Build Docker image

Push to GHCR

Container Security Scan

Trivy scan on pushed image

Upload Trivy report as artifact

Artifacts generated:

bandit.json

pip-audit.json

trivy.json

Docker image published to:

ghcr.io/amanj20/todo-app:latest

ghcr.io/amanj20/todo-app:<commit-sha>