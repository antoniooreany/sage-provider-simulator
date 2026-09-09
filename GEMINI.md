# Sage Provider Simulator — AI Agent Instructions

Read and obey these files in order:

1. `~/.gemini/GEMINI.md` — global engineering rules.
2. Parent `../GEMINI.md` — ecosystem-level boundaries.
3. Parent `../AGENTS.md` — workspace agent orchestration.
4. This file — repository-specific rules.
5. `.specify/memory/constitution.md` — project constitution.
6. Active `specs/<version>/spec.md`, `plan.md`, `tasks.md`.

## Repository Scope

This repository owns **deterministic provider simulation** only:

- Flask application factory and Blueprints.
- Static fixture invoice data (JSON).
- Authenticated `GET /api/v1/invoices` endpoint (X-API-Key).
- Public `GET /health` endpoint.
- Public local browser UI at `GET /`.
- Deterministic error scenarios (500; 429 in P1).
- Pagination support (P1).
- Dockerfile for container builds.
- Repository-level CI: Ruff lint, pytest, Docker image build.

## Prohibited Content

Do NOT place in this repository:

- Invoice normalization or sync logic (belongs in `unified-finance-integration-api`).
- Database persistence (the simulator uses static fixtures only).
- Docker Compose orchestration (belongs in `integration-workspace`).
- Real API keys, tokens, passwords, or provider credentials.
- Production deployment manifests or cloud infrastructure.
- Real Sage API compatibility or OAuth flows.

## Naming and Honesty

- This is a **local Sage-like portfolio simulator**, not an official Sage API.
- Never describe fixtures or simulated responses as production integrations.
- Never fabricate test results, deployments, CI outcomes, or releases.

## API Contract

- The provider API contract is owned by `integration-workspace`.
- This repository implements the contract; it does not define it.
- Cross-service API changes must follow the contract workflow in the workspace.

## Git Workflow

- Follow strict Gitflow: `main`, `develop`, `feature/*`, `release/*`, `hotfix/*`.
- Use Conventional Commits: `docs:`, `feat:`, `fix:`, `chore:`, `ci:`, `test:`.
- Never commit directly to `main` or `develop`.
- All changes go through Pull Requests with review.
