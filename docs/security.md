# Security Documentation — todoapp (Flask Secure To-Do App)

## 1. Overview

This project is a beginner-friendly CI/CD + DevSecOps starter. It includes:

- A Flask To-Do web application using SQLite (CRUD + filters + edit).
- A CI pipeline (GitHub Actions) that runs tests and security scans.
- Docker containerization and publishing the image to GitHub Container Registry (GHCR).

This document explains:

- What security controls were implemented in the application.
- How secrets are handled.
- How security scanning is integrated into CI.
- What the scans reported and how findings were handled.

---

## 2. Threat Model (Simple)

**Assets**

- Task data stored in SQLite.
- Source code and dependency integrity.
- CI pipeline integrity and build artifacts (Docker image).

**Main risks**

- User input abuse (empty/overlong input, injection attempts).
- Vulnerable dependencies.
- Insecure container image configuration.
- Accidental secrets leakage into source control.

**Out of scope (for this simplified version)**

- Full authentication/authorization (optional/bonus feature).
- Multi-tenant security controls.
- Advanced monitoring, WAF, or Kubernetes security.

---

## 3. Application Security Controls

### 3.1 Input validation

The application validates task titles:

- Rejects empty task titles.
- Applies a maximum length limit to reduce abuse and unexpected behavior.

This reduces risks related to:

- Excessive payload sizes / UI rendering issues.
- Storing unexpected large data.

### 3.2 SQL injection prevention

Database queries use parameterized statements (prepared queries) rather than string concatenation.
This mitigates SQL injection risks when interacting with SQLite.

### 3.3 Error handling (basic)

For invalid requests (e.g., empty title, missing record), the application returns appropriate errors (e.g., 400/404).
This avoids ambiguous behavior and reduces the chance of inconsistent state.

### 3.4 Secrets and configuration

- No secrets are hardcoded in source code.
- A `.env.example` file documents required environment variables.
- `.env` is excluded from git via `.gitignore`.

**Current usage**

- `SECRET_KEY` is read from environment variables (or a safe development fallback).
- Database path can be configured via environment variables.

---

## 4. Repository Hygiene and Secret Management

### 4.1 Prevent committing secrets

Controls implemented:

- `.gitignore` excludes `.env` and typical local artifacts.
- `.dockerignore` excludes `.env`, `.venv`, `.git/`, and local DB files.

This reduces the chance of:

- Leaking secrets to GitHub.
- Shipping local-only files into Docker images.

### 4.2 CI permissions

GitHub Actions uses least-privilege permissions needed for this project:

- `contents: read`
- `packages: write` (to publish the image to GHCR)

The pipeline authenticates to GHCR using `GITHUB_TOKEN` (GitHub-managed token), avoiding storing registry passwords in the repo.

---

## 5. CI/CD Security (DevSecOps Integration)

## 5.1 Pipeline location

Workflow file:

- `.github/workflows/cicd.yml`

## 5.2 Pipeline stages

1. **Build & Test**

- Install dependencies
- Run automated tests (`pytest`)

2. **Static code scan (Bandit)**

- Scans Python code for common insecure patterns.

3. **Dependency vulnerability scan (pip-audit)**

- Scans Python dependencies for known vulnerabilities.

4. **Docker build & publish**

- Builds Docker image using `Dockerfile`
- Pushes to GHCR:
  - `ghcr.io/amanj20/todo-app:latest`
  - `ghcr.io/amanj20/todo-app:<commit-sha>`

5. **Container image scan (Trivy)**

- Scans the pushed image for OS/package vulnerabilities.
- Produces a report artifact.

## 5.3 Reports and artifacts

GitHub Actions uploads JSON reports as artifacts:

- `bandit.json`
- `pip-audit.json`
- `trivy.json`

**Note:** In this beginner configuration, scans generate reports but do not fail the build (report-only mode). This is useful for learning and grading evidence. In a stricter setup, HIGH/CRITICAL findings would fail the pipeline.

---

## 6. Security Scan Results (Summary)

Fill these sections using your downloaded artifacts from GitHub Actions.

### 6.1 Bandit (code scan)

- Result summary: [e.g., “No high severity findings” / “X medium findings”]
- Notes / actions taken:
  - [Example: “Reviewed finding Bxxx; accepted as low risk for this demo”]
  - [Example: “Adjusted code to avoid insecure pattern”]

### 6.2 pip-audit (dependencies)

- Result summary: [e.g., “No known vulnerabilities” / “Found X vulnerabilities”]
- Notes / actions taken:
  - [Example: “Updated package versions in requirements.txt”]
  - [Example: “Pinned dependency version”]

### 6.3 Trivy (container scan)

- Result summary (HIGH/CRITICAL): [e.g., “0 critical, 1 high”]
- Notes / actions taken:
  - [Example: “Rebuilt image after dependency updates”]
  - [Example: “Base image kept updated”]

---
