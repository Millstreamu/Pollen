# Next Chat Task — Milestone 4.2 Completion Closeout Validation + Sign-off

Use this brief in future chats to continue work without re-planning completed slices.

## Active Milestone
- Milestone 4.2 — Start Batch (`release-candidate`)

## Objective
Execute completion-closeout validation/sign-off for Milestone 4.2 and transition to `complete` if checks pass.

## Scope Lock (current)
In scope for current next task:
- run full Codex-cloud validation commands
- confirm Start Batch transition behavior remains regression-safe
- update milestone status from `release-candidate` to `complete` if checks pass
- publish completion closeout report and update milestone tracking artifacts

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

## Evidence
- `docs/ai/reports/milestone-4.2-startup-planning-scope-lock-report-2026-05-27.md`
- `docs/ai/reports/milestone-4.2-first-vertical-slice-implementation-report-2026-05-27.md`
- `docs/ai/reports/milestone-4.2-stabilization-validation-report-2026-05-27.md`
- `docs/ai/reports/milestone-4.2-release-candidate-validation-signoff-2026-05-27.md`
