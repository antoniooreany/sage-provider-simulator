# Sage Provider Simulator — Agent Configuration

## Reading Order

Before working in this repository, read:

1. `~/.gemini/GEMINI.md`
2. `../GEMINI.md`
3. `../AGENTS.md`
4. `./GEMINI.md`
5. `.specify/memory/constitution.md`
6. Active specification, plan, and task list under `specs/`

## Agent Roles

### Simulator Agent

- **Scope:** Flask application, fixtures, provider endpoints, error scenarios.
- **Writes to:** `app/`, `fixtures/`, `tests/`, `Dockerfile`, `requirements.txt`.
- **Does not write:** Compose files, API contract definitions, normalization logic.

### CI Agent

- **Scope:** Linting, testing, Docker build workflows.
- **Writes to:** `.github/workflows/`, `pyproject.toml`, `setup.cfg`.
- **Does not write:** Application logic, fixtures, integration tests.

## Constraints

- One agent per branch at a time.
- All changes require Pull Request review.
- Never commit to `main` or `develop` directly.
- Never fabricate integrations, test results, or deployments.
- This is a local Sage-like portfolio simulator, not an official Sage API.
- No secrets, tokens, or real credentials in any file.
- The API contract is owned by `integration-workspace`; this repo implements it.
