# Next Chat Task — Milestone 4.1 First Vertical Slice (Create Batch)

Use this brief in future chats to continue work without re-planning completed milestones.

## Active Milestone
- Milestone 4.1 — Create Batch first implementation slice (`in-progress`)

## Objective
Startup planning for Milestone 4.1 is complete; implement the first Create Batch vertical slice with tests and durable evidence.

## Scope Lock (initial)
In scope for current next task:
- add Create Batch service/app behavior for product + quantity planned batches
- validate quantity and required fields
- calculate/check material requirements for requested quantity
- block creation when materials are insufficient with actionable error output
- add/extend tests for create-batch success + insufficient-material paths
- publish implementation report and update milestone tracking

Out of scope for current slice:
- Start Batch transition logic (Milestone 4.2)
- Complete Batch stock/material mutation logic (Milestone 4.3)
- Money module features
- unrelated UX redesign

## Recommended Implementation Order
1. Implement Create Batch model/service/app flow (create-only lifecycle state).
2. Add tests that prove no stock/material mutation on create and proper insufficient-material blocking.
3. Run full Codex-cloud validation suite.
4. Publish implementation report and move milestone status to reflect first-slice completion progress.

## Validation Commands (Codex cloud)
- `python -m pip install --upgrade pip`
- `pip install -r requirements.txt`
- `pip install -r requirements-dev.txt`
- `python -m compileall -q src tests`
- `pytest -q`

## Planning Evidence
- `docs/ai/reports/milestone-3.4-completion-closeout-signoff-2026-05-27.md`
- `docs/ai/reports/milestone-4.1-startup-planning-scope-lock-report-2026-05-27.md`
- `project-roadmap.md`
