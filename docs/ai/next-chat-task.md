# Next Chat Task — Milestone 4.3 First Vertical Slice Implementation

Use this brief in future chats to continue work without re-planning completed slices.

## Active Milestone
- Milestone 4.3 — Complete Batch (`in-progress`)

## Objective
Implement the first Milestone 4.3 vertical slice for Complete Batch lifecycle transition with safe stock mutation behavior and test coverage.

## Scope Lock (current)
In scope for current next task:
- add Complete Batch action in service/app flow for in-progress batches
- enforce transition gate (`in-progress` -> `complete` only)
- decrease material quantities according to recipe requirements × batch quantity
- increase finished product stock by batch quantity
- persist completion timestamp/status metadata
- add/extend tests for successful completion + blocked invalid transitions
- add/extend journey test coverage for create -> start -> complete integrity

Out of scope for current slice:
- partial completion or rollback workflows
- post-completion rework/cancel flows
- Money module features
- unrelated UX redesign

## Validation Commands (Codex cloud)
- `python -m pip install --upgrade pip`
- `pip install -r requirements.txt`
- `pip install -r requirements-dev.txt`
- `python -m compileall -q src tests`
- `ruff check src tests`
- `pytest -q`

## Evidence
- `docs/ai/reports/milestone-4.3-startup-planning-scope-lock-report-2026-05-28.md`
