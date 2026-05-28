# Next Chat Task — Milestone 5.3 Startup Planning + Scope Lock

Use this brief in future chats to continue work without re-planning completed slices.

## Active Milestone
- Milestone 5.3 — Receive Purchase (`not-started`)

## Objective
Execute Milestone 5.3 startup planning and scope lock, then implement the first vertical slice for receiving purchases with stock movement safety and tests.

## Scope Lock (current)
In scope for current next task:
- define Milestone 5.3 scope boundaries against roadmap acceptance criteria
- implement purchase receiving transition (`Ordered` -> `Received`)
- increase material stock only on receive (never on create)
- create InventoryMovement + ActivityLog entries on receive
- block double-receive idempotency violations
- add/extend tests for receive behavior and regressions
- record milestone report evidence and update status/progress artifacts

Out of scope for current slice:
- supplier automation or auto-replenishment
- partial receive/backorder workflows
- bulk receive UX redesign
- non-milestone procurement analytics

## Validation Commands (Codex cloud)
- `python -m pip install --upgrade pip`
- `pip install -r requirements.txt`
- `pip install -r requirements-dev.txt`
- `python -m compileall -q src tests`
- `ruff check src tests`
- `pytest -q`

## Evidence
- `docs/ai/reports/milestone-5.2-first-vertical-slice-implementation-report-2026-05-28.md`
- `docs/ai/reports/milestone-5.2-stabilization-validation-report-2026-05-28.md`
- `docs/ai/reports/milestone-5.2-release-candidate-validation-signoff-2026-05-28.md`
- `docs/ai/reports/milestone-5.2-completion-closeout-signoff-2026-05-28.md`
