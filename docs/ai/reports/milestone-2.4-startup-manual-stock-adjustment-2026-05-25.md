# Milestone 2.4 Startup Report — Manual Stock Adjustment

Date: 2026-05-25
Owner: Codex
Milestone: Milestone 2.4 — Manual Stock Adjustment
Status: startup-planned

## Task understood
Close Milestone 2.3 as complete after human sign-off, then begin Milestone 2.4 planning using the repo AI development method.

## Task source
- Human instruction in current task thread.
- Roadmap source of truth: `project-roadmap.md`.

## Rule files read
- `AI_DEVELOPMENT.md`
- `docs/ai/development-process.md`
- `docs/ai/task-execution-rules.md`
- `docs/ai/testing-rules.md`
- `docs/ai/finish-line-protocol.md`
- `docs/ai/reporting-rules.md`

## Project memory files read
- `docs/ai/progress-log.md`
- `docs/ai/completion-status.md`
- `docs/ai/known-issues.md`
- `docs/ai/do-not-build-yet.md`
- `docs/ai/project-roadmap.md` (pointer)
- `project-roadmap.md` (milestone source)

## Milestone 2.4 goal
Allow safe manual stock corrections for products/materials with reason capture and inventory/activity audit records.

## Planned scope (Milestone 2.4)
- Adjust product stock.
- Adjust material stock.
- Require adjustment reason.
- Create `InventoryMovement` record.
- Create `ActivityLog` record.

## Out of scope
- Any work beyond Milestone 2.4.
- Advanced inventory features not listed in roadmap scope.
- New integration/OAuth/payment capabilities.

## Acceptance criteria to satisfy
- Stock can be increased.
- Stock can be decreased.
- Negative stock is blocked unless explicitly allowed later.
- Movement record is created.
- Activity log is created.

## Required journey (from roadmap)
- Create material.
- Adjust stock.
- Confirm material stock changed.
- Confirm movement and activity log exist.

## Risks
- Data integrity risk when decreasing stock near zero.
- Missing audit metadata if reason or actor context is not enforced.
- Cross-shop safety risk if stock adjustments are not strictly shop-scoped.

## Planned implementation slices
1. Domain/data model slice for inventory movement + activity log entities.
2. Service layer stock-adjust API with validation, reason requirement, and shop scoping.
3. UI/API wiring for adjustment flows.
4. Test slices: unit/service + journey coverage for increase/decrease and negative-stock block.

## Validation plan
- `python -m pip install --upgrade pip`
- `pip install -r requirements.txt`
- `pip install -r requirements-dev.txt`
- `python -m compileall -q src tests`
- `pytest -q`

## Current decision
Milestone 2.3 is signed off and marked complete. Milestone 2.4 is now active and planned; implementation is not started in this startup report.
