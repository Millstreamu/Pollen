# Next Chat Task — Milestone 5.3 Release-Candidate Validation

## Active Milestone
- Milestone 5.3 — Receive Purchase (`stabilising`)

## Objective
Run release-candidate validation and sign-off for Milestone 5.3 after stabilization validation.

## Scope Lock (current)
In scope for current next task:
- run full Codex cloud validation command set
- verify no regressions in purchase creation and receiving
- update milestone status and evidence reports

Out of scope for current slice:
- new feature additions beyond Milestone 5.3 acceptance criteria

## Validation Commands (Codex cloud)
- `python -m pip install --upgrade pip`
- `pip install -r requirements.txt`
- `pip install -r requirements-dev.txt`
- `python -m compileall -q src tests`
- `ruff check src tests`
- `pytest -q`

## Evidence
- `docs/ai/reports/milestone-5.3-stabilization-validation-report-2026-05-28.md`
