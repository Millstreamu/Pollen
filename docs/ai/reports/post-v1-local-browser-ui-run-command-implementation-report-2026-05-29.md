# Post-V1 Local Browser UI Run Command — Implementation Report

Date: 2026-05-29

## Task source
- `docs/ai/next-chat-task.md`
- `docs/ai/reports/post-v1-local-browser-ui-run-command-startup-report-2026-05-29.md`

## Scope implemented
- Added a local development HTTP server entrypoint at `src/pollen/dev_server.py`.
- Used only Python standard-library HTTP serving; no runtime dependencies were added.
- Added a deterministic local demo auth header so private app-shell pages can be opened in a browser without adding login or session work.
- Exposed the existing app-shell GET routes through HTTP:
  - `/`
  - `/orders`
  - `/products-stock`
  - `/make-buy`
  - `/money`
  - `/settings`
- Adapted `application/x-www-form-urlencoded` POST bodies to the existing `AppShell.post()` flow for supported forms.
- Returned non-success HTTP responses for unsupported paths, unsupported methods, and unsupported POST content types.
- Documented the run command and URL in `README.md`.
- Added tests for the server adapter and server factory path.

## Command

```bash
PYTHONPATH=src python -m pollen.dev_server
```

Default local URL:

```text
http://localhost:8000
```

Optional local override example:

```bash
PYTHONPATH=src python -m pollen.dev_server --host 127.0.0.1 --port 8001
```

## Acceptance criteria result
- [x] One documented command starts a local browser server.
- [x] Opening `http://localhost:8000` renders the existing Today page through the server adapter and direct local smoke check.
- [x] Existing navigation links work in the browser-served app shell routes.
- [x] Supported forms continue to use existing app-shell service logic through URL-encoded POST adaptation.
- [x] Unsupported paths return a non-success status rather than crashing.
- [x] Runtime dependencies remain unchanged.
- [x] Tests cover the new server adapter/run-command path.
- [x] Full Codex-cloud validation passes.

## Out of scope intentionally not implemented
- Production hosting/server hardening.
- Docker/deployment work.
- OAuth, login, sessions, or role systems.
- Persistent database storage.
- New product features or new screens.
- Visual redesign or broad UI polish.
- Marketplace integrations.
- Optional Milestone 9.2 screenshot evidence.
- Replacing the app shell with Flask, FastAPI, Django, or another web framework.

## Validation commands run
- `python -m pip install --upgrade pip`
- `pip install -r requirements.txt`
- `pip install -r requirements-dev.txt`
- `python -m compileall -q src tests`
- `ruff check src tests`
- `pytest -q`
- `PYTHONPATH=src pytest -q tests/test_dev_server.py`
- `PYTHONPATH=src python -m pollen.dev_server --help`
- `PYTHONPATH=src python -m pollen.dev_server --port 8765` with a local `curl -i http://localhost:8765/` smoke check

## Result
Full validation passed in the Codex cloud environment after implementation (`106 passed`).

## Environment limitations
No blocking environment limitations were encountered.

A visual screenshot was not captured because the implementation did not redesign UI pixels; the browser-serving behavior was verified with deterministic adapter tests and a local HTTP smoke check.

## Known limitations
- The server is local-development only.
- Data remains in-memory, matching the current app-shell architecture.
- The deterministic demo auth header is intentionally local-only and is not a login/session system.

## Follow-up backlog items
- Select a separate scoped post-V1 task before adding any production hosting, auth/session work, persistence, or visual polish.

## Project memory files updated
- `README.md`
- `docs/ai/progress-log.md`
- `docs/ai/completion-status.md`
- `docs/ai/next-chat-task.md`
- `docs/ai/reports/post-v1-local-browser-ui-run-command-implementation-report-2026-05-29.md`
