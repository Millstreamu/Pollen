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

It also exposes a simple local readiness check at `/healthz`, which returns `OK` for browser-server smoke tests.

Optional flags are available for local port conflicts:

```bash
PYTHONPATH=src python -m pollen.dev_server --host 127.0.0.1 --port 8001
```

## Optional UI screenshot review

The app shell includes screenshot-friendly styling and two optional visual-review helpers.

For a no-dependency fallback, export standalone HTML pages and open them in a browser or screenshot tool:

```bash
PYTHONPATH=src python scripts/export_ui_review_pages.py
```

Review pages are written to `docs/ai/ui-review-pages/` by default and are ignored by git so they can be regenerated locally.

If your GitHub Codespace already has Playwright available, capture PNG screenshots directly:

```bash
PYTHONPATH=src python scripts/capture_ui_screenshots.py
```

If Playwright or Chromium's Linux shared libraries are missing in a Codespace/local Linux environment, install the optional browser tooling first. The `install-deps` step is required on fresh Codespaces because installing the Python package and downloading Chromium does not install OS-level shared libraries such as `libatk-1.0.so.0`.

```bash
python -m pip install playwright
python -m playwright install-deps chromium
python -m playwright install chromium
PYTHONPATH=src python scripts/capture_ui_screenshots.py
```

You can also run the checked-in optional setup helper, which prints the same verification command after installing Playwright, Chromium's Linux system dependencies, and the Chromium browser binary:

```bash
python scripts/setup_playwright_screenshots.py
PYTHONPATH=src python scripts/capture_ui_screenshots.py
```

Screenshots are written to `docs/ai/ui-screenshots/` by default and are ignored by git. Playwright remains optional and is not part of normal runtime or Codex-cloud test dependencies.

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
