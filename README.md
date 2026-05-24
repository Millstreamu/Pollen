# Pollen

Lightweight ERP-like management tool.

## Milestone 0 (Scaffold)

This repository now includes a minimal Python scaffold so Codex cloud can install dependencies and run tests consistently.

### Setup

```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
pip install -r requirements-dev.txt
```

### Validation

```bash
python -m compileall -q src tests
pytest -q
```

## Current app slice

- `src/pollen/app.py` exposes a `healthcheck()` function.
- `src/pollen/models.py` contains the first domain model, `OrderStatus`.
- `tests/` includes unit tests for the healthcheck and status transitions.
