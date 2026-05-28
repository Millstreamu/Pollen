# Milestone 8.1 Startup Planning + Scope Lock Report (2026-05-28)

## Objective
Execute startup planning + scope lock for Milestone 8.1 (Integration Architecture), then prepare implementation handoff with explicit boundaries and a Codex-safe validation plan.

## Inputs reviewed
- `project-roadmap.md` (Phase 8 / Milestone 8.1 and 8.2 sequencing)
- `docs/ai/development-process.md`
- `docs/ai/next-chat-task.md`
- `docs/ai/completion-status.md`
- `docs/ai/progress-log.md`
- existing service boundaries under `src/pollen/` and tests under `tests/`

## Milestone 8.1 definition (roadmap)
Goal:
- Add safe integration structure without live automation.

Scope:
- integration client interfaces
- sync job model/log if needed
- external ID storage
- mocked fixtures
- error handling

Acceptance criteria:
- integration logic is isolated
- tests can run without live API
- failures are visible
- duplicate protection strategy exists

## Scan summary
- Current app workflows are manual-first and stable through Milestone 7.1, which satisfies the roadmap prerequisite for starting integrations.
- Existing architecture can absorb a new integration service module without touching live auth/network flows.
- Tests currently run fully in local/Codex contexts; milestone design must preserve offline fixture testing as a hard requirement.

## Scope lock (Milestone 8.1 first implementation slice)
In scope for first implementation slice:
- Add explicit integration interface abstraction for Etsy-like order input.
- Add external source ID tracking for imported orders and duplicate detection guardrails.
- Add fixture-driven mocked import execution path + unit/service tests.
- Add visible error capture/logging path for failed import attempts.

Out of scope for this slice:
- live OAuth credentials, tokens, or API calls
- webhook/event-driven auto-sync
- stock push back to Etsy or other channels
- advanced reconciliation UX beyond basic visibility

## Simplest safe approach
- Define thin protocol/interface + one mocked adapter implementation.
- Keep import orchestration in a service module with explicit duplicate checks before order creation.
- Persist minimal sync/error metadata required for operator visibility and debugging.
- Validate via deterministic fixtures and tests only; no external network in default test path.

## Risks and mitigations
- **Risk:** coupling import logic directly to order routes could leak integration concerns across the app.  
  **Mitigation:** isolate mapping/orchestration inside a dedicated service layer boundary.
- **Risk:** duplicate imports create over-reservation or duplicate orders.  
  **Mitigation:** enforce external ID uniqueness strategy before write operations and test idempotency paths.
- **Risk:** hidden failures reduce operator trust.  
  **Mitigation:** add explicit error logging/report records visible to future UI/reporting surfaces.

## Validation plan (Codex cloud)
- `python -m pip install --upgrade pip`
- `pip install -r requirements.txt`
- `pip install -r requirements-dev.txt`
- `python -m compileall -q src tests`
- `ruff check src tests`
- `pytest -q`

## Decisions and status transition
- Milestone 8.1 is now the active milestone.
- Milestone status transitioned from `not-started` to `in-progress` after startup planning scope lock completion.
- Next-chat handoff updated to Milestone 8.1 first vertical-slice implementation.

## Result
Startup planning and scope lock are complete for Milestone 8.1. The next required task is implementing the first vertical slice of mocked integration architecture with duplicate protection and failure visibility tests.
