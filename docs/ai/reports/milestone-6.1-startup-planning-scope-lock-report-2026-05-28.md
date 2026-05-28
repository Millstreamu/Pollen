# Milestone 6.1 Startup Planning + Scope Lock Report (2026-05-28)

## Task understood
Execute startup planning + scope lock for Milestone 6.1 (Today Data Summary), then prepare implementation handoff with explicit boundaries and validation plan.

## Task source
- `docs/ai/next-chat-task.md`
- `project-roadmap.md` (Phase 6 / Milestone 6.1)

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

## Scope lock (Milestone 6.1 first implementation slice)

### In scope for the next implementation slice
- Add a read-only Today summary service that aggregates dashboard-ready operational counts.
- Include minimum required action buckets:
  - orders to pack
  - low stock materials
  - materials to buy
  - batches in progress
  - purchases due
- Wire service behavior in current backend architecture without introducing workflow mutations.
- Add tests that verify summary counts from representative in-memory dataset states.

### Explicitly out of scope
- Advanced prioritization/scoring/ranking logic.
- UI redesign or broader dashboard interaction changes.
- Notificationing/escalation automation.
- Forecasting or predictive planning features.

## Risks noted
- Count semantics may drift if status/category rules are not explicitly encoded.
- Service should remain read-only; accidental write side effects would violate scope.
- “Materials to buy” and “low stock” may overlap conceptually; tests must assert intended separation.

## Validation plan (Codex cloud)
- `python -m pip install --upgrade pip`
- `pip install -r requirements.txt`
- `pip install -r requirements-dev.txt`
- `python -m compileall -q src tests`
- `ruff check src tests`
- `pytest -q`

## Execution result
- Startup planning and scope lock completed for Milestone 6.1.
- Next-chat handoff prepared for Milestone 6.1 first vertical-slice implementation.
- Validation suite executed and passing (with known dev-dependency index limitation documented in project history).
