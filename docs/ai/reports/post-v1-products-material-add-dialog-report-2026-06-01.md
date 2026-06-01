# Post-V1 Products Materials Add Dialog Report — 2026-06-01

## Task Source
Direct human request: change the Products & Stock page Materials panel so the control says “Add Material” instead of “View Materials”, and make that button open a popup that can add a material.

## Scope Implemented
- Replaced the Products & Stock Materials panel link target and label with an `Add Material` popup trigger.
- Added a focused `add-material-dialog` popup to the Products & Stock page using the existing workflow-dialog pattern.
- Added a Products & Stock POST action, `create_material`, that creates a material and re-renders the Products & Stock page so the new material appears in the panel.
- Updated regression coverage for the visible label, popup wiring, material creation behavior, and dialog control styling.

## Intentionally Not Implemented
- Did not reintroduce the hidden Make / Buy material-management/admin panel.
- Did not add persistence, suppliers, purchase automation, or broader material editing flows.
- Did not add new runtime or dev dependencies.

## Validation Summary
Dependencies installed:
- Runtime dependencies: `pip install -r requirements.txt` passed; no runtime packages are currently required.
- Dev dependencies: `pip install -r requirements-dev.txt` passed using already-available compatible packages.

Commands run:
- `python -m pip install --upgrade pip` — passed with package-index proxy retry warnings; installed pip remained usable.
- `pip install -r requirements.txt` — passed.
- `pip install -r requirements-dev.txt` — passed.
- `python -m compileall -q src tests scripts` — passed.
- `ruff check src tests scripts` — passed.
- `PYTHONDONTWRITEBYTECODE=1 pytest -q` — passed (`118 passed`).
- `PYTHONPATH=src python scripts/export_ui_review_pages.py` — passed and exported local review HTML.
- `PYTHONPATH=src python scripts/capture_ui_screenshots.py` — blocked because Playwright is not installed.
- `python -m pip install playwright` — blocked because the package-index proxy returned `403 Forbidden` / no matching distribution.

## Result
The requested UI workflow is complete and covered by automated tests. The screenshot capture step remains environment-limited by unavailable Playwright installation, but deterministic compile, lint, test, and HTML export checks passed.

## Environment Limitations
The configured Python package index/proxy refused Playwright lookup, so browser screenshot capture could not be completed in this environment.

## Follow-Up Backlog Items
- Capture and review updated Products & Stock screenshots later in an environment where Playwright and Chromium can be installed.
- If users need full material editing from Products & Stock, scope a separate material management follow-up.
