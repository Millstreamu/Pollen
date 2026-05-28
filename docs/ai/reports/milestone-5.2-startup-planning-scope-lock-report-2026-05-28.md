# Milestone 5.2 Startup Planning + Scope Lock Report (2026-05-28)

## Task understood
Execute startup planning + scope lock for Milestone 5.2 (Create Purchase), then transition milestone tracking to `in-progress` with durable evidence.

## Task source
- `docs/ai/next-chat-task.md`
- `project-roadmap.md` (Phase 5 / Milestone 5.2)

## Rule files read
- `AI_DEVELOPMENT.md`
- `docs/ai/development-process.md`
- `docs/ai/testing-rules.md`
- `docs/ai/task-execution-rules.md`
- `docs/ai/report-format.md`

## Project memory files read
- `docs/ai/project-rules.md`
- `docs/ai/progress-log.md`
- `docs/ai/completion-status.md`
- `docs/ai/known-issues.md`
- `docs/ai/do-not-build-yet.md`

## Scope lock (Milestone 5.2 first implementation slice)

### In scope for the next implementation slice
- Create persisted Purchase records from Make/Buy flow.
- Add purchase fields required by roadmap scope: supplier (optional), expected date (optional), and status (`Draft`/`Ordered`).
- Support adding purchase line items for materials + quantity.
- Ensure purchase creation does **not** mutate material stock.
- Ensure created purchases are visible in Buy page listing.
- Add tests for successful creation and no-stock-mutation behavior.

### Explicitly out of scope
- Purchase receiving stock mutation workflow (Milestone 5.3).
- InventoryMovement creation on receiving (Milestone 5.3).
- ActivityLog receiving audit flow (Milestone 5.3).
- Supplier automation, lead-time prediction, or advanced procurement UX.
- Broad UI redesign outside minimal Milestone 5.2 workflow.

## Risks noted
- Accidental stock mutation at purchase creation time would violate roadmap acceptance criteria.
- Status transition behavior can creep into Milestone 5.3 if not constrained.
- Optional-field handling (supplier/expected date) needs deterministic defaults.

## Validation plan (Codex cloud)
- `python -m pip install --upgrade pip`
- `pip install -r requirements.txt`
- `pip install -r requirements-dev.txt`
- `python -m compileall -q src tests`
- `ruff check src tests`
- `pytest -q`

## Execution result
- Startup planning and scope lock completed.
- Milestone tracking transitioned to `in-progress` for Milestone 5.2.
- Next-chat handoff updated to first vertical-slice implementation for Milestone 5.2.
- Validation suite executed and passing (with known dev-dependency index limitation documented in progress history).
