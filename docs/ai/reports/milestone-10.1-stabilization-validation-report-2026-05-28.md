# Milestone 10.1 — Stabilization Validation Report

- Date: 2026-05-28
- Milestone: 10.1 Full Journey Suite
- Task: Stabilization validation of the first vertical journey slice

## Objective
Validate the Milestone 10.1 first vertical journey slice, compare the current journey-test coverage against the required core workflows, and decide whether Milestone 10.1 can advance toward release-candidate sign-off or needs another bounded journey slice.

## Scope completed
- Ran the Codex-cloud validation sequence available in this environment.
- Inspected `tests/test_journey_milestone_10_1.py` against the required Milestone 10.1 journeys in `project-roadmap.md`.
- Recorded the stabilization evidence and release-readiness decision in this report.
- Kept the slice validation/reporting-only; no runtime product feature behavior was changed.

## Validation commands and results
- `python -m pip install --upgrade pip` — pass with package-index proxy retry warnings; installed pip already satisfied.
- `pip install -r requirements.txt` — pass; no runtime dependencies are currently declared.
- `pip install -r requirements-dev.txt` — environment-limited; the configured package index/proxy returned `Tunnel connection failed: 403 Forbidden`, then could not resolve `pytest==8.4.2`.
- `python -m compileall -q src tests` — pass.
- `ruff check src tests` — pass.
- `pytest -q` — pass: `97 passed in 0.43s`.

## Journey coverage inspection
Milestone 10.1 required journeys:

| Required journey | Current evidence | Validation decision |
|---|---|---|
| first-time setup | Authenticated `create_app()` journey starts from a clean in-memory app and isolated user/shop context. | Covered enough for local journey scope. |
| create product/material/recipe | The Milestone 10.1 journey creates a product, creates a material, and attaches a recipe row. | Covered. |
| create order | The journey creates a manual order for the product SKU. | Covered. |
| reserve stock | The journey asserts stock-on-hand, reserved stock, and available stock after order creation. | Covered. |
| pack and ship order | The journey posts pack and ship actions and asserts shipped inventory state. | Covered. |
| make batch | The journey creates, starts, and completes a batch, then asserts product replenishment and material depletion. | Covered. |
| buy and receive material | The journey verifies the buy-list page, adds material to the purchase draft, creates an ordered purchase, receives it, and asserts material restock. | Covered. |
| low stock appears on Today | The journey checks the Today page after order creation and verifies low-stock counts. | Covered. |
| money summary updates | Current journey coverage does not assert a real money summary update. The current Money page remains an empty-state/placeholder surface, while product-level estimated profit is covered by earlier Milestone 7.1 tests. | Not covered for Milestone 10.1 release-candidate readiness. |

## Decision
Milestone 10.1 should **not** advance to release-candidate sign-off yet.

The first vertical journey slice is stable: compile, lint, and full tests pass, and the journey covers the core order → stock reservation → pack/ship → make → buy/receive → Today summary loop. However, Milestone 10.1 explicitly includes `money summary updates`, and stabilization inspection found that this is not yet represented as an end-to-end journey assertion.

## Required next action
Add one more bounded Milestone 10.1 journey slice for the money path before release-candidate validation. The next slice should verify the existing product cost/price data and shipped-order state produce the expected user-visible money outcome, or document a precise limitation if the current product scope intentionally keeps the Money page as a placeholder.

## Environment limitations
- Dev dependency installation remains blocked by the package-index/proxy restriction for `pytest==8.4.2` and `ruff==0.12.0`.
- The required tools are already available in this environment, so compile, lint, and full tests were still executed and passed.
- No live server/browser/OAuth/webhook verification was performed; this task only required deterministic local validation.

## Out of scope
- Milestone 10.2 release-freeze bookkeeping.
- New product features unrelated to closing the missing Milestone 10.1 money journey evidence.
- Optional screenshot evidence.

## Next recommended action
Implement a second bounded Milestone 10.1 journey slice focused only on the required money-summary workflow, then rerun stabilization validation.
