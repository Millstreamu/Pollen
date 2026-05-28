# Next Chat Task — Milestone 5.1 Completion Closeout Sign-off

Use this brief in future chats to continue work without re-planning completed slices.

## Active Milestone
- Milestone 5.1 — Buy List / Reorder Suggestions (`release-candidate`)

## Objective
Run completion closeout validation for Milestone 5.1 and, if checks pass, transition the milestone to `complete`.

## Scope Lock (current)
In scope for current next task:
- run Codex-cloud dependency install commands
- run compile, lint, and full tests
- document pass/fail outcomes and any environment exceptions
- if validation passes, advance milestone from `release-candidate` to `complete`

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
- `docs/ai/reports/milestone-5.1-release-candidate-validation-signoff-2026-05-28.md`
