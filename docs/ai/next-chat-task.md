# Next Chat Task — Milestone 4.3 Completion Closeout Sign-off

Use this brief in future chats to continue work without re-planning completed slices.

## Active Milestone
- Milestone 4.3 — Complete Batch (`release-candidate`)

## Objective
Execute completion closeout validation/sign-off for Milestone 4.3 and transition milestone status to `complete` when all required checks pass.

## Scope Lock (current)
In scope for current next task:
- run full Codex-cloud validation command sequence
- confirm Complete Batch lifecycle behavior remains regression-safe
- update milestone tracking from `release-candidate` to `complete` once checks pass
- produce durable closeout sign-off report evidence

Out of scope for current slice:
- new feature development unrelated to Milestone 4.3 closeout
- UX redesign or Money module work
- partial-completion/rollback workflow expansion

## Validation Commands (Codex cloud)
- `python -m pip install --upgrade pip`
- `pip install -r requirements.txt`
- `pip install -r requirements-dev.txt`
- `python -m compileall -q src tests`
- `ruff check src tests`
- `pytest -q`

## Evidence
- `docs/ai/reports/milestone-4.3-release-candidate-validation-signoff-2026-05-28.md`
