# Milestone 1.2 Continuation Report (Shop-Scoped Persistence Slice)

Date: 2026-05-25  
Scope reference: `project-roadmap.md` → `Milestone 1.2 — Managed Auth and Shop Ownership`

## Task understood
Implement the Milestone 1.2 continuation slice so record scoping is persistence-backed (not only helper-level auth checks), and document the work using the AI development method.

## Task source
Direct human request in Codex chat: implement Milestone 1.2 continuation and write a report using AI dev method.

## Rule files read
- `AI_DEVELOPMENT.md`
- `docs/ai/development-process.md`
- `docs/ai/testing-rules.md`
- `docs/ai/task-execution-rules.md`
- `docs/ai/security-rules.md`
- `docs/ai/safety-critical-rules.md`
- `docs/ai/reporting-rules.md`

## Project memory files read
- `docs/ai/progress-log.md`
- `docs/ai/completion-status.md`
- `docs/ai/known-issues.md`
- `docs/ai/do-not-build-yet.md`
- `docs/ai/reports/milestone-1.2-implementation-report-2026-05-24.md`
- `docs/ai/reports/startup-report-milestone-1.2-shop-scoping-2026-05-24.md`

## Relevant repo files found
- `src/pollen/auth.py`
- `src/pollen/app.py`
- `src/pollen/models.py`
- `tests/test_app.py`
- `tests/test_models.py`

## Existing patterns observed
- In-memory deterministic test seams are used for milestone slices.
- Route auth checks already depend on `AuthService.resolve_context(...)`.
- Ownership helper existed, but persistence-backed record scoping was not present before this continuation.

## Planned changes
- Add one persistence-backed record path for orders with strict `shop_id` boundaries.
- Add a service that always derives `shop_id` from authenticated server context.
- Ignore client-provided shop identifier hints.
- Add regression tests for cross-shop denial and unauthenticated denial.

## What was implemented
- Added `src/pollen/orders.py` with:
  - `OrderRecord`
  - `OrderRepository.create(...)`
  - `OrderRepository.list_for_shop(...)`
  - `OrderRepository.get_for_shop(...)`
- Added `src/pollen/services.py` with `OrderService` methods:
  - `create_order(...)` (server-resolved shop scope; ignores `requested_shop_id`)
  - `list_orders(...)` (current-shop filtered)
  - `get_order(...)` (current-shop filtered)
- Added `tests/test_order_scoping.py` with regression tests for:
  - server-side shop assignment on create
  - list isolation by shop
  - cross-shop read denial
  - unauthenticated create/list/get denial

## What was intentionally not implemented
- No managed OAuth provider SDK wiring (out of this slice).
- No advanced role/invite system (explicitly out of milestone scope).
- No Phase 2 product/material/order workflow features.

## Acceptance criteria mapping
- Logged-out users cannot access private pages: covered by existing tests (`tests/test_app.py`).
- Logged-in user gets or creates a shop: covered by existing tests (`tests/test_app.py`).
- Records are scoped by `shop_id`: covered by new persistence-backed tests (`tests/test_order_scoping.py`).
- User cannot access another shop’s records: covered by new cross-shop read denial test.

## Tests/checks run
- `python -m pip install --upgrade pip`
- `pip install -r requirements.txt`
- `pip install -r requirements-dev.txt`
- `python -m compileall -q src tests`
- `pytest -q`

## Result
- Compile checks: pass.
- Test suite: pass (`15 passed`).

## Environment limitations
- Dev dependency installation remains environment-limited for index/proxy access (`pip install -r requirements-dev.txt` could not fetch pinned `pytest` from network index).
- Existing environment already had a working `pytest`, allowing local suite execution.

## Known limitations
- Persistence layer is in-memory only for deterministic milestone testing.

## Follow-up backlog items
- Wire real managed auth provider integration while preserving server-owned shop scoping.
- Introduce persistent datastore-backed repositories in a later scoped slice.

## Project memory files updated
- `docs/ai/completion-status.md`
- `docs/ai/progress-log.md`
- `docs/ai/reports/milestone-1.2-continuation-report-2026-05-25.md`
