# Implementation Plan — Sage Provider Simulator v0.1.0

**Version:** 0.1.0
**Status:** Draft
**Date:** 2026-09-08
**Specification:** [spec.md](spec.md)
**Constitution:** [constitution.md](../../.specify/memory/constitution.md)

---

## 1. Project Structure

```
sage-provider-simulator/
├── app/
│   ├── __init__.py          # Application factory (create_app)
│   ├── config.py            # Configuration from environment
│   ├── blueprints/
│   │   ├── __init__.py
│   │   ├── health.py        # GET /health
│   │   └── invoices.py      # GET /api/v1/invoices
│   ├── auth.py              # X-API-Key middleware/decorator
│   └── errors.py            # JSON error handlers
├── fixtures/
│   └── invoices.json        # Static fixture invoice data
├── tests/
│   ├── __init__.py
│   ├── conftest.py          # Test fixtures and app client
│   ├── test_health.py       # Health endpoint tests
│   ├── test_auth.py         # Authentication tests
│   ├── test_invoices.py     # Invoice retrieval tests
│   └── test_errors.py       # Error scenario tests (500)
├── Dockerfile
├── requirements.txt
├── pyproject.toml            # Ruff config, project metadata
├── README.md
├── .env.example
├── .gitignore
├── GEMINI.md
├── AGENTS.md
├── .specify/memory/constitution.md
└── specs/v0.1.0/
    ├── spec.md
    ├── plan.md
    └── tasks.md
```

---

## 2. Technology Stack

| Component | Choice | Rationale |
|---|---|---|
| Framework | Flask 3.x | Lightweight, matches ecosystem spec |
| Auth | X-API-Key via decorator | Simple, deterministic |
| Data | Static JSON fixtures | No database needed (SIM-001) |
| Testing | pytest + Flask test client | Fast, deterministic |
| Linting | Ruff | Fast, comprehensive |
| Container | Docker (python:3.12-slim) | Reproducible builds |
| CI | GitHub Actions | Ruff + pytest + Docker build |

---

## 3. Endpoint Design

### 3.1 Public Endpoints

| Method | Path | Auth | Response |
|---|---|---|---|
| GET | `/health` | None | `200 {"status": "ok"}` |

### 3.2 Authenticated Endpoints

| Method | Path | Auth | Response |
|---|---|---|---|
| GET | `/api/v1/invoices` | X-API-Key | `200` with invoice array |

### 3.3 Error Responses

| Trigger | Status | Body |
|---|---|---|
| Missing/invalid X-API-Key | 401 | `{"error": "Unauthorized", "message": "..."}` |
| `?simulate_error=500` | 500 | `{"error": "Internal Server Error", "message": "..."}` |
| `?simulate_error=429` (P1a) | 429 | `{"error":"Too Many Requests","message":"Simulated rate limit exceeded. Please retry after 5 seconds."}` + `Retry-After: 5` header |

### 3.4 Invoice Response Schema

The invoice response schema and P1a simulator extensions are governed by the
canonical contract in `integration-workspace/docs/contracts/invoice-sync-v0.1.md`,
merged into `develop` at commit `1b481345748f7b66084ade31231d0bf146013c4a`.
Both the Flask provider and the FastAPI consumer follow this versioned
workspace contract baseline.

---

## 4. Authentication Design

- X-API-Key is read from the `PROVIDER_API_KEY` environment variable.
- A `@require_api_key` decorator validates the `X-API-Key` header.
- Applied only to the `/api/v1/` Blueprint.
- `GET /health` bypasses authentication.

---

## 5. Test Strategy (Test-First)

| Test File | Scope | Priority |
|---|---|---|
| `test_health.py` | `GET /health` returns 200, correct JSON | P0 |
| `test_auth.py` | 401 without key, 401 with bad key, 200 with valid key | P0 |
| `test_invoices.py` | invoice response/schema and fixtures; pagination defaults, slicing, metadata, beyond-final-page behavior; invalid and duplicate pagination parameters; authentication-before-validation precedence | P0 |
| `test_errors.py` | deterministic `simulate_error=500` and `simulate_error=429`; exact 429 JSON response and `Retry-After: 5`; authentication requirements; simulation-before-pagination-validation precedence | P0 |

All tests use the Flask test client. No external services required.
Tests are written before implementation (red → green → refactor).

---

## 6. Dockerfile Plan

```dockerfile
FROM python:3.12-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
EXPOSE 5000
CMD ["python", "-m", "flask", "--app", "app", "run", "--host", "0.0.0.0", "--port", "5000"]
```

---

## 7. CI Plan

GitHub Actions workflow (`.github/workflows/ci.yml`):

1. **Lint:** `ruff check .`
2. **Test:** `pytest -v`
3. **Build:** `docker build -t sage-provider-simulator .`

Triggers: push and PR to `develop`.

---

## 8. Gitflow Workflow

```mermaid
gitgraph
    commit id: "initial commit"
    branch develop
    commit id: "docs: spec and bootstrap"
    branch feature/flask-health
    commit id: "test: health endpoint"
    commit id: "feat: health endpoint"
    checkout develop
    merge feature/flask-health
    branch feature/flask-invoices
    commit id: "test: auth and invoices"
    commit id: "feat: auth, invoices, 500"
    checkout develop
    merge feature/flask-invoices
    branch feature/dockerfile-ci
    commit id: "build: Dockerfile"
    commit id: "ci: GitHub Actions"
    checkout develop
    merge feature/dockerfile-ci
    branch release/v0.1.0
    commit id: "chore: release prep"
    checkout main
    merge release/v0.1.0 tag: "v0.1.0"
    checkout develop
    merge release/v0.1.0
```

---

## 9. Implementation Order

After all gates pass, the recommended implementation order is:

1. **Tests first:** `test_health.py` (red).
2. **Health endpoint:** `GET /health`, app factory, Blueprint. Tests go green.
3. **Tests first:** `test_auth.py`, `test_invoices.py` (red).
4. **Auth + invoices:** X-API-Key decorator, fixture loading, invoice endpoint. Tests go green.
5. **Tests first:** `test_errors.py` (red).
6. **Error scenarios:** `?simulate_error=500` handler. Tests go green.
7. **Dockerfile:** Build and verify container starts.
8. **CI workflow:** Ruff + pytest + Docker build.
9. **README:** Setup, usage, and contract reference.

> Browser UI (FR-206) remains deferred to P1.
> Pagination (FR-203) and 429 error simulation (FR-204) were implemented as a
> combined P1a extension on `feature/p1a-pagination-and-429`.

### 9.1 P1a Simulator Extension Implementation Status

- **Branch:** `feature/p1a-pagination-and-429` (single combined feature branch)
- **Implementation Commit:** `c62b6e9e4ea3ee26478307bbd78089214ba8786f`
- **Contract Baseline:** Merged into `integration-workspace/develop` at commit
  `1b481345748f7b66084ade31231d0bf146013c4a` (`docs/contracts/invoice-sync-v0.1.md`).
- **Sequencing Note:** The workspace contract amendment was merged after the
  simulator implementation existed, and now governs its merge criteria.
- **Local Test Evidence:**
  - `pytest -v`: 32 passed in 1.01s.
  - `ruff check .`: passed.
- **Pending Merge Gates:**
  - No simulator PR has been created or reviewed yet.
  - No simulator merge has occurred.
  - No live cross-service E2E verification has happened.
  - End-to-end Compose verification remains required before simulator merge and
    is not performed by this documentation-only task.

---

## 10. Risks and Trade-Offs

| Decision | Trade-Off |
|---|---|
| Static fixtures, no DB | Simpler but less flexible; acceptable for P0 |
| Response schema deferred to contract | Fixture shape finalized only after workspace contract is approved |
| Ruff over flake8/black | Faster, single tool; acceptable for this project size |
