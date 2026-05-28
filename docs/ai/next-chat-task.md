# Next Chat Task — Milestone 10.1 Release-Candidate Validation

## Active Milestone
- Milestone 10.1 — Full Journey Suite (`release-candidate`)

## Objective
Run release-candidate validation/sign-off for Milestone 10.1 now that the money-summary journey coverage gap is closed.

## Scope Lock (current)
In scope for current next task:
- inspect Milestone 10.1 completion status, progress log, and latest money-summary journey report
- run the required validation sequence
- confirm the full journey suite covers the required workflows, including money summary updates
- add release-candidate validation/sign-off evidence under `docs/ai/reports/`
- update completion/progress tracking based on the validation decision

Out of scope for current slice:
- Milestone 10.2 release-freeze bookkeeping unless Milestone 10.1 is explicitly completed first
- new product features or journey expansion beyond validation fixes
- full accounting, taxes, analytics, or advanced money dashboards
- new external integrations or live payment data
- optional screenshot evidence unless explicitly scoped

## Validation Commands (Codex cloud)
- `python -m pip install --upgrade pip`
- `pip install -r requirements.txt`
- `pip install -r requirements-dev.txt`
- `python -m compileall -q src tests`
- `ruff check src tests`
- `pytest -q`

## Evidence
- add a bounded implementation/validation report under `docs/ai/reports/` for the Milestone 10.1 money journey slice
