# Next Chat Task — Milestone 5.2 Release-Candidate Validation + Sign-off

Use this brief in future chats to continue work without re-planning completed slices.

## Active Milestone
- Milestone 5.2 — Purchase Workflow Persistence (`stabilising`)

## Objective
Execute Milestone 5.2 release-candidate validation + sign-off after stabilization, including full validation evidence and status transition updates.

## Scope Lock (current)
In scope for current next task:
- run full Codex-cloud validation sequence
- confirm Milestone 5.2 purchase creation persistence behavior remains regression-safe
- record release-candidate validation/sign-off report evidence
- transition milestone status from `stabilising` to `release-candidate` if checks pass
- update progress log and next-chat handoff

Out of scope for current slice:
- purchase receiving stock mutation workflow (Milestone 5.3)
- InventoryMovement or ActivityLog receiving semantics
- supplier automation, smart replenishment, or broader procurement UX redesign

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
