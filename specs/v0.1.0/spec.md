# Specification — Sage Provider Simulator v0.1.0

**Version:** 0.1.0
**Status:** Draft
**Author:** AI Agent (Architect)
**Date:** 2026-09-08
**Constitution:** [constitution.md](../../.specify/memory/constitution.md)
**Ecosystem Spec:** [integration-workspace spec](../../../integration-workspace/specs/v0.1.0/spec.md)

---

## 1. Overview

The Sage Provider Simulator is a local Flask application that deterministically
simulates a Sage-like invoice provider. It serves fixture invoice data behind
X-API-Key authentication, provides controlled error scenarios, and exposes a
public health endpoint and browser UI.

It is a **local portfolio simulator** — not an official Sage API.

The API contract is owned by `integration-workspace`. This repository implements
that contract.

---

## 2. User Stories

### US-SIM-001: Fixture Invoice Retrieval

> As a consuming service, I want to fetch invoices from the simulator via
> `GET /api/v1/invoices` so that I can test sync and normalization logic.

### US-SIM-002: API-Key Authentication

> As a consuming service, I want the simulator to require X-API-Key so that
> the integration demonstrates realistic auth flows.

### US-SIM-003: Health Check

> As a container orchestrator, I want the simulator to expose `GET /health`
> publicly so that Docker Compose can verify readiness.

### US-SIM-004: Simulated 500 Errors

> As a consuming service, I want the simulator to return 500 under
> predictable conditions so that I can test error handling.

### US-SIM-005: Simulated 429 Errors (P1)

> As a consuming service, I want the simulator to return 429 under
> predictable conditions so that I can test retry/backoff logic.

### US-SIM-006: Pagination (P1)

> As a consuming service, I want the simulator to support pagination
> so that I can test multi-page retrieval.

### US-SIM-007: Simulator Browser UI

> As a developer, I want a simple browser UI at `GET /` showing fixture
> data and simulator status so that I can inspect the simulator visually.

---

## 3. Functional Requirements

| ID | Requirement | Priority |
|---|---|---|
| FR-201 | Serve `GET /api/v1/invoices` with static fixture invoice data | P0 |
| FR-202 | Require X-API-Key authentication on all `/api/v1/` endpoints; health and UI are public | P0 |
| FR-203 | Support pagination with `page` and `per_page` query parameters | P1 |
| FR-204 | Return 429 on predictable conditions (e.g., specific header) | P1 |
| FR-205 | Return 500 on predictable conditions (e.g., `?simulate_error=500` query parameter) | P0 |
| FR-206 | Serve a local browser UI at `GET /` showing fixture data and simulator status | P1 |
| FR-207 | Expose `GET /health` as a public endpoint returning `{"status": "ok"}` | P0 |
| FR-208 | Return structured JSON error responses for 401, 429, and 500 | P0 |
| FR-209 | Use Flask application factory pattern with Blueprints | P0 |
| FR-210 | Provide a Dockerfile for container builds | P0 |
| FR-211 | Provide repository-level CI: Ruff lint, pytest, Docker image build | P0 |

---

## 4. Non-Functional Requirements

| ID | Requirement | Priority |
|---|---|---|
| NFR-SIM-001 | All responses are deterministic and reproducible | P0 |
| NFR-SIM-002 | No real API keys, tokens, or provider credentials | P0 |
| NFR-SIM-003 | All code and documentation in English | P0 |
| NFR-SIM-004 | Always described as a local portfolio simulator | P0 |
| NFR-SIM-005 | Tests are deterministic, independent, and fast | P0 |
| NFR-SIM-006 | No database or persistence layer | P0 |

---

## 5. Acceptance Criteria

### AC-SIM-001: Health Check (US-SIM-003, FR-207)

- [ ] `GET /health` returns 200 with `{"status": "ok"}`.
- [ ] No authentication is required.
- [ ] Works without any environment configuration.

### AC-SIM-002: Invoice Retrieval (US-SIM-001, FR-201, FR-202)

- [ ] `GET /api/v1/invoices` with valid X-API-Key returns 200 with fixture invoices.
- [ ] Response format matches the provider API contract schema.
- [ ] Fixture data contains at least 3 invoices with distinct values.

### AC-SIM-003: Authentication (US-SIM-002, FR-202, FR-208)

- [ ] `GET /api/v1/invoices` without X-API-Key returns 401 JSON error.
- [ ] `GET /api/v1/invoices` with invalid X-API-Key returns 401 JSON error.
- [ ] `GET /health` does not require authentication.

### AC-SIM-004: Simulated 500 (US-SIM-004, FR-205, FR-208)

- [ ] `GET /api/v1/invoices?simulate_error=500` with valid key returns 500 JSON error.
- [ ] The 500 trigger is deterministic and documented.
- [ ] The response body is structured JSON with an error message.

### AC-SIM-005: Application Structure (FR-209, FR-210, FR-211)

- [ ] Flask app uses application factory (`create_app()`) and Blueprints.
- [ ] Dockerfile builds a runnable image.
- [ ] CI workflow runs Ruff, pytest, and Docker build.
- [ ] All tests pass before any merge.

### AC-SIM-006: Pagination — P1 (US-SIM-006, FR-203)

> **Status:** Implemented and locally validated on `feature/p1a-pagination-and-429`
> at `c62b6e9e4ea3ee26478307bbd78089214ba8786f`. Aligns with canonical contract
> merged in `integration-workspace` at `1b481345748f7b66084ade31231d0bf146013c4a`.
> **Not yet PR-reviewed, merged, or live-E2E-verified.**

> The criteria below remain unchecked until simulator PR review, end-to-end
> Compose verification, and explicit merge approval are complete.

- [ ] `page` defaults to `1`; valid values are canonical positive integers >= 1.
- [ ] `per_page` defaults to `10`; valid values are canonical integers from `1` through `100`.
- [ ] Successful 200 responses retain top-level `invoices` list (ensuring P0 API compatibility).
- [ ] Response includes `pagination` object with integer fields `page`, `per_page`, `total_items`, and `total_pages`.
- [ ] A request beyond the final page returns 200 with `invoices: []` and accurate pagination metadata.
- [ ] Invalid `page` returns 400 with exact JSON:
      `{"error":"Bad Request","message":"Invalid 'page' parameter: must be an integer >= 1."}`.
- [ ] Invalid `per_page` returns 400 with exact JSON:
      `{"error":"Bad Request","message":"Invalid 'per_page' parameter: must be an integer between 1 and 100."}`.
- [ ] Duplicate `page` query parameter returns 400 with exact JSON:
      `{"error":"Bad Request","message":"Duplicate 'page' query parameter."}`.
- [ ] Duplicate `per_page` query parameter returns 400 with exact JSON:
      `{"error":"Bad Request","message":"Duplicate 'per_page' query parameter."}`.
- [ ] Missing or invalid `X-API-Key` returns 401 before any pagination validation or duplicate checking.
- [ ] Multi-page traversal on the consuming API is explicitly not part of this simulator task.

### AC-SIM-007: Simulated 429 — P1 (US-SIM-005, FR-204)

> **Status:** Implemented and locally validated on `feature/p1a-pagination-and-429`
> at `c62b6e9e4ea3ee26478307bbd78089214ba8786f`. Aligns with canonical contract
> merged in `integration-workspace` at `1b481345748f7b66084ade31231d0bf146013c4a`.
> **Not yet PR-reviewed, merged, or live-E2E-verified.**

> The criteria below remain unchecked until simulator PR review, end-to-end
> Compose verification, and explicit merge approval are complete.

- [ ] Missing or invalid `X-API-Key` returns 401 before any error simulation is evaluated.
- [ ] Following successful authentication, `simulate_error=429` and `simulate_error=500`
      take precedence over duplicate parameter checks and pagination validation.
- [ ] `simulate_error=429` returns HTTP 429 with `Content-Type: application/json` and
      header `Retry-After: 5`.
- [ ] Exact 429 JSON response body:
      `{"error":"Too Many Requests","message":"Simulated rate limit exceeded. Please retry after 5 seconds."}`.
- [ ] P0 API compatibility is preserved because provider responses retain top-level `invoices`.

### AC-SIM-008: Browser UI — P1 (US-SIM-007, FR-206)

- [ ] `GET /` renders an HTML page showing fixture data and simulator status.
- [ ] No authentication required.

---

## 6. Assumptions

- A-SIM-001: The canonical system contract is defined in
  `integration-workspace/docs/contracts/invoice-sync-v0.1.md`.
- A-SIM-002: The X-API-Key is a non-secret test value provided via environment.
- A-SIM-003: Fixture data is static JSON; no database is used.
- A-SIM-004: The simulator runs as a Docker container in the Compose network.
- A-SIM-005: Python 3.12+ is the target runtime.

---

## 7. Out of Scope

- OS-SIM-001: Real Sage API compatibility or OAuth authentication.
- OS-SIM-002: Database persistence or ORM.
- OS-SIM-003: Cloud deployment or production infrastructure.
- OS-SIM-004: Webhook or callback support.
- OS-SIM-005: Real credentials or secrets.
- OS-SIM-006: Contract definition (owned by `integration-workspace`).
- OS-SIM-007: Invoice normalization or sync logic.
- OS-SIM-008: Multi-tenant or multi-user support.
- OS-SIM-009: Performance optimization or load testing.
- OS-SIM-010: CD pipeline (no deployment target).

---

## 8. Risks

| ID | Risk | Mitigation |
|---|---|---|
| R-SIM-001 | Fixture schema drifts from contract | Contract tests in workspace (P1), manual review in P0 |
| R-SIM-002 | Over-engineering beyond P0 | KISS/YAGNI, strict P0/P1 gating |
| R-SIM-003 | Misrepresentation as real provider | Constitution SIM-003, NFR-SIM-004 |
