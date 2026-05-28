# Next Chat Task — Milestone 5.1 Stabilization Validation

Use this brief in future chats to continue work without re-planning completed slices.

## Active Milestone
- Milestone 5.1 — Buy List / Reorder Suggestions (`stabilising`)

## Objective
Run full stabilization validation for the completed Milestone 5.1 vertical slice and confirm it is regression-safe before release-candidate sign-off.

## Scope Lock (current)
In scope for current next task:
- run Codex-cloud dependency install commands
- run compile, lint, and full tests
- document pass/fail outcomes and any environment exceptions
- if validation passes, advance milestone from `stabilising` to `release-candidate`

Out of scope for current slice:
- new feature work for Milestone 5.1
- purchase persistence workflow (Milestone 5.2)
- purchase receiving stock mutation workflow (Milestone 5.3)

## Validation Commands (Codex cloud)
- `python -m pip install --upgrade pip`
- `pip install -r requirements.txt`
- `pip install -r requirements-dev.txt`
- `python -m compileall -q src tests`
- `ruff check src tests`
- `pytest -q`

## Evidence
- `docs/ai/reports/milestone-5.1-first-vertical-slice-implementation-report-2026-05-28.md`
- `docs/ai/reports/milestone-5.1-stabilization-validation-report-2026-05-28.md`
