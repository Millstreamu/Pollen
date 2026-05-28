# Next Chat Task — Milestone 6.1 Completion Closeout Sign-off

## Active Milestone
- Milestone 6.1 — Today Data Summary (`release-candidate`)

## Objective
Execute Milestone 6.1 completion closeout validation/sign-off and mark milestone complete when checks pass.

## Scope Lock (current)
In scope for current next task:
- rerun required milestone validation commands in Codex cloud
- confirm no outstanding in-scope items remain
- produce completion closeout report
- update milestone status to `complete` only if validation passes

Out of scope for current slice:
- new feature development
- UX expansion or prioritization logic changes
- cross-milestone scope additions

## Validation Commands (Codex cloud)
- `python -m pip install --upgrade pip`
- `pip install -r requirements.txt`
- `pip install -r requirements-dev.txt`
- `python -m compileall -q src tests`
- `ruff check src tests`
- `pytest -q`

## Evidence
- `docs/ai/reports/milestone-6.1-release-candidate-validation-signoff-2026-05-28.md`
