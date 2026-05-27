# Next Chat Task — Milestone 4.1 Completion Closeout Validation

Use this brief in future chats to continue work without re-planning completed milestones.

## Active Milestone
- Milestone 4.1 — Create Batch (`release-candidate`)

## Objective
Milestone 4.1 release-candidate validation/signoff is complete. Execute completion closeout validation and produce final milestone completion evidence.

## Scope Lock (current)
In scope for current next task:
- run full Codex-cloud validation suite
- confirm Create Batch behavior remains regression-safe
- publish Milestone 4.1 completion closeout signoff report
- update milestone tracking artifacts from `release-candidate` to `complete`

Out of scope for current slice:
- Start Batch transition logic (Milestone 4.2)
- Complete Batch stock/material mutation logic (Milestone 4.3)
- Money module features
- unrelated UX redesign

## Recommended Implementation Order
1. Run validation commands and capture pass/fail output.
2. Publish Milestone 4.1 completion closeout signoff report.
3. Update completion status/progress log and advance next-chat handoff.

## Validation Commands (Codex cloud)
- `python -m pip install --upgrade pip`
- `pip install -r requirements.txt`
- `pip install -r requirements-dev.txt`
- `python -m compileall -q src tests`
- `pytest -q`

## Planning Evidence
- `docs/ai/reports/milestone-4.1-startup-planning-scope-lock-report-2026-05-27.md`
- `docs/ai/reports/milestone-4.1-first-vertical-slice-implementation-report-2026-05-27.md`
- `docs/ai/reports/milestone-4.1-release-candidate-validation-signoff-2026-05-27.md`
- `project-roadmap.md`
