# Next Chat Task — Milestone 3.4 Startup Planning (Cancel Order)

Use this brief in future chats to continue work without re-planning completed milestones.

## Active Milestone
- Milestone 3.4 — Cancel Order (`stabilising`)

## Objective
Milestone 3.4 first vertical slice is implemented and validated; execute release-flow validation/sign-off to move to release-candidate.

## Scope Lock (initial)
In scope for current next task:
- run full Codex-cloud validation commands
- record Milestone 3.4 stabilising evidence in durable report
- update milestone tracking + next-task handoff toward release-candidate sign-off

Out of scope for current slice:
- new cancellation behavior beyond already approved scope
- Milestone 4.x make/buy implementation
- unrelated UX polish

## Recommended Implementation Order
1. Execute full validation pass in Codex cloud.
2. Confirm no regressions in cancellation/stock workflows.
3. Update status docs (`completion-status`, `progress-log`, `next-chat-task`).
4. Publish Milestone 3.4 stabilising report with command evidence.

## Validation Commands (Codex cloud)
- `python -m pip install --upgrade pip`
- `pip install -r requirements.txt`
- `pip install -r requirements-dev.txt`
- `python -m compileall -q src tests`
- `pytest -q`

## Planning Evidence
- `docs/ai/reports/milestone-3.4-startup-planning-scope-lock-report-2026-05-27.md`
- `docs/ai/reports/milestone-3.4-first-vertical-slice-implementation-report-2026-05-27.md`
