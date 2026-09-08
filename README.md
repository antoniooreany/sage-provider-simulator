# Sage Provider Simulator

This repository contains a local portfolio simulator designed to mimic the behavior of a Sage-like provider API. This allows testing integrations against a stable, predictable, and local API without needing access to real staging or production environments.

This simulator is not the official Sage API. The API contract simulated here is owned by the `integration-workspace` team.

## Overview

The simulator is built with Python 3.12 and Flask. It uses a straightforward Application Factory pattern with Blueprints to mock API responses and error states. It reads static JSON fixtures to simulate data like invoices.

## Quick Start

### Prerequisites
- Python 3.12+

### Installation & Execution

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```
2. **Set the environment (optional):**
   Copy `.env.example` to `.env` or just export variables if needed.
3. **Run the application:**
   ```bash
   python -m flask --app app run --host 0.0.0.0 --port 5000
   ```

## Endpoints

### Health Check
- **`GET /health`**
  - **Auth:** None required.
  - **Response:** `200 OK` with JSON `{"status": "ok"}`.

### Invoices
- **`GET /api/v1/invoices`**
  - **Auth:** Requires valid `X-API-Key` header.
  - **Response:** `200 OK` with JSON array of invoices sourced from `fixtures/invoices.json`.

## Error Simulation

You can simulate a server error by appending a query parameter `simulate_error=500` to the endpoint:
```bash
curl -H "X-API-Key: test-api-key-not-a-secret" "http://localhost:5000/api/v1/invoices?simulate_error=500"
```
This will return a `500 Internal Server Error` response.

## Environment Variables

| Variable | Description | Default |
| -------- | ----------- | ------- |
| `PROVIDER_API_KEY` | Expected API key in the `X-API-Key` header | `test-api-key-not-a-secret` |

## Testing

This project follows Test-Driven Development using `pytest`.

To run tests:
```bash
pytest -v
```

To run formatting and linting:
```bash
ruff check .
```

## Docker

You can build and run the simulator using Docker:

```bash
docker build -t sage-provider-simulator .
docker run -p 5000:5000 sage-provider-simulator
```

## CI

This project is configured with GitHub Actions (`.github/workflows/ci.yml`) to automatically run linting, tests, and a test Docker build on pushes and pull requests to the `develop` branch.
