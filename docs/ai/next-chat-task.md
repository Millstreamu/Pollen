# Next Chat Task — Post-V1 Local Browser UI Run Command

## Active Milestone
- V1 Release — complete

## Selected Post-V1 Task
- Post-V1 Local Browser UI Run Command — scoped / ready for implementation

## Objective
Add a small local development server so a user can run one documented command and open the existing Pollen app shell in a browser.

This task has been selected as the bounded post-V1 task requested after V1 completion. The startup/scope-lock evidence is recorded in `docs/ai/reports/post-v1-local-browser-ui-run-command-startup-report-2026-05-29.md`.

## Scope Lock (current)
In scope for the implementation task:
- add a local development server entrypoint under `src/pollen/`
- prefer Python standard-library HTTP serving; avoid runtime dependencies unless a report justifies them
- expose the existing app-shell pages in a browser:
  - `/`
  - `/orders`
  - `/products-stock`
  - `/make-buy`
  - `/money`
  - `/settings`
- adapt supported browser form submissions to the existing `AppShell.post()` flow
- use a deterministic local demo auth header so private pages can be opened without adding login/session work
- document the command in `README.md`
- add tests for the run-command/server adapter path
- add a bounded implementation report under `docs/ai/reports/`

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
- [ ] One documented command starts a local browser server.
- [ ] Opening `http://localhost:8000` renders the existing Today page.
- [ ] Existing navigation links work in the browser.
- [ ] Supported forms continue to use existing app-shell service logic.
- [ ] Unsupported paths return a non-success status rather than crashing.
- [ ] Runtime dependencies remain unchanged unless explicitly justified in the implementation report.
- [ ] Tests cover the new server adapter/run-command path.
- [ ] Full Codex-cloud validation passes.

## Validation Commands (Codex cloud)
- `python -m pip install --upgrade pip`
- `pip install -r requirements.txt`
- `pip install -r requirements-dev.txt`
- `python -m compileall -q src tests`
- `ruff check src tests`
- `pytest -q`

## Evidence
- Startup/scope-lock report: `docs/ai/reports/post-v1-local-browser-ui-run-command-startup-report-2026-05-29.md`
- For implementation, add a bounded completion report under `docs/ai/reports/`.
