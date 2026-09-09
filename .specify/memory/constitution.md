# Project Constitution — Sage Provider Simulator

Version: 0.1.0
Status: Active
Last Updated: 2026-09-08
Parent Constitution: `../../integration-workspace/.specify/memory/constitution.md`

## Purpose

This constitution defines non-negotiable principles for the Sage Provider
Simulator repository. It inherits all invariants from the ecosystem constitution
and adds simulator-specific rules.

## Inherited Invariants

All invariants INV-001 through INV-015 from the ecosystem constitution apply
without exception. Key invariants for this repository:

- **INV-001:** Service boundary enforcement — this repo owns only simulation.
- **INV-003:** Honest naming — local portfolio simulator, never official Sage API.
- **INV-004:** No secrets in Git.
- **INV-005:** Spec-driven development.
- **INV-006:** Gitflow discipline.
- **INV-007:** Conventional Commits.
- **INV-010:** Incremental delivery (P0 → P1 → P2).
- **INV-011:** Test-first for critical behavior.
- **INV-012:** KISS and YAGNI.
- **INV-014:** CI as gate.

## Simulator-Specific Rules

### SIM-001: No Database

The simulator uses static fixture data (JSON files). No database, ORM, or
persistence layer is permitted in this repository.

### SIM-002: Contract Compliance

This repository implements the provider API contract owned by
`integration-workspace`. It does not define or modify the contract.

### SIM-003: Deterministic Behavior

All simulator responses must be deterministic and reproducible. Error scenarios
(500, 429) are triggered by specific, documented request parameters — never
by random chance.

### SIM-004: Fixture Data Ownership

Fixture invoice data lives in this repository under `fixtures/`. The data
format must match the provider API contract's response schema.

### SIM-005: Public Endpoints

`GET /health` and `GET /` (simulator UI) must remain public — no authentication
required. Only endpoints under `/api/v1/` require X-API-Key authentication.

## Traceability

Every requirement (FR-2xx) traces through:
specification → plan → tasks → tests → contract compliance.
