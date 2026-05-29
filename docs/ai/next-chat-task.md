# Next Chat Task — Select Next Post-V1 Task

## Active Milestone
- V1 Release — complete

## Selected Post-V1 Task
- Post-V1 Local Browser UI Run Command — complete

## Objective
The selected local browser UI run command task is complete. Select a new bounded post-V1 task before any further implementation.

Implementation evidence is recorded in `docs/ai/reports/post-v1-local-browser-ui-run-command-implementation-report-2026-05-29.md`.

## Completed Scope
Implemented in the completed task:
- added a local development server entrypoint under `src/pollen/`
- used Python standard-library HTTP serving without adding runtime dependencies
- exposed the existing app-shell pages in a browser:
  - `/`
  - `/orders`
  - `/products-stock`
  - `/make-buy`
  - `/money`
  - `/settings`
- adapted supported browser form submissions to the existing `AppShell.post()` flow
- used a deterministic local demo auth header so private pages can be opened without adding login/session work
- documented the command in `README.md`
- added tests for the run-command/server adapter path
- added a bounded implementation report under `docs/ai/reports/`

Out of scope unless separately scoped:
- production hosting/server hardening
- Docker/deployment work
- OAuth, login, sessions, or role systems
- persistent database storage
- new product features or new screens
- visual redesign or broad UI polish
- marketplace integrations
- optional Milestone 9.2 screenshot evidence
- replacing the app shell with a full web framework

## Acceptance Criteria
- [x] One documented command starts a local browser server.
- [x] Opening `http://localhost:8000` renders the existing Today page.
- [x] Existing navigation links work in the browser.
- [x] Supported forms continue to use existing app-shell service logic.
- [x] Unsupported paths return a non-success status rather than crashing.
- [x] Runtime dependencies remain unchanged.
- [x] Tests cover the new server adapter/run-command path.
- [x] Full Codex-cloud validation passes.

## Validation Commands (Codex cloud)
- `python -m pip install --upgrade pip`
- `pip install -r requirements.txt`
- `pip install -r requirements-dev.txt`
- `python -m compileall -q src tests`
- `ruff check src tests`
- `pytest -q`

## Evidence
- Startup/scope-lock report: `docs/ai/reports/post-v1-local-browser-ui-run-command-startup-report-2026-05-29.md`
- Implementation report: `docs/ai/reports/post-v1-local-browser-ui-run-command-implementation-report-2026-05-29.md`

## Next Required Action
Select a new bounded post-V1 task before further implementation.
