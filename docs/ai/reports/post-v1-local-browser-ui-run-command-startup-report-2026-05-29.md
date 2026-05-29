# Post-V1 Local Browser UI Run Command Startup Report (2026-05-29)

## Task understood
Create a bounded post-V1 task for adding a local browser UI run command, and record startup/scope-lock evidence before implementation.

This planning slice does **not** implement the run command. It prepares the next implementation slice so the app can later be opened in a browser with one documented local command.

## Task source
Direct human request:

> can you create a task as per the ai dev method for adding a local browser UI run command. do a start up report as well

This request selects a bounded post-V1 task after V1 completion and satisfies the current handoff requirement to choose one scoped post-V1 task before implementation.

## Rule files read
- `AI_DEVELOPMENT.md`
- `docs/ai/project-rules.md`
- `docs/ai/development-process.md`
- `docs/ai/testing-rules.md`
- `docs/ai/task-execution-rules.md`
- `docs/ai/ui-rules.md`
- `docs/ai/reporting-rules.md`

## Project memory files read
- `docs/ai/next-chat-task.md`
- `docs/ai/completion-status.md`
- `docs/ai/progress-log.md`
- `docs/ai/known-issues.md`
- `docs/ai/do-not-build-yet.md`
- `docs/ai/reports/milestone-10.3-v1-release-decision-report-2026-05-29.md`

## Relevant repo files found
- `README.md` documents dependency setup and validation commands, but no browser run command.
- `requirements.txt` has no runtime dependencies.
- `requirements-dev.txt` contains pytest and ruff only.
- `pyproject.toml` configures ruff.
- `pytest.ini` sets `pythonpath = src` for tests.
- `src/pollen/app.py` provides `AppShell`, route handling through `get()`/`post()`, page rendering, and `create_app()`.
- `tests/test_app.py` exercises the app shell routes and page HTML directly.

## Existing patterns observed
- The project intentionally uses a small Python app shell instead of a framework such as Flask/FastAPI/Django.
- Page routes already exist for Today, Orders, Products & Stock, Make / Buy, Money, and Settings.
- Private routes require an authorization header; tests use a deterministic bearer header such as `Bearer user:u1:maker@example.com`.
- Existing UI behaviour is tested by calling `create_app().get(...)` and `app.post(...)` directly.
- The repo's standard validation sequence is:
  - `python -m pip install --upgrade pip`
  - `pip install -r requirements.txt`
  - `pip install -r requirements-dev.txt`
  - `python -m compileall -q src tests`
  - `ruff check src tests`
  - `pytest -q`

## Selected post-V1 task
Name: Post-V1 Local Browser UI Run Command

Status: scoped / ready for implementation

Goal:
Allow a user to run one local command and open the existing Pollen app shell in a browser.

Recommended command:

```bash
PYTHONPATH=src python -m pollen.dev_server
```

Recommended local URL:

```text
http://localhost:8000
```

## Planned implementation scope for the next coding slice
- Add a small local development server entrypoint under `src/pollen/`.
- Prefer Python standard-library HTTP serving so no runtime dependency is added unless implementation proves it necessary.
- Serve the existing `AppShell` routes through HTTP:
  - `GET /`
  - `GET /orders`
  - `GET /products-stock`
  - `GET /make-buy`
  - `GET /money`
  - `GET /settings`
- Adapt form submissions to the existing `AppShell.post()` flow for supported POST routes.
- Use a deterministic local demo auth header by default so private pages can be opened without adding a login system.
- Return reasonable HTTP responses for missing routes and unsupported methods.
- Document the run command in `README.md`.
- Add tests for the server adapter/handler behaviour without requiring a long-running manual server.
- Add a bounded completion report under `docs/ai/reports/` after implementation.

## Acceptance criteria for the implementation task
- [ ] One documented command starts a local browser server.
- [ ] Opening `http://localhost:8000` renders the existing Today page.
- [ ] Existing navigation links work in the browser.
- [ ] Existing forms continue to use the existing app-shell service logic where supported.
- [ ] Unsupported paths return a non-success status rather than crashing.
- [ ] The implementation does not add new product features, new screens, marketplace integrations, auth systems, persistence layers, or broad redesigns.
- [ ] Runtime dependencies remain unchanged unless a report justifies why a dependency is necessary.
- [ ] Tests cover the new run-command/server adapter path.
- [ ] The full validation sequence passes in Codex cloud.

## Out-of-scope items
- A production web server.
- Deployment hosting.
- Docker setup.
- OAuth/login/session management.
- Persistent database storage.
- New UI features or visual redesign.
- New marketplace integrations.
- Screenshot evidence unless separately scoped.
- Replacing the existing app shell with Flask/FastAPI/Django.

## Risks
- The existing app shell expects an authorization header for private routes, so the local server needs an explicit demo-auth approach to keep browser testing simple.
- Browser form submissions require URL-encoded form parsing and safe mapping into existing `AppShell.post()` calls.
- The server must be easy to test without leaving a long-running process in automated validation.
- The command may need `PYTHONPATH=src` unless the package is installed; documentation should be clear.

## Tests/checks to run for the implementation task
- `python -m pip install --upgrade pip`
- `pip install -r requirements.txt`
- `pip install -r requirements-dev.txt`
- `python -m compileall -q src tests`
- `ruff check src tests`
- `pytest -q`

If the implementation introduces a direct command smoke check that can run without hanging, also run that check and report it.

## Decision
The local browser UI run command is selected as the next bounded post-V1 implementation task.

No code implementation is included in this startup slice.
