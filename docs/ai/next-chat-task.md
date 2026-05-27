# Next Chat Task — Milestone 4.2 Release-Candidate Validation + Sign-off

Use this brief in future chats to continue work without re-planning completed slices.

## Active Milestone
- Milestone 4.2 — Start Batch (`stabilising`)

## Objective
Execute release-candidate validation/sign-off for Milestone 4.2 after first-slice implementation and stabilization checks.

## Scope Lock (current)
In scope for current next task:
- run full Codex-cloud validation commands
- confirm Start Batch transition behavior remains regression-safe
- update milestone status from `stabilising` to `release-candidate` if checks pass
- publish release-candidate validation report and update milestone tracking artifacts

Out of scope for current slice:
- Milestone 4.3 Complete Batch stock/material mutation logic
- Money module features
- unrelated UX redesign

## Validation Commands (Codex cloud)
- `python -m pip install --upgrade pip`
- `pip install -r requirements.txt`
- `pip install -r requirements-dev.txt`
- `python -m compileall -q src tests`
- `ruff check src tests`
- `pytest -q`

## Planning Evidence
- `docs/ai/reports/milestone-4.2-startup-planning-scope-lock-report-2026-05-27.md`
- `docs/ai/reports/milestone-4.2-first-vertical-slice-implementation-report-2026-05-27.md`
- `docs/ai/reports/milestone-4.2-stabilization-validation-report-2026-05-27.md`
