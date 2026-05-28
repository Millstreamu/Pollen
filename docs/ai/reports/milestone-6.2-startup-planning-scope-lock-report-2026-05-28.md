# Milestone 6.2 Startup Planning + Scope Lock Report (2026-05-28)

## Objective
Execute startup planning + scope lock for Milestone 6.2 (Today Actions), then prepare implementation handoff with explicit boundaries and validation plan.

## Inputs reviewed
- `project-roadmap.md` (Phase 6 / Milestone 6.2)
- `docs/ai/development-process.md`
- `docs/ai/completion-status.md` (updated for new active milestone)
- `src/pollen/app.py`
- `tests/test_today_summary.py`

## Milestone 6.2 definition (roadmap)
Goal:
- Allow common next actions from Today.

Scope:
- open order
- start packing
- open low stock item
- create batch
- create purchase

Acceptance criteria:
- actions route to correct workflow
- no hidden automation
- user remains in control

## Scan summary
- Today currently renders summary counts only (read-only cards) without action affordances.
- Existing route-based workflows already exist for orders, products, make/batches, and purchases; Milestone 6.2 should reuse these instead of inventing new mutation paths.
- Existing test coverage validates summary metrics; action routing tests will need to be added for links/buttons and route resolution behavior.

## Scope lock (Milestone 6.2 first implementation slice)
In scope for first implementation slice:
- Add explicit Today action affordances for:
  - open order(s)
  - start packing flow
  - open low stock products/materials
  - create batch
  - create purchase
- Wire actions to existing routes/workflows only.
- Add/extend tests to validate action visibility and expected target endpoints.

Out of scope for this slice:
- automatic status transitions from Today
- prioritization/scoring engines
- notifications/escalation logic
- milestone 7+ money analytics expansion

## Simplest safe approach
- Keep Today actions as plain links/buttons to existing pages/endpoints.
- Do not add background jobs or side-effectful “one-click automation” actions.
- Reuse established services and route handlers; prefer minimal template/view updates plus focused tests.

## Validation plan (Codex cloud)
- `python -m pip install --upgrade pip`
- `pip install -r requirements.txt`
- `pip install -r requirements-dev.txt`
- `python -m compileall -q src tests`
- `ruff check src tests`
- `pytest -q`

## Decisions and status transition
- Milestone 6.2 is now the active milestone.
- Milestone status transitioned from `not-started` to `in-progress` for implementation readiness.
- Next-chat handoff updated to Milestone 6.2 first vertical-slice implementation.

## Result
Startup planning and scope lock are complete for Milestone 6.2. The next required task is implementing the first vertical slice of Today action routing with tests.
