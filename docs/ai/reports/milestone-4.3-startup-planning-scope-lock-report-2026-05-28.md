# Milestone 4.3 Startup Planning + Scope Lock Report (2026-05-28)

## Task understood
Execute startup planning and scope lock for Milestone 4.3 (Complete Batch) after Milestone 4.2 completion.

## Task source
- `docs/ai/next-chat-task.md`
- `project-roadmap.md`

## Rule and memory files read
- `AI_DEVELOPMENT.md`
- `docs/ai/development-process.md`
- `docs/ai/project-rules.md`
- `docs/ai/progress-log.md`
- `docs/ai/completion-status.md`
- `docs/ai/known-issues.md`
- `docs/ai/do-not-build-yet.md`
- `docs/ai/testing-rules.md`
- `docs/ai/task-execution-rules.md`

## Milestone 4.3 objective (locked)
Enable explicit **Complete Batch** lifecycle transition for in-progress batches with safe, atomic stock mutation behavior.

## In-scope for first Milestone 4.3 implementation slice
1. Add Complete Batch service/app flow for batches currently in `in-progress` state.
2. Permit transition only from `in-progress` and block invalid status transitions.
3. Decrease required material quantities according to recipe * batch quantity at completion time.
4. Increase finished product stock by batch quantity at completion time.
5. Persist completion metadata (status transition and completion timestamp).
6. Add tests for successful completion mutation and blocked invalid transitions.
7. Add/extend journey coverage for create -> start -> complete workflow stock integrity.

## Out of scope for this first Milestone 4.3 slice
- Rework, undo, or cancellation after completion.
- Multi-step partial completion flows.
- Purchasing automation enhancements beyond existing material stock updates.
- Money/profit accounting impacts from batch completion.
- Broad Make/Buy UX redesign beyond minimum required Complete action affordance.

## Risks
- Double-apply mutation risk if completion endpoint can be retried without idempotency/status gate.
- Data-integrity risk if material decrement and product increment are not committed together.
- Regression risk to order reservation/pack/ship stock consistency invariants.
- Validation risk if recipe/material existence assumptions are not enforced during completion.

## Verification plan (Codex cloud)
- `python -m pip install --upgrade pip`
- `pip install -r requirements.txt`
- `pip install -r requirements-dev.txt`
- `python -m compileall -q src tests`
- `ruff check src tests`
- `pytest -q`

## Tracking updates completed in this planning slice
- Updated milestone tracking and handoff to the Milestone 4.3 first vertical slice implementation.
- Recorded this startup planning evidence report for durable context.

## Next recommended action
Implement Milestone 4.3 first vertical slice: Complete Batch transition endpoint/service behavior with atomic material/product stock mutation plus full regression and journey validation.
