# Next Chat Task — Milestone 3.4 Startup Planning (Cancel Order)

Use this brief in future chats to continue work without re-planning completed milestones.

## Active Milestone
- Milestone 3.4 — Cancel Order (`in-progress`)

## Objective
Milestone 3.4 startup planning + scope lock is complete; execute the first vertical implementation slice for cancellation workflow.

## Scope Lock (initial)
In scope for current next task:
- implement cancel transition for eligible statuses
- release reserved stock on cancellation
- block shipped cancellation transitions
- write cancellation activity logs
- add service/app/journey test coverage for cancellation and stock consistency

Out of scope for current slice:
- Milestone 4.x make/buy implementation
- unrelated UX polish
- broad order workflow refactors outside cancellation criteria

## Recommended Implementation Order
1. Service/model implementation slice for cancel transition + reservation release.
2. Tests (unit/service/journey) for valid cancel, invalid transitions, and stock consistency.
3. App/UI wiring for cancel action + user-facing error handling.
4. Full validation pass in Codex cloud.
5. Documentation sync (`completion-status`, `progress-log`, milestone report).

## Validation Commands (Codex cloud)
- `python -m pip install --upgrade pip`
- `pip install -r requirements.txt`
- `pip install -r requirements-dev.txt`
- `python -m compileall -q src tests`
- `pytest -q`

## Planning Evidence
- `docs/ai/reports/milestone-3.4-startup-planning-scope-lock-report-2026-05-27.md`
