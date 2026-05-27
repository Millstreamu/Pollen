# Next Chat Task — Milestone 3.4 Startup Planning (Cancel Order)

Use this brief in future chats to continue work without re-planning completed milestones.

## Active Milestone
- Milestone 3.4 — Cancel Order (`in-progress`)

## Objective
Execute Milestone 3.4 startup planning + scope lock, then begin first vertical slice only after planning evidence is captured.

## Scope Lock (initial)
In scope for startup/planning:
- confirm roadmap acceptance criteria for order cancellation behavior
- define reservation-release behavior for cancellation
- identify required service/model/app/test touchpoints
- capture explicit in-scope vs out-of-scope boundaries

Out of scope during startup/planning:
- implementation of Milestone 4.x make/buy workflow
- unrelated UX polish
- broad order workflow refactors outside cancellation criteria

## Recommended Implementation Order
1. Planning and scope-lock report for Milestone 3.4.
2. Service/model implementation slice for cancel transition + reservation release.
3. Tests (unit/service/journey) for valid cancel, invalid transitions, and stock consistency.
4. App/UI wiring for cancel action + user-facing error handling.
5. Full validation pass in Codex cloud.
6. Documentation sync (`completion-status`, `progress-log`, milestone report).

## Validation Commands (Codex cloud)
- `python -m pip install --upgrade pip`
- `pip install -r requirements.txt`
- `pip install -r requirements-dev.txt`
- `python -m compileall -q src tests`
- `pytest -q`

## Planning Evidence
- `docs/ai/reports/milestone-3.3-release-validation-signoff-2026-05-27.md`
