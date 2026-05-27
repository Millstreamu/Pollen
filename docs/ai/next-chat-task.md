# Next Chat Task — Milestone 4.2 First Vertical Slice Implementation

Use this brief in future chats to continue work without re-planning completed slices.

## Active Milestone
- Milestone 4.2 — Start Batch (`in-progress`)

## Objective
Startup planning and scope lock are complete. Implement the first vertical slice of Milestone 4.2: Start Batch transition behavior.

## Scope Lock (current)
In scope for current next task:
- implement Start Batch transition for existing planned batches
- enforce status gate: planned -> in-progress only
- persist started timestamp and status mutation
- return clear errors for invalid transitions
- add/extend tests for success and blocked transitions
- publish implementation report and update milestone tracking artifacts

Out of scope for current slice:
- Complete Batch stock/material mutation logic (Milestone 4.3)
- Money module features
- unrelated UX redesign

## Recommended Implementation Order
1. Add service/model/app transition logic for Start Batch.
2. Add tests for valid and invalid transition paths.
3. Run compile + full test suite.
4. Publish Milestone 4.2 implementation report and update tracking files.

## Validation Commands (Codex cloud)
- `python -m pip install --upgrade pip`
- `pip install -r requirements.txt`
- `pip install -r requirements-dev.txt`
- `python -m compileall -q src tests`
- `pytest -q`

## Planning Evidence
- `docs/ai/reports/milestone-4.2-startup-planning-scope-lock-report-2026-05-27.md`
- `docs/ai/reports/milestone-4.1-completion-closeout-signoff-2026-05-27.md`
- `project-roadmap.md`
