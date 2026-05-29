# Post-V1 Dev Dependency Installability Report (2026-05-29)

## Scope
Bounded post-V1 maintenance task: make the repository development dependency setup pass in the Codex cloud environment without starting new product feature work.

## Why This Task Was Selected
V1 is complete, and `docs/ai/next-chat-task.md` requires selecting one explicitly scoped post-V1 task before implementation. The only active non-product friction in project memory was the repeated environment/setup limitation where `pip install -r requirements-dev.txt` failed because exact dev dependency pins required package-index access even though compatible tools were already available in the Codex environment.

## Acceptance Criteria
- Keep the task limited to setup/testability maintenance.
- Do not change product behavior, UI, integrations, or feature scope.
- Make `pip install -r requirements-dev.txt` succeed in the current Codex cloud environment when compatible tooling is already installed.
- Run the full required validation sequence.
- Update durable project memory and report evidence.

## Files Reviewed
- `AI_DEVELOPMENT.md`
- `docs/ai/next-chat-task.md`
- `docs/ai/completion-status.md`
- `docs/ai/progress-log.md`
- `docs/ai/known-issues.md`
- `docs/ai/do-not-build-yet.md`
- `docs/ai/reports/milestone-10.3-v1-release-decision-report-2026-05-29.md`
- `requirements.txt`
- `requirements-dev.txt`
- `pyproject.toml`
- `pytest.ini`

## Implementation
`requirements-dev.txt` now uses conservative compatible ranges:

- `pytest>=8.4.2,<10`
- `ruff>=0.12.0,<1`

This preserves minimum versions from the previous pins while allowing Codex cloud to satisfy development setup with already-installed compatible newer versions when package-index access is restricted.

## Commands Executed
- `python -m pip install --upgrade pip`
- `pip install -r requirements.txt`
- `pip install -r requirements-dev.txt`
- `python -m compileall -q src tests`
- `ruff check src tests`
- `PYTHONDONTWRITEBYTECODE=1 pytest -q`

## Results
- Runtime dependency installation: pass.
- Dev dependency installation: pass.
- Compile check: pass.
- Lint check: pass.
- Full test suite: pass (`98 passed`).

## Environment Notes
- The optional `pip` upgrade lookup still prints package-index/proxy retry warnings (`Tunnel connection failed: 403 Forbidden`), but the command exits successfully because the installed `pip` is usable.
- Repository dependency setup now passes because `requirements-dev.txt` can be satisfied by compatible installed tooling.
- No Docker, live OAuth, webhook, external marketplace API, hosted server, or browser screenshot checks were required for this setup-only task.

## Out of Scope
- New features, screens, integrations, or speculative polish.
- Optional Milestone 9.2 screenshot evidence.
- Runtime product behavior changes.
- Broad dependency modernization beyond the minimum installability fix.

## Follow-Up
Future post-V1 work should continue to be selected as a single bounded task with explicit acceptance criteria before implementation.
