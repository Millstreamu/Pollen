# Pollen

Lightweight ERP-like management tool.

## Setup

```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
pip install -r requirements-dev.txt
```

## Run the local browser UI

Start the local development server with one command:

```bash
PYTHONPATH=src python -m pollen.dev_server
```

Then open:

```text
http://localhost:8000
```

The development server uses Python's standard-library HTTP server and a deterministic local demo user so the existing private app-shell pages can be opened in a browser without adding a login system. It is intended for local development only, not production hosting.

The command serves the current app-shell pages:

- `/`
- `/orders`
- `/products-stock`
- `/make-buy`
- `/money`
- `/settings`

Optional flags are available for local port conflicts:

```bash
PYTHONPATH=src python -m pollen.dev_server --host 127.0.0.1 --port 8001
```

## Validation

```bash
python -m compileall -q src tests
ruff check src tests
pytest -q
```

## Current app slice

- `src/pollen/app.py` exposes the in-memory app shell and workflow routes.
- `src/pollen/dev_server.py` exposes the local browser development server.
- `src/pollen/models.py` contains domain models used by the workflow services.
- `tests/` includes unit, service, journey, app-shell, and dev-server adapter coverage.
