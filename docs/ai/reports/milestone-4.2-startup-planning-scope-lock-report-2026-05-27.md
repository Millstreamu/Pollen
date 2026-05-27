# Milestone 4.2 Startup Planning + Scope Lock Report (2026-05-27)

## Task understood
Execute startup planning and scope lock for Milestone 4.2 (Start Batch) after Milestone 4.1 completion.

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

## Milestone 4.2 objective (locked)
Enable explicit **Start Batch** lifecycle transition for previously planned batches, with status and validation safety controls.

## In-scope for first Milestone 4.2 implementation slice
1. Add Start Batch service/app flow for batch records created in Milestone 4.1.
2. Permit transition only from planned/not-started state.
3. Set and persist start metadata (status transition and started timestamp).
4. Block invalid transitions (already started/completed/cancelled where applicable).
5. Add tests for successful start and invalid transition blocking.

## Out of scope for this first Milestone 4.2 slice
- Complete Batch mutation behavior and stock/material quantity changes (Milestone 4.3).
- Batch cancellation/rework UX beyond direct Start Batch transition.
- Money module accounting/profit impacts.
- Broad UI redesign beyond minimum required Start action affordance.

## Risks
- Transition integrity risk if start is allowed from invalid statuses.
- Regression risk to existing create-batch and order stock reservation flows.
- Timestamp consistency risk if mixed naive/aware datetime handling is introduced.

## Verification plan (Codex cloud)
- `python -m pip install --upgrade pip`
- `pip install -r requirements.txt`
- `pip install -r requirements-dev.txt`
- `python -m compileall -q src tests`
- `pytest -q`

## Tracking updates completed in this planning slice
- Updated milestone tracking and handoff to the Milestone 4.2 first vertical slice implementation.
- Recorded this startup planning evidence report for durable context.

## Next recommended action
Implement Milestone 4.2 first vertical slice: Start Batch transition endpoint/service behavior plus full regression and targeted tests.
